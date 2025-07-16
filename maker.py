#!/usr/bin/env python3
"""
Build System Generator - A comprehensive tool for generating build systems

This module provides functionality to generate Makefiles and CMake files for
C, C++, and Java projects. It includes features for architecture targeting,
configuration management, and project template creation.

Author: Build System Generator Team
Version: 2.0
Created: 2024
License: Open Source

Features:
    - Multi-language support (C, C++, Java)
    - Architecture targeting (32-bit, 64-bit, native)
    - Configuration management with persistent settings
    - Project template generation
    - Automatic source file discovery
    - Cross-platform compatibility

Dependencies:
    - Python 3.6+
    - GCC/G++ (for C/C++ projects)
    - Java Development Kit (for Java projects)
    - CMake (optional, for CMake build system)

Usage:
    python maker.py

Configuration:
    Settings are stored in maker_config.json and include:
    - Default architecture targeting
    - Compiler flags for each language
    - Default project directory names
    - Preferred build system
    - Auto-directory creation preferences
"""

import os
import glob
import sys
import time
import json
from typing import Tuple, List, Dict, Any

def clear_screen():
    """
    Clear the terminal screen in a cross-platform manner.
    
    Uses 'cls' command on Windows and 'clear' command on Unix-like systems.
    This provides a consistent user experience across different operating systems.
    
    Returns:
        None
    
    Example:
        >>> clear_screen()  # Screen is cleared
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config() -> Dict[str, Any]:
    """
    Load configuration settings from maker_config.json file.
    
    Loads user configuration from the JSON file and merges it with default
    settings to ensure all required keys are present. If the config file
    doesn't exist or is corrupted, returns default configuration.
    
    Returns:
        Dict[str, Any]: Configuration dictionary containing:
            - default_architecture: Target architecture ('32', '64', 'native')
            - default_compiler_flags: Language-specific compiler flags
            - default_project_dir: Default project directory name
            - custom_flags: User-defined custom flags
            - preferred_build_system: Preferred build system ('make', 'cmake')
            - auto_create_directories: Whether to auto-create directories
    
    Raises:
        None: Function handles all exceptions gracefully
    
    Example:
        >>> config = load_config()
        >>> print(config['default_architecture'])
        '64'
    """
    config_file = 'maker_config.json'
    default_config = {
        'default_architecture': '64',
        'default_compiler_flags': {
            'C': '-Wall -Wextra -O2',
            'C++': '-Wall -Wextra -O2 -std=c++17',
            'Java': '-Xlint:all'
        },
        'default_project_dir': 'new_project',
        'custom_flags': {},
        'preferred_build_system': 'make',
        'auto_create_directories': True
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Warning: Invalid config file. Using defaults.")
    
    return default_config

def save_config(config: Dict[str, Any]):
    """
    Save configuration settings to maker_config.json file.
    
    Persists the current configuration dictionary to disk as JSON.
    Handles file writing errors gracefully with user feedback.
    
    Args:
        config (Dict[str, Any]): Configuration dictionary to save
    
    Returns:
        None
    
    Raises:
        Exception: Catches and reports any file writing errors
    
    Example:
        >>> config = load_config()
        >>> config['default_architecture'] = '32'
        >>> save_config(config)
        Configuration saved to maker_config.json
    """
    config_file = 'maker_config.json'
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to {config_file}")
    except Exception as e:
        print(f"Error saving config: {e}")

def manage_config():
    """
    Interactive configuration management interface.
    
    Provides a menu-driven interface for users to modify configuration
    settings including architecture, project directories, build systems,
    and compiler flags. Changes are persisted to the config file.
    
    Menu Options:
        1. Default Architecture - Set 32/64-bit or native targeting
        2. Default Project Directory - Set default project folder name
        3. Preferred Build System - Choose between Make or CMake
        4. Auto Create Directories - Toggle automatic directory creation
        5. Manage Compiler Flags - Configure language-specific flags
        6. Save and Return - Save changes and return to main menu
        7. Cancel and Return - Return without saving changes
        8. Reset to Defaults - Reset all settings to default values
    
    Returns:
        None
    
    Example:
        >>> manage_config()  # Opens interactive configuration menu
    """
    config = load_config()
    
    while True:
        clear_screen()
        print("=" * 60)
        print("Configuration Management".center(60))
        print("=" * 60)
        print()
        
        print("Current Configuration:")
        print(f"1. Default Architecture: {config['default_architecture']}")
        print(f"2. Default Project Directory: {config['default_project_dir']}")
        print(f"3. Preferred Build System: {config['preferred_build_system']}")
        print(f"4. Auto Create Directories: {config['auto_create_directories']}")
        print("5. Manage Compiler Flags")
        print("6. Save and Return to Main Menu")
        print("7. Cancel and Return to Main Menu (without saving)")
        print("8. Reset to Defaults")
        print()
        
        choice = input("Choice: ").strip()
        
        if choice == '1':
            print("\nSelect default architecture:")
            print("1. 64-bit")
            print("2. 32-bit")
            print("3. Native")
            arch_choice = input("Choice: ").strip()
            arch_map = {'1': '64', '2': '32', '3': 'native'}
            if arch_choice in arch_map:
                config['default_architecture'] = arch_map[arch_choice]
                
        elif choice == '2':
            new_dir = input(f"Enter default project directory [{config['default_project_dir']}]: ").strip()
            if new_dir:
                config['default_project_dir'] = new_dir
                
        elif choice == '3':
            print("\nSelect preferred build system:")
            print("1. Make")
            print("2. CMake")
            build_choice = input("Choice: ").strip()
            if build_choice == '1':
                config['preferred_build_system'] = 'make'
            elif build_choice == '2':
                config['preferred_build_system'] = 'cmake'
                
        elif choice == '4':
            config['auto_create_directories'] = not config['auto_create_directories']
            
        elif choice == '5':
            manage_compiler_flags(config)
            
        elif choice == '6':
            save_config(config)
            break
            
        elif choice == '7':
            print("Configuration changes cancelled. Returning to main menu.")
            time.sleep(1)
            break
            
        elif choice == '8':
            config = load_config()  # Reset to defaults
            print("Configuration reset to defaults.")
            time.sleep(1)
            
        else:
            print("Invalid choice!")
            time.sleep(1)

def manage_compiler_flags(config: Dict[str, Any]):
    """
    Interactive compiler flags management interface.
    
    Allows users to customize compiler flags for C, C++, and Java languages.
    Provides a menu-driven interface to edit flags for each supported language.
    Changes are made to the provided configuration dictionary.
    
    Args:
        config (Dict[str, Any]): Configuration dictionary to modify
    
    Returns:
        None: Modifies the config dictionary in place
    
    Menu Options:
        1. Edit C flags - Modify GCC compiler flags
        2. Edit C++ flags - Modify G++ compiler flags  
        3. Edit Java flags - Modify JavaC compiler flags
        4. Return to config menu - Exit to main config menu
    
    Example:
        >>> config = load_config()
        >>> manage_compiler_flags(config)  # Opens flags management menu
    """
    while True:
        clear_screen()
        print("=" * 60)
        print("Compiler Flags Management".center(60))
        print("=" * 60)
        print()
        
        print("Current Compiler Flags:")
        for lang, flags in config['default_compiler_flags'].items():
            print(f"{lang}: {flags}")
        print()
        
        print("1. Edit C flags")
        print("2. Edit C++ flags")
        print("3. Edit Java flags")
        print("4. Return to config menu")
        
        choice = input("Choice: ").strip()
        
        if choice == '1':
            new_flags = input(f"Enter C flags [{config['default_compiler_flags']['C']}]: ").strip()
            if new_flags:
                config['default_compiler_flags']['C'] = new_flags
        elif choice == '2':
            new_flags = input(f"Enter C++ flags [{config['default_compiler_flags']['C++']}]: ").strip()
            if new_flags:
                config['default_compiler_flags']['C++'] = new_flags
        elif choice == '3':
            new_flags = input(f"Enter Java flags [{config['default_compiler_flags']['Java']}]: ").strip()
            if new_flags:
                config['default_compiler_flags']['Java'] = new_flags
        elif choice == '4':
            break
        else:
            print("Invalid choice!")
            time.sleep(1)

def print_header():
    """
    Print the program header with title and decorative formatting.
    
    Displays a formatted header for the Build System Generator application
    with centered title and decorative border lines for visual appeal.
    
    Returns:
        None
    
    Output:
        ============================================================
                           Build System Generator
        ============================================================
    
    Example:
        >>> print_header()  # Prints formatted header
    """
    print("=" * 60)
    print("Build System Generator".center(60))
    print("=" * 60)
    print()

def get_dir_name() -> str:
    """
    Get project directory name from user input with validation.
    
    Prompts the user to enter a directory name for the project, with the
    default taken from configuration settings. Validates that the name
    contains only alphanumeric characters and underscores.
    
    Returns:
        str: Valid directory name for the project
    
    Validation Rules:
        - Must contain only alphanumeric characters and underscores
        - Cannot be empty (default will be used)
        - Will be used as both directory name and default project name
    
    Example:
        >>> dir_name = get_dir_name()
        Enter directory for project [default: new_project]: my_project
        >>> print(dir_name)
        'my_project'
    """
    config = load_config()
    default_name = config['default_project_dir']
    while True:        
        print(f"\nEnter directory for project [default: {default_name}]: ", end='')
        print("\nThis will also be the default project name.")
        name = input().strip()
        if not name:
            return default_name
        if name.isalnum() or '_' in name:
            return name
        print("Invalid name! Use only alphanumeric characters and underscores.")

def get_target_name() -> str:
    """
    Get target executable name from user input with validation.
    
    Prompts the user to enter a target name for the executable/binary,
    with the current directory name as the default. Validates that the
    name contains only alphanumeric characters and underscores.
    
    Returns:
        str: Valid target name for the executable
    
    Validation Rules:
        - Must contain only alphanumeric characters and underscores
        - Cannot be empty (current directory name will be used)
        - Used as the final executable/binary name
    
    Example:
        >>> target_name = get_target_name()
        Enter target name [default: myproject]: calculator
        >>> print(target_name)
        'calculator'
    """
    default_name = os.path.basename(os.getcwd())
    while True:
        print(f"\nEnter target name [default: {default_name}]: ", end='')
        name = input().strip()
        if not name:
            return default_name
        if name.isalnum() or '_' in name:
            return name
        print("Invalid name! Use only alphanumeric characters and underscores.")

def get_target_architecture() -> str:
    """
    Get target architecture from user input with configuration defaults.
    
    Prompts the user to select target architecture (32-bit, 64-bit, or native)
    with the default value taken from configuration settings. The selection
    determines compiler flags added to the build system.
    
    Returns:
        str: Target architecture ('32', '64', or 'native')
    
    Architecture Options:
        - '32': 32-bit targeting (adds -m32 flag)
        - '64': 64-bit targeting (adds -m64 flag)  
        - 'native': Native targeting (no architecture flag)
    
    Example:
        >>> arch = get_target_architecture()
        Select target architecture:
        1. 64-bit (default)
        2. 32-bit
        3. Native
        Choice [1]: 2
        >>> print(arch)
        '32'
    """
    config = load_config()
    default_arch = config['default_architecture']
    
    arch_map = {'64': '1', '32': '2', 'native': '3'}
    default_choice = arch_map.get(default_arch, '1')
    
    print("\nSelect target architecture:")
    print(f"1. 64-bit {'(default)' if default_arch == '64' else ''}")
    print(f"2. 32-bit {'(default)' if default_arch == '32' else ''}")
    print(f"3. Native {'(default)' if default_arch == 'native' else ''}")
    
    while True:
        choice = input(f"\nChoice [{default_choice}]: ").strip()
        if not choice:
            return default_arch
        elif choice == '1':
            return '64'
        elif choice == '2':
            return '32'
        elif choice == '3':
            return 'native'
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


def get_source_files(lang: str) -> Tuple[List[str], List[str]]:
    """
    Discover and categorize source files for the specified language.
    
    Recursively searches the current directory for source files matching
    the specified language. Excludes files in build directories (obj/, build/)
    to avoid including generated or temporary files.
    
    Args:
        lang (str): Programming language ('C', 'C++', 'Java')
    
    Returns:
        Tuple[List[str], List[str]]: A tuple containing:
            - List of source files (.c, .cpp, .java)
            - List of header files (.h, .hpp) or empty list for Java
    
    File Extensions by Language:
        - C: .c (source), .h (headers)
        - C++: .cpp/.cc (source), .hpp/.h (headers)
        - Java: .java (source), no headers
    
    Example:
        >>> src_files, header_files = get_source_files('C++')
        >>> print(src_files)
        ['main.cpp', 'utils.cpp', 'src/helper.cc']
        >>> print(header_files)
        ['utils.hpp', 'include/helper.h']
    """
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

def generate_traditional_makefile(target_name: str, lang: str, arch: str = '64'):
    """
    Generate a traditional GNU Makefile for the specified language and architecture.
    
    Creates a comprehensive Makefile with automatic dependency tracking,
    proper compiler flags, and standard targets (all, clean, obj).
    Supports C, C++, and Java with architecture-specific optimizations.
    
    Args:
        target_name (str): Name of the target executable/jar
        lang (str): Programming language ('C', 'C++', 'Java')
        arch (str, optional): Target architecture ('32', '64', 'native'). Defaults to '64'.
    
    Returns:
        None: Creates Makefile in current directory
    
    Generated Makefile Features:
        - Automatic dependency generation
        - Architecture-specific compiler flags
        - Configurable compiler settings from config file
        - Standard targets: all, clean, obj/build
        - Incremental compilation support
        - Cross-platform compatibility
    
    Example:
        >>> generate_traditional_makefile('myapp', 'C++', '64')
        # Creates Makefile with G++ compiler, 64-bit targeting
    """
    config = load_config()
    
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
    arch_flag = ""
    if arch == '32':
        arch_flag = " -m32"
    elif arch == '64':
        arch_flag = " -m64"
    
    # Get compiler flags from config
    base_flags = config['default_compiler_flags'].get(lang, '-Wall -Wextra')
    
    makefile_content = """# Compiler settings
CC = {compiler}
CFLAGS = {base_flags} -I.{arch_flag}

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
""".format(compiler=compiler, src_ext=src_ext, target=target_name, arch_flag=arch_flag, base_flags=base_flags)

    with open('Makefile', 'w') as f:
        f.write(makefile_content)
    
    if not os.path.exists('obj'):
        os.makedirs('obj')

def generate_cmake(target_name: str, src_files: List[str], header_files: List[str], lang: str, arch: str = '64'):
    """
    Generate CMake configuration files for the specified language and architecture.
    
    Creates a modern CMakeLists.txt with proper target configuration,
    compiler flags, and installation rules. Supports C, C++, and Java
    with architecture-specific optimizations and modern CMake practices.
    
    Args:
        target_name (str): Name of the target executable/jar
        src_files (List[str]): List of source file paths
        header_files (List[str]): List of header file paths (unused for Java)
        lang (str): Programming language ('C', 'C++', 'Java')
        arch (str, optional): Target architecture ('32', '64', 'native'). Defaults to '64'.
    
    Returns:
        None: Creates CMakeLists.txt in current directory
    
    Generated CMake Features:
        - Modern CMake 3.10+ practices
        - Language-specific standards (C11, C++17)
        - Architecture-specific compiler flags
        - Configurable compiler settings from config file
        - Proper output directory organization
        - Installation rules for deployment
        - Java JAR creation support
    
    Example:
        >>> src_files = ['main.cpp', 'utils.cpp']
        >>> header_files = ['utils.h']
        >>> generate_cmake('myapp', src_files, header_files, 'C++', '64')
        # Creates CMakeLists.txt with modern C++17 configuration
    """
    config = load_config()
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
    arch_flags = ""
    if arch == '32':
        arch_flags = "\n# Set architecture to 32-bit\nset(CMAKE_C_FLAGS \"${CMAKE_C_FLAGS} -m32\")\nset(CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -m32\")"
    elif arch == '64':
        arch_flags = "\n# Set architecture to 64-bit\nset(CMAKE_C_FLAGS \"${CMAKE_C_FLAGS} -m64\")\nset(CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -m64\")"
    
    # Get compiler flags from config
    base_flags = config['default_compiler_flags'].get(lang, '-Wall -Wextra')
    cmake_flags = ' '.join([f'"{flag}"' for flag in base_flags.split()])
    
    cmake_content = """cmake_minimum_required(VERSION 3.10)

# Set project name and language
project({target} {lang})

# Set language standard
set(CMAKE_{lang_std})
set(CMAKE_{lang_std}_REQUIRED ON)

# Set compiler flags
add_compile_options({cmake_flags}){arch_flags}

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
""".format(target=target_name, lang=project_lang, lang_std=lang_std, sources=src_files_str, arch_flags=arch_flags, cmake_flags=cmake_flags)

    with open('CMakeLists.txt', 'w') as f:
        f.write(cmake_content)

def show_file_summary(src_files: List[str], header_files: List[str], lang: str):
    """
    Display a summary of discovered source and header files.
    
    Presents a formatted list of all source files and header files
    found in the project, organized by type. Provides file counts
    and waits for user acknowledgment before continuing.
    
    Args:
        src_files (List[str]): List of source file paths
        header_files (List[str]): List of header file paths
        lang (str): Programming language ('C', 'C++', 'Java')
    
    Returns:
        None: Displays information and waits for user input
    
    Display Format:
        - Source files with count
        - Header files with count (C/C++ only)
        - Individual file paths listed
    
    Example:
        >>> src_files = ['main.cpp', 'utils.cpp']
        >>> header_files = ['utils.h']
        >>> show_file_summary(src_files, header_files, 'C++')
        
        Source Files Found:
        ----------------------------------------
        Source Files (2):
          - main.cpp
          - utils.cpp
        
        Header Files (1):
          - utils.h
    """
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
    """
    Create a new project directory with sample source files and basic structure.
    
    Creates a project directory and populates it with language-appropriate
    sample files including main source file, headers (for C/C++), and README.
    Directory creation behavior is controlled by configuration settings.
    
    Args:
        dir_name (str): Name of the project directory to create
        lang (str): Programming language ('C', 'C++', 'Java')
    
    Returns:
        None: Creates directory and files, changes to new directory
    
    Created Files by Language:
        - C: main.c, main.h, README.md
        - C++: main.cpp, main.hpp, README.md
        - Java: {dir_name}.java, README.md
    
    Sample Content:
        - Working "Hello, World!" program
        - Proper headers and includes
        - Basic project README
    
    Example:
        >>> create_sample_files('calculator', 'C++')
        # Creates calculator/ directory with main.cpp, main.hpp, README.md
    """
    config = load_config()
    
    if config['auto_create_directories']:
        os.makedirs(dir_name, exist_ok=True)
        os.chdir(dir_name)
    else:
        if not os.path.exists(dir_name):
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

def show_success_message(build_type: str, target_name: str, lang: str):
    """
    Display success message with language and build-system specific instructions.
    
    Shows a comprehensive success message after build file generation,
    including the target name, language, and step-by-step build instructions
    tailored to the specific build system (Make/CMake) and language.
    
    Args:
        build_type (str): Type of build system ('make' or 'cmake')
        target_name (str): Name of the target executable/jar
        lang (str): Programming language ('C', 'C++', 'Java')
    
    Returns:
        None: Displays formatted success message and waits for user input
    
    Instruction Sets:
        - Make + C/C++: make, make clean commands
        - Make + Java: make, make run, make clean commands
        - CMake + C/C++: mkdir build, cmake, make sequence
        - CMake + Java: mkdir build, cmake, make, jar execution
    
    Example:
        >>> show_success_message('cmake', 'myapp', 'C++')
        Success! Build files generated successfully.
        Target name: myapp
        Language: C++
        
        To build with CMake:
        1. mkdir build
        2. cd build
        3. cmake ..
        4. make
    """
    print("\nSuccess! Build files generated successfully.")
    print(f"Target name: {target_name}")
    print(f"Language: {lang}")
    
    if build_type == 'cmake':
        print("\nTo build with CMake:")
        if lang == 'Java':
            print("1. mkdir build")
            print("2. cd build")
            print("3. cmake ..")
            print("4. make")
            print("5. java -jar {target_name}.jar".format(target_name=target_name))
        else:
            print("1. mkdir build")
            print("2. cd build")
            print("3. cmake ..")
            print("4. make")
    else:  # traditional makefile
        if lang == 'Java':
            print("\nTo build with Make:")
            print("1. make")
            print("\nTo run:")
            print("2. make run")
            print("\nTo clean:")
            print("make clean")
        else:
            print("\nTo build with Make:")
            print("1. make")
            print("\nTo clean (aka recompile with headers):")
            print("make clean")
    
    print("\nPress Enter to return to main menu...")
    input()

def main_menu():
    """
    Main application menu and control loop.
    
    Presents the primary user interface with menu options for all major
    functionality. Handles user input, validates choices, and coordinates
    between different subsystems (file discovery, build generation, 
    configuration management, project creation).
    
    Menu Options:
        1. Show source files summary - Display discovered files
        2. Generate traditional Makefile - Create GNU Makefile
        3. Generate CMake files - Create CMakeLists.txt
        4. Start new project - Create project template
        5. Configuration Management - Modify settings
        6. Exit - Quit the application
    
    Returns:
        None: Runs until user selects exit option
    
    Raises:
        KeyboardInterrupt: Handled gracefully with exit message
        SystemExit: Normal exit on user selection
    
    Example:
        >>> main_menu()  # Starts the interactive menu system
        ============================================================
                           Build System Generator
        ============================================================
        
        Main Menu:
        1. Show source files summary
        2. Generate traditional Makefile
        3. Generate CMake files
        4. Start new project
        5. Configuration Management
        6. Exit
    """
    while True:
        clear_screen()
        print_header()
        
        print("Main Menu:")
        print("1. Show source files summary")
        print("2. Generate traditional Makefile")
        print("3. Generate CMake files")
        print("4. Start new project")
        print("5. Configuration Management")
        print("6. Exit")
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
            arch = get_target_architecture()
            generate_traditional_makefile(target_name, lang, arch)
            show_success_message('make', target_name, lang)
        elif choice == '3':
            target_name = get_target_name()
            arch = get_target_architecture()
            generate_cmake(target_name, src_files, header_files, lang, arch)
            show_success_message('cmake', target_name, lang)
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
            manage_config()
        elif choice == '6':
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