#!/usr/bin/env python3
import os
import glob
import sys
import time
from typing import Tuple, List

def clear_screen():    
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the program header"""
    print("=" * 60)
    print("Build System Generator".center(60))
    print("=" * 60)
    print()

def get_dir_name() -> str:    
    default_name = "new_project"
    while True:        
        print(f"\nEnter directory for project [default: {default_name}]: ", end='')
        print("\nThis will also be the default project name.")
        name = input().strip()
        if not name:
            return default_name
        if name.isalnum() or '_' in name:
            return name
        print("Invalid name! Use only alphanumeric characters and underscores.")


def get_source_files(lang: str) -> Tuple[List[str], List[str]]:    
    if lang == 'C':
        src_files = glob.glob("**/*.c", recursive=True)
        header_files = glob.glob("**/*.h", recursive=True)
    elif lang == 'C++':
        src_files = glob.glob("**/*.cpp", recursive=True) + glob.glob("**/*.cc", recursive=True)
        header_files = glob.glob("**/*.hpp", recursive=True) + glob.glob("**/*.h", recursive=True)
    else:  # Java
        src_files = glob.glob("**/*.java", recursive=True)
        header_files = []  # Java doesn't have separate header files
    
    # Remove any files from subdirectories that start with 'obj/' or 'build/'
    src_files = [f for f in src_files if not f.startswith(('obj/', 'build/'))]
    header_files = [f for f in header_files if not f.startswith(('obj/', 'build/'))]
    
    return src_files, header_files

def generate_traditional_makefile(target_name: str, lang: str):
    if lang == 'C':
        compiler = 'gcc'
        src_ext = 'c'
    elif lang == 'C++':
        compiler = 'g++'
        src_ext = 'cpp'
    else:  # Java
        makefile_content = """# Compiler settings
JAVAC = javac
JAVA = java
JFLAGS = -d build

# Source files
SOURCES = $(shell find . -name "*.java")
CLASSES = $(SOURCES:%.java=build/%.class)

# Main class (change this to your main class name)
MAIN_CLASS = {target}

# Default rule
all: build $(CLASSES)

# Create build directory
build:
	mkdir -p build

# Compile rule
build/%.class: %.java
	$(JAVAC) $(JFLAGS) $<

# Run rule
run: all
	$(JAVA) -cp build $(MAIN_CLASS)

# Clean rule
clean:
	rm -rf build

.PHONY: all clean run build
""".format(target=target_name)
        
        with open('Makefile', 'w') as f:
            f.write(makefile_content)
        
        if not os.path.exists('build'):
            os.makedirs('build')
        return

    # For C/C++
    makefile_content = """# Compiler settings
CC = {compiler}
CFLAGS = -Wall -Wextra -I.

# Get all source files
SRC = $(wildcard *.{src_ext})
OBJ = $(patsubst %.{src_ext},obj/%.o,$(SRC))

# Main target
TARGET = {target}

# Default rule
all: obj $(TARGET)

# Create obj directory
obj:
	mkdir -p obj

# Link rule
$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET)

# Compile rule
obj/%.o: %.{src_ext}
	$(CC) $(CFLAGS) -c $< -o $@

# Clean rule
clean:
	rm -rf obj $(TARGET)

# Dependencies
-include $(OBJ:.o=.d)

# Generate dependencies
obj/%.d: %.{src_ext}
	@set -e; rm -f $@; \\
	$(CC) -MM $(CFLAGS) $< > $@.$$$$; \\
	sed 's,\\($*\\)\\.o[ :]*,obj/\\1.o $@ : ,g' < $@.$$$$ > $@; \\
	rm -f $@.$$$$

.PHONY: all clean obj
""".format(compiler=compiler, src_ext=src_ext, target=target_name)

    with open('Makefile', 'w') as f:
        f.write(makefile_content)
    
    if not os.path.exists('obj'):
        os.makedirs('obj')

def generate_cmake(target_name: str, src_files: List[str], header_files: List[str], lang: str):
    src_files_str = ' '.join(src_files)
    
    if lang == 'C':
        lang_std = 'C_STANDARD 11'
        project_lang = 'C'
    elif lang == 'C++':
        lang_std = 'CXX_STANDARD 17'
        project_lang = 'CXX'
    else:  # Java
        cmake_content = """cmake_minimum_required(VERSION 3.10)

# Set project name
project({target} Java)

# Find Java
find_package(Java REQUIRED)
include(UseJava)

# Set Java source files
file(GLOB_RECURSE JAVA_SOURCES "*.java")

# Create jar file
add_jar(${{PROJECT_NAME}}
    SOURCES ${{JAVA_SOURCES}}
    ENTRY_POINT {target}
)

# Install rules
install_jar(${{PROJECT_NAME}} DESTINATION bin)
""".format(target=target_name)

        with open('CMakeLists.txt', 'w') as f:
            f.write(cmake_content)
        return

    # For C/C++
    cmake_content = """cmake_minimum_required(VERSION 3.10)

# Set project name and language
project({target} {lang})

# Set language standard
set(CMAKE_{lang_std})
set(CMAKE_{lang_std}_REQUIRED ON)

# Set compiler flags
add_compile_options(-Wall -Wextra)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/lib)

# Create list of source files
set(SOURCES
    {sources}
)

# Create executable target
add_executable(${{PROJECT_NAME}} ${{SOURCES}})

# Add include directories
target_include_directories(${{PROJECT_NAME}} PRIVATE
    ${{CMAKE_CURRENT_SOURCE_DIR}}
)

# Install rules
install(TARGETS ${{PROJECT_NAME}}
    RUNTIME DESTINATION bin
)
""".format(target=target_name, lang=project_lang, lang_std=lang_std, sources=src_files_str)

    with open('CMakeLists.txt', 'w') as f:
        f.write(cmake_content)

def show_file_summary(src_files: List[str], header_files: List[str], lang: str):    
    print("\nSource Files Found:")
    print("-" * 40)
    if lang == 'Java':
        print(f"Java Files ({len(src_files)}):")
    else:
        print(f"Source Files ({len(src_files)}):")
    for f in src_files:
        print(f"  - {f}")
    
    if header_files:  # Only show header files for C/C++
        print(f"\nHeader Files ({len(header_files)}):")
        for f in header_files:
            print(f"  - {f}")
    print("\nPress Enter to continue...")
    input()

def create_sample_files(dir_name: str, lang: str):
    os.makedirs(dir_name, exist_ok=True)
    os.chdir(dir_name)
    
    if lang == 'C':
        with open('main.c', 'w') as f:
            f.write("""#include "main.h"

int main(int argc, char *argv[]) {
    printf("Hello, World!\\n");
    return 0;
}""")
        
        with open('main.h', 'w') as f:
            f.write("""#ifndef MAIN_H
#define MAIN_H

#include <stdio.h>
#include <stdlib.h>

#endif // MAIN_H""")
            
    elif lang == 'C++':
        with open('main.cpp', 'w') as f:
            f.write("""#include "main.hpp"

int main(int argc, char* argv[]) {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}""")
        
        with open('main.hpp', 'w') as f:
            f.write("""#ifndef MAIN_HPP
#define MAIN_HPP

#include <iostream>
#include <string>

#endif // MAIN_HPP""")
            
    else:  # Java
        with open(f'{dir_name}.java', 'w') as f:
            f.write(f"""public class {dir_name} {{
    public static void main(String[] args) {{
        System.out.println("Hello, World!");
    }}
}}""")
    
    with open('README.md', 'w') as f:
        f.write(f"# {dir_name}\nA new {lang} project.")

def main_menu():    
    while True:
        clear_screen()
        print_header()
        
        print("Main Menu:")
        print("1. Show source files summary")
        print("2. Generate traditional Makefile")
        print("3. Generate CMake files")
        print("4. Start new project")
        print("5. Exit")
        print("\nChoice: ", end='')
        
        choice = input().strip()
        
        if choice in ['1', '2', '3']:
            print("\nSelect language:")
            print("1. C")
            print("2. C++")
            print("3. Java")
            lang_choice = input("\nChoice: ").strip()
            lang = {'1': 'C', '2': 'C++', '3': 'Java'}[lang_choice]
            
            src_files, header_files = get_source_files(lang)
            
            if not src_files and choice in ['2', '3']:
                print(f"\nError: No {lang} source files found in the current directory!")
                print("Press Enter to continue...")
                input()
                continue
        
        if choice == '1':
            show_file_summary(src_files, header_files, lang)
        elif choice == '2':
            target_name = get_target_name()
            generate_traditional_makefile(target_name, lang)
            show_success_message('make', target_name)
        elif choice == '3':
            target_name = get_target_name()
            generate_cmake(target_name, src_files, header_files, lang)
            show_success_message('cmake', target_name)
        elif choice == '4':
            dir_name = get_dir_name()
            print("\nSelect language:")
            print("1. C")
            print("2. C++")
            print("3. Java")
            lang_choice = input("\nChoice: ").strip()
            lang = {'1': 'C', '2': 'C++', '3': 'Java'}[lang_choice]
            
            create_sample_files(dir_name, lang)
            print(f"\nNew {lang} project '{dir_name}' created successfully!")
            print("\nPress Enter to return to main menu...")
            input()
        elif choice == '5':
            clear_screen()
            print("Thank you for using Build System Generator!")
            sys.exit(0)
        else:
            print("\nInvalid choice! Press Enter to try again...")
            input()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(1)