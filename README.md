# Build System Generator

A powerful Python tool for generating build systems (Makefiles and CMake files) for C, C++, and Java projects. This tool simplifies the process of setting up build environments with customizable configurations, architecture targeting, and project templates.

## Features

### 🚀 **Core Functionality**
- **Multi-language support**: Generate build files for C, C++, and Java projects
- **Dual build systems**: Support for both traditional Makefiles and CMake
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

#### 4. Start New Project
- Creates a new project directory
- Generates sample source files
- Includes basic project structure and README

#### 5. Configuration Management
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

## Project Structure

```
project/
├── src/                    # Source files (.c, .cpp, .java)
├── include/               # Header files (.h, .hpp)
├── obj/                   # Object files (created by build)
├── build/                 # CMake build directory
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
- **Features**: Classpath management, JAR creation
- **Standards**: Modern Java practices

## Advanced Features

### Architecture Targeting
- **32-bit**: Adds `-m32` compiler flag
- **64-bit**: Adds `-m64` compiler flag
- **Native**: Lets compiler choose optimal architecture

### Dependency Management
- Automatic header dependency generation
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## License

This project is open source. See the LICENSE file for details.

## Changelog

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
