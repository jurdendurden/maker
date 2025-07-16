# Build System Generator

A powerful Python tool for generating build systems (Makefiles and CMake files) for C, C++, and Java projects. This tool simplifies the process of setting up build environments with customizable configurations, architecture targeting, and project templates.

## Features

### 🚀 **Core Functionality**
- **Multi-language support**: Generate build files for C, C++, and Java projects
- **Dual build systems**: Support for both traditional Makefiles and CMake
- **Advanced Java support**: Enterprise-grade Java Makefiles with dependency management
- **Architecture targeting**: 32-bit, 64-bit, or native compilation support
- **Project templates**: Create new projects with sample files and structure
- **Source file discovery**: Automatically finds and organizes source files

### ⚙️ **Configuration Management**
- **Persistent settings**: Save preferences in `maker_config.json`
- **Customizable compiler flags**: Set default flags for each language
- **Default preferences**: Configure default architecture, project names, and build systems
- **Environment customization**: Flexible development environment setup

### 🎯 **Smart Build Generation**
- **Automatic dependency tracking**: Generates proper dependency rules
- **Clean build support**: Includes clean targets for easy rebuilds
- **Organized output**: Separate object files and build directories
- **Cross-platform compatibility**: Works on Windows, Linux, and macOS

### ☕ **Advanced Java Features**
- **Multiple source directories**: Support for complex project structures
- **External JAR management**: Automatic classpath construction with dependencies
- **JAR file creation**: Built-in support for creating executable JAR files
- **Custom manifest support**: Use custom manifest files or auto-generate
- **Package structure handling**: Proper handling of Java package hierarchies
- **Advanced compiler options**: Configurable JavaC flags and optimizations
- **Dependency installation**: Integrated dependency management workflow

## Installation

### Prerequisites
- Python 3.6 or higher
- GCC/G++ compiler (for C/C++ projects)
- Java Development Kit (for Java projects)
- CMake (optional, for CMake build system)

### Setup
1. Clone or download the repository
2. Make the script executable (Linux/macOS):
   ```bash
   chmod +x maker.py
   ```
3. Run the tool:
   ```bash
   python maker.py
   ```

## Usage

### Quick Start
1. Navigate to your project directory
2. Run `python maker.py`
3. Choose from the main menu options

### Main Menu Options

#### 1. Show Source Files Summary
- Displays all discovered source files
- Shows file count and organization
- Helps verify project structure before build generation

#### 2. Generate Traditional Makefile
- Creates a traditional GNU Makefile
- Supports automatic dependency generation
- Includes standard targets: `all`, `clean`, `obj`

#### 3. Generate CMake Files
- Creates CMakeLists.txt for CMake build system
- Modern CMake practices with proper target configuration
- Cross-platform build support

#### 4. Generate Advanced Java Makefile
- Creates sophisticated Java Makefiles with enterprise features
- Multiple source directory support
- External JAR dependency management
- Classpath construction and management
- JAR file creation with custom manifest support
- Package structure handling and advanced compiler options

#### 5. Start New Project
- Creates a new project directory
- Generates sample source files
- Includes basic project structure and README

#### 6. Configuration Management
- Persistent configuration settings
- Customizable compiler flags
- Default preferences setup

## Configuration

The tool uses `maker_config.json` for persistent settings:

```json
{
  "default_architecture": "64",
  "default_compiler_flags": {
    "C": "-Wall -Wextra -O2",
    "C++": "-Wall -Wextra -O2 -std=c++17",
    "Java": "-Xlint:all"
  },
  "default_project_dir": "new_project",
  "preferred_build_system": "make",
  "auto_create_directories": true
}
```

### Configuration Options

| Setting | Description | Options |
|---------|-------------|---------|
| `default_architecture` | Target architecture | `"32"`, `"64"`, `"native"` |
| `default_compiler_flags` | Language-specific flags | Custom flag strings |
| `default_project_dir` | Default project directory name | Any valid directory name |
| `preferred_build_system` | Preferred build system | `"make"`, `"cmake"` |
| `auto_create_directories` | Automatic directory creation | `true`, `false` |

## Examples

### Generated Makefile (C Project)
```makefile
# Compiler settings
CC = gcc
CFLAGS = -Wall -Wextra -O2 -I. -m64

# Get all source files
SRC = $(wildcard *.c)
OBJ = $(patsubst %.c,obj/%.o,$(SRC))

# Main target
TARGET = myproject

# Default rule
all: obj $(TARGET)

# Create obj directory
obj:
	mkdir -p obj

# Link rule
$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET)

# Compile rule
obj/%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean rule
clean:
	rm -rf obj $(TARGET)
```

### Generated CMakeLists.txt (C++ Project)
```cmake
cmake_minimum_required(VERSION 3.10)

# Set project name and language
project(myproject CXX)

# Set language standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set compiler flags
add_compile_options("-Wall" "-Wextra" "-O2" "-std=c++17")

# Set architecture to 64-bit
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -m64")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m64")

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Create executable target
add_executable(${PROJECT_NAME} main.cpp)

# Add include directories
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Install rules
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)
```

### Generated Advanced Java Makefile
```makefile
# Advanced Java Project Makefile
# Generated by Build System Generator

# Project settings
PROJECT_NAME = MyJavaApp
MAIN_CLASS = com.example.MainApp

# Compiler settings
JAVAC = javac
JAVA = java
JAR = jar

# Directories
SRC_DIRS = src test/src
BUILD_DIR = build
CLASSES_DIR = $(BUILD_DIR)/classes
DIST_DIR = $(BUILD_DIR)/dist
LIB_DIR = lib

# Source files
SOURCES = $(shell find $(SRC_DIRS) -name "*.java" 2>/dev/null)
CLASSES = $(SOURCES:%.java=$(CLASSES_DIR)/%.class)

# Classpath configuration
EXTERNAL_JARS = lib/junit-4.13.2.jar lib/commons-lang3-3.12.0.jar
ADDITIONAL_CP = config resources

# Build classpath
CP_PARTS = $(CLASSES_DIR)
ifneq ($(EXTERNAL_JARS),)
    CP_PARTS := $(CP_PARTS):$(shell echo "$(EXTERNAL_JARS)" | tr ' ' ':')
endif
ifneq ($(ADDITIONAL_CP),)
    CP_PARTS := $(CP_PARTS):$(shell echo "$(ADDITIONAL_CP)" | tr ' ' ':')
endif

# Compiler flags
JAVAC_FLAGS = -Xlint:all -deprecation -Werror

# Default target
all: compile jar

# Create necessary directories
$(CLASSES_DIR):
	mkdir -p $(CLASSES_DIR)

$(DIST_DIR):
	mkdir -p $(DIST_DIR)

# Compile Java sources
compile: $(CLASSES_DIR) $(CLASSES)

# Pattern rule for compiling Java files
$(CLASSES_DIR)/%.class: %.java
	$(JAVAC) $(JAVAC_FLAGS) -cp "$(CP_PARTS)" -d $(CLASSES_DIR) $<

# Create JAR file
jar: compile $(DIST_DIR)
	echo "Main-Class: $(MAIN_CLASS)" > $(BUILD_DIR)/MANIFEST.MF
	$(JAR) cfm $(DIST_DIR)/$(PROJECT_NAME).jar $(BUILD_DIR)/MANIFEST.MF -C $(CLASSES_DIR) .

# Run the application
run: compile
	$(JAVA) -cp "$(CP_PARTS)" $(MAIN_CLASS)

# Run JAR file
run-jar: jar
	$(JAVA) -jar $(DIST_DIR)/$(PROJECT_NAME).jar

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)

# Clean and rebuild
rebuild: clean all

# Show project info
info:
	@echo "Project: $(PROJECT_NAME)"
	@echo "Main Class: $(MAIN_CLASS)"
	@echo "Source Dirs: $(SRC_DIRS)"
	@echo "Build Dir: $(BUILD_DIR)"
	@echo "Classpath: $(CP_PARTS)"
	@echo "Sources Found: $(words $(SOURCES))"

# Install dependencies (create lib directory)
install-deps:
	mkdir -p $(LIB_DIR)
	@echo "Place external JAR files in $(LIB_DIR)/ directory"

# Package source code
src-package:
	tar -czf $(DIST_DIR)/$(PROJECT_NAME)-src.tar.gz $(SRC_DIRS) Makefile README.md

# Help target
help:
	@echo "Available targets:"
	@echo "  all        - Compile the project and create JAR"
	@echo "  compile    - Compile Java sources"
	@echo "  jar        - Create JAR file"
	@echo "  run        - Run the application"
	@echo "  run-jar    - Run JAR file"
	@echo "  clean      - Remove build artifacts"
	@echo "  rebuild    - Clean and rebuild"
	@echo "  info       - Show project information"
	@echo "  install-deps - Create lib directory for dependencies"
	@echo "  src-package - Package source code"
	@echo "  help       - Show this help message"

# Phony targets
.PHONY: all compile jar run run-jar clean rebuild info install-deps src-package help
```

## Build Instructions

### Using Generated Makefile
```bash
# Build the project
make

# Clean build files
make clean

# Force rebuild
make clean && make
```

### Using Generated CMake Files
```bash
# Create build directory
mkdir build
cd build

# Generate build files
cmake ..

# Build the project
make

# For Java projects
java -jar projectname.jar
```

### Using Advanced Java Makefile
```bash
# Compile and create JAR
make all

# Compile only
make compile

# Create JAR file
make jar

# Run application directly
make run

# Run JAR file
make run-jar

# View project information
make info

# Install dependencies
make install-deps

# Package source code
make src-package

# Show all available targets
make help

# Clean and rebuild
make rebuild
```

## Project Structure

```
project/
├── src/                    # Source files (.c, .cpp, .java)
├── test/src/              # Test source files (Java projects)
├── include/               # Header files (.h, .hpp)
├── lib/                   # External JAR files (Java projects)
├── obj/                   # Object files (created by build)
├── build/                 # Build directory
│   ├── classes/           # Compiled Java classes
│   └── dist/              # Distribution files (JARs)
├── Makefile               # Generated Makefile
├── CMakeLists.txt         # Generated CMake file
├── maker_config.json      # Configuration file
└── README.md              # Project documentation
```

## Language Support

### C Projects
- **Extensions**: `.c`, `.h`
- **Compiler**: GCC
- **Features**: Automatic header dependency tracking
- **Standards**: C11 default

### C++ Projects
- **Extensions**: `.cpp`, `.cc`, `.hpp`, `.h`
- **Compiler**: G++
- **Features**: Modern C++ standards support
- **Standards**: C++17 default

### Java Projects
- **Extensions**: `.java`
- **Compiler**: JavaC
- **Features**: Enterprise-grade build system with advanced features
- **Standards**: Modern Java practices

#### Advanced Java Features
- **Multiple source directories**: Support for `src/`, `test/src/`, etc.
- **External JAR management**: Automatic classpath with `lib/` directory
- **Package structure**: Proper handling of Java package hierarchies
- **JAR creation**: Executable JAR files with custom manifests
- **Dependency management**: Integrated workflow for external dependencies
- **Advanced compiler options**: Configurable JavaC flags and optimizations

## Advanced Features

### Architecture Targeting
- **32-bit**: Adds `-m32` compiler flag
- **64-bit**: Adds `-m64` compiler flag
- **Native**: Lets compiler choose optimal architecture

### Dependency Management
- Automatic header dependency generation (C/C++)
- External JAR dependency management (Java)
- Incremental compilation support
- Clean rebuild capabilities

### Cross-Platform Support
- Windows PowerShell compatibility
- Linux/macOS bash compatibility
- Portable file path handling

## Troubleshooting

### Common Issues

**No source files found**
- Ensure you're in the correct directory
- Check file extensions match language selection
- Verify files aren't in excluded directories (`obj/`, `build/`)

**Build errors**
- Check compiler installation
- Verify architecture compatibility
- Review compiler flags in configuration

**Permission errors**
- Ensure write permissions in project directory
- Check executable permissions on generated files

**Java-specific issues**
- Verify JAVA_HOME environment variable
- Check external JAR files exist in `lib/` directory
- Ensure main class is correctly specified
- Verify package structure matches directory structure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## License

This project is open source. See the LICENSE file for details.

## Changelog

### Version 2.1
- Added advanced Java makefile generation
- Enhanced Java project support with enterprise features
- Multiple source directory support
- External JAR dependency management
- JAR creation with custom manifest support
- Added comprehensive help system for Java builds

### Version 2.0
- Added architecture targeting (32/64-bit)
- Implemented configuration management system
- Enhanced build system generation
- Improved user interface and workflow

### Version 1.0
- Initial release
- Basic Makefile and CMake generation
- Multi-language support
- Project template creation