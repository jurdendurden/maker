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
import re
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

def get_java_build_options() -> Dict[str, Any]:
    """
    Get advanced Java build options from user input.
    
    Prompts the user for Java-specific build configuration including
    main class, source directories, classpath, external JARs, and
    compiler options for enhanced Java project builds.
    
    Returns:
        Dict[str, Any]: Java build configuration containing:
            - main_class: Main class name for execution
            - source_dirs: List of source directories
            - classpath: Additional classpath entries
            - external_jars: List of external JAR dependencies
            - compiler_opts: Additional JavaC compiler options
            - create_jar: Whether to create JAR file
            - manifest_file: Custom manifest file path
    
    Example:
        >>> options = get_java_build_options()
        >>> print(options['main_class'])
        'com.example.MainApp'
    """
    print("\n" + "=" * 50)
    print("Advanced Java Build Configuration")
    print("=" * 50)
    
    options = {}
    
    # Main class
    main_class = input("Enter main class name [Main]: ").strip()
    options['main_class'] = main_class if main_class else 'Main'
    
    # Source directories
    print("\nSource directories (comma-separated, press Enter for 'src'):")
    src_input = input("Source dirs: ").strip()
    if src_input:
        options['source_dirs'] = [d.strip() for d in src_input.split(',')]
    else:
        options['source_dirs'] = ['src']
    
    # External JAR dependencies
    print("\nExternal JAR files (comma-separated, press Enter for none):")
    jar_input = input("JAR files: ").strip()
    if jar_input:
        options['external_jars'] = [j.strip() for j in jar_input.split(',')]
    else:
        options['external_jars'] = []
    
    # Additional classpath
    print("\nAdditional classpath entries (comma-separated, press Enter for none):")
    cp_input = input("Classpath: ").strip()
    if cp_input:
        options['classpath'] = [c.strip() for c in cp_input.split(',')]
    else:
        options['classpath'] = []
    
    # Compiler options
    print("\nAdditional JavaC options (press Enter for defaults):")
    print("Example: -Xlint:unchecked -deprecation")
    comp_input = input("Compiler options: ").strip()
    options['compiler_opts'] = comp_input if comp_input else ''
    
    # JAR creation
    create_jar = input("\nCreate JAR file? [y/N]: ").strip().lower()
    options['create_jar'] = create_jar in ['y', 'yes']
    
    # Manifest file
    if options['create_jar']:
        manifest_input = input("Custom manifest file path (press Enter for auto-generated): ").strip()
        options['manifest_file'] = manifest_input if manifest_input else None
    else:
        options['manifest_file'] = None
    
    return options

def generate_advanced_java_makefile(target_name: str, java_options: Dict[str, Any]):
    """
    Generate an advanced Java Makefile with comprehensive build features.
    
    Creates a sophisticated Makefile for Java projects with support for
    multiple source directories, external JAR dependencies, classpath
    management, JAR creation, and advanced compilation options.
    
    Args:
        target_name (str): Name of the target project/JAR
        java_options (Dict[str, Any]): Java build configuration options
    
    Returns:
        None: Creates advanced Makefile in current directory
    
    Generated Makefile Features:
        - Multiple source directory support
        - External JAR dependency management
        - Classpath construction and management
        - JAR file creation with manifest
        - Advanced JavaC compiler options
        - Package structure handling
        - Clean and rebuild targets
        - Run target with proper classpath
    
    Example:
        >>> java_opts = get_java_build_options()
        >>> generate_advanced_java_makefile('MyApp', java_opts)
        # Creates advanced Java Makefile with all features
    """
    config = load_config()
    
    # Build source directories list
    src_dirs = ' '.join(java_options['source_dirs'])
    
    # Build classpath
    classpath_parts = []
    if java_options['external_jars']:
        classpath_parts.extend(java_options['external_jars'])
    if java_options['classpath']:
        classpath_parts.extend(java_options['classpath'])
    
    classpath_str = ':'.join(classpath_parts) if classpath_parts else ''
    
    # Build compiler flags
    base_flags = config['default_compiler_flags'].get('Java', '-Xlint:all')
    compiler_flags = f"{base_flags} {java_options['compiler_opts']}".strip()
    
    makefile_content = f"""# Advanced Java Project Makefile
# Generated by Build System Generator

# Project settings
PROJECT_NAME = {target_name}
MAIN_CLASS = {java_options['main_class']}

# Compiler settings
JAVAC = javac
JAVA = java
JAR = jar

# Directories
SRC_DIRS = {src_dirs}
BUILD_DIR = build
CLASSES_DIR = $(BUILD_DIR)/classes
DIST_DIR = $(BUILD_DIR)/dist
LIB_DIR = lib

# Source files
SOURCES = $(shell find $(SRC_DIRS) -name "*.java" 2>/dev/null)
CLASSES = $(SOURCES:%.java=$(CLASSES_DIR)/%.class)

# Classpath configuration
EXTERNAL_JARS = {' '.join(java_options['external_jars']) if java_options['external_jars'] else ''}
ADDITIONAL_CP = {' '.join(java_options['classpath']) if java_options['classpath'] else ''}

# Build classpath
CP_PARTS = $(CLASSES_DIR)
ifneq ($(EXTERNAL_JARS),)
    CP_PARTS := $(CP_PARTS):$(shell echo "$(EXTERNAL_JARS)" | tr ' ' ':')
endif
ifneq ($(ADDITIONAL_CP),)
    CP_PARTS := $(CP_PARTS):$(shell echo "$(ADDITIONAL_CP)" | tr ' ' ':')
endif

# Compiler flags
JAVAC_FLAGS = {compiler_flags}

# Default target
all: compile{"" if not java_options['create_jar'] else " jar"}

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
{"jar: compile $(DIST_DIR)" if java_options['create_jar'] else "# JAR creation disabled"}"""

    if java_options['create_jar']:
        if java_options['manifest_file']:
            makefile_content += f"""
	$(JAR) cfm $(DIST_DIR)/$(PROJECT_NAME).jar {java_options['manifest_file']} -C $(CLASSES_DIR) ."""
        else:
            makefile_content += f"""
	echo "Main-Class: $(MAIN_CLASS)" > $(BUILD_DIR)/MANIFEST.MF
	$(JAR) cfm $(DIST_DIR)/$(PROJECT_NAME).jar $(BUILD_DIR)/MANIFEST.MF -C $(CLASSES_DIR) ."""

    makefile_content += f"""

# Run the application
run: compile
	$(JAVA) -cp "$(CP_PARTS)" $(MAIN_CLASS)

{"# Run JAR file" if java_options['create_jar'] else ""}
{"run-jar: jar" if java_options['create_jar'] else ""}
{"	$(JAVA) -jar $(DIST_DIR)/$(PROJECT_NAME).jar" if java_options['create_jar'] else ""}

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
	@echo "  all        - Compile the project{"" if not java_options['create_jar'] else " and create JAR"}"
	@echo "  compile    - Compile Java sources"
	{"@echo \"  jar        - Create JAR file\"" if java_options['create_jar'] else ""}
	@echo "  run        - Run the application"
	{"@echo \"  run-jar    - Run JAR file\"" if java_options['create_jar'] else ""}
	@echo "  clean      - Remove build artifacts"
	@echo "  rebuild    - Clean and rebuild"
	@echo "  info       - Show project information"
	@echo "  install-deps - Create lib directory for dependencies"
	@echo "  src-package - Package source code"
	@echo "  help       - Show this help message"

# Phony targets
.PHONY: all compile{"" if not java_options['create_jar'] else " jar"} run{"" if not java_options['create_jar'] else " run-jar"} clean rebuild info install-deps src-package help
"""

    with open('Makefile', 'w') as f:
        f.write(makefile_content)
    
    # Create build directory structure
    os.makedirs('build/classes', exist_ok=True)
    if java_options['create_jar']:
        os.makedirs('build/dist', exist_ok=True)
    
    # Create source directories if they don't exist
    for src_dir in java_options['source_dirs']:
        os.makedirs(src_dir, exist_ok=True)
    
    # Create lib directory for external JARs
    os.makedirs('lib', exist_ok=True)

# Database Schema Generation System
class DatabaseType:
    """Enumeration of supported database types for schema generation."""
    MYSQL = "mysql"
    MARIADB = "mariadb"
    # Future: POSTGRESQL = "postgresql", SQLITE = "sqlite", etc.

class DataType:
    """Represents a data type with language-specific mapping to SQL types."""
    def __init__(self, name: str, size: int = None, nullable: bool = True):
        self.name = name
        self.size = size
        self.nullable = nullable
    
    def __str__(self):
        return f"{self.name}{'(' + str(self.size) + ')' if self.size else ''}{'NULL' if self.nullable else 'NOT NULL'}"

class Field:
    """Represents a field/column in a database table."""
    def __init__(self, name: str, data_type: DataType, is_primary_key: bool = False, 
                 is_foreign_key: bool = False, foreign_table: str = None, 
                 default_value: str = None, comment: str = None):
        self.name = name
        self.data_type = data_type
        self.is_primary_key = is_primary_key
        self.is_foreign_key = is_foreign_key
        self.foreign_table = foreign_table
        self.default_value = default_value
        self.comment = comment

class Table:
    """Represents a database table with fields and metadata."""
    def __init__(self, name: str, fields: List[Field], comment: str = None):
        self.name = name
        self.fields = fields
        self.comment = comment

class CodeStructureParser:
    """Parser for extracting database schema information from code structures."""
    
    @staticmethod
    def parse_c_structs(file_path: str) -> List[Table]:
        """
        Parse C structures from header files to extract table definitions.
        
        Args:
            file_path (str): Path to the C header file
            
        Returns:
            List[Table]: List of table definitions extracted from structs
        """
        tables = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Simple regex to find struct definitions
            import re
            struct_pattern = r'typedef\s+struct\s*{([^}]+)}\s*(\w+);'
            
            for match in re.finditer(struct_pattern, content, re.DOTALL):
                struct_body = match.group(1).strip()
                struct_name = match.group(2)
                
                fields = []
                for line in struct_body.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//') and not line.startswith('/*'):
                        # Parse field definition
                        field = CodeStructureParser._parse_c_field(line)
                        if field:
                            fields.append(field)
                
                if fields:
                    tables.append(Table(struct_name.lower(), fields, f"Generated from C struct {struct_name}"))
                    
        except Exception as e:
            print(f"Error parsing C structs from {file_path}: {e}")
            
        return tables
    
    @staticmethod
    def _parse_c_field(line: str) -> Field:
        """Parse a single C struct field line."""
        import re
        
        # Remove semicolon and clean up
        line = line.rstrip(';').strip()
        
        # Basic field parsing (type name)
        parts = line.split()
        if len(parts) >= 2:
            c_type = parts[0]
            field_name = parts[1]
            
            # Map C types to SQL types
            sql_type = CodeStructureParser._map_c_type_to_sql(c_type)
            
            return Field(field_name, sql_type)
        
        return None
    
    @staticmethod
    def _map_c_type_to_sql(c_type: str) -> DataType:
        """Map C data types to SQL data types."""
        type_mapping = {
            'int': DataType('INT'),
            'long': DataType('BIGINT'),
            'short': DataType('SMALLINT'),
            'char': DataType('CHAR', 1),
            'float': DataType('FLOAT'),
            'double': DataType('DOUBLE'),
            'char*': DataType('VARCHAR', 255),
            'bool': DataType('BOOLEAN'),
            'unsigned int': DataType('INT UNSIGNED'),
            'unsigned long': DataType('BIGINT UNSIGNED'),
        }
        
        return type_mapping.get(c_type, DataType('TEXT'))
    
    @staticmethod
    def parse_cpp_classes(file_path: str) -> List[Table]:
        """
        Parse C++ classes from header files to extract table definitions.
        
        Args:
            file_path (str): Path to the C++ header file
            
        Returns:
            List[Table]: List of table definitions extracted from classes
        """
        tables = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            import re
            # Find class definitions
            class_pattern = r'class\s+(\w+)\s*{([^}]+)}'
            
            for match in re.finditer(class_pattern, content, re.DOTALL):
                class_name = match.group(1)
                class_body = match.group(2).strip()
                
                fields = []
                for line in class_body.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//') and not line.startswith('/*'):
                        # Look for member variables (skip methods)
                        if ';' in line and '(' not in line:
                            field = CodeStructureParser._parse_cpp_field(line)
                            if field:
                                fields.append(field)
                
                if fields:
                    tables.append(Table(class_name.lower(), fields, f"Generated from C++ class {class_name}"))
                    
        except Exception as e:
            print(f"Error parsing C++ classes from {file_path}: {e}")
            
        return tables
    
    @staticmethod
    def _parse_cpp_field(line: str) -> Field:
        """Parse a single C++ class member variable line."""
        import re
        
        # Remove access specifiers and clean up
        line = re.sub(r'(public|private|protected):', '', line)
        line = line.rstrip(';').strip()
        
        # Skip static, const, and other modifiers for now
        if 'static' in line or 'const' in line or '(' in line:
            return None
            
        parts = line.split()
        if len(parts) >= 2:
            cpp_type = parts[0]
            field_name = parts[1]
            
            # Map C++ types to SQL types
            sql_type = CodeStructureParser._map_cpp_type_to_sql(cpp_type)
            
            return Field(field_name, sql_type)
        
        return None
    
    @staticmethod
    def _map_cpp_type_to_sql(cpp_type: str) -> DataType:
        """Map C++ data types to SQL data types."""
        type_mapping = {
            'int': DataType('INT'),
            'long': DataType('BIGINT'),
            'short': DataType('SMALLINT'),
            'char': DataType('CHAR', 1),
            'float': DataType('FLOAT'),
            'double': DataType('DOUBLE'),
            'string': DataType('VARCHAR', 255),
            'std::string': DataType('VARCHAR', 255),
            'bool': DataType('BOOLEAN'),
            'unsigned': DataType('INT UNSIGNED'),
            'size_t': DataType('BIGINT UNSIGNED'),
        }
        
        return type_mapping.get(cpp_type, DataType('TEXT'))
    
    @staticmethod
    def parse_java_classes(file_path: str) -> List[Table]:
        """
        Parse Java classes to extract table definitions.
        
        Args:
            file_path (str): Path to the Java source file
            
        Returns:
            List[Table]: List of table definitions extracted from classes
        """
        tables = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            import re
            # Find class definitions
            class_pattern = r'public\s+class\s+(\w+)\s*{([^}]+)}'
            
            for match in re.finditer(class_pattern, content, re.DOTALL):
                class_name = match.group(1)
                class_body = match.group(2).strip()
                
                fields = []
                for line in class_body.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//') and not line.startswith('/*'):
                        # Look for field declarations
                        if ';' in line and '(' not in line and not line.startswith('public') and not line.startswith('private'):
                            field = CodeStructureParser._parse_java_field(line)
                            if field:
                                fields.append(field)
                
                if fields:
                    tables.append(Table(class_name.lower(), fields, f"Generated from Java class {class_name}"))
                    
        except Exception as e:
            print(f"Error parsing Java classes from {file_path}: {e}")
            
        return tables
    
    @staticmethod
    def _parse_java_field(line: str) -> Field:
        """Parse a single Java class field line."""
        import re
        
        # Remove modifiers and clean up
        line = re.sub(r'(public|private|protected|static|final)', '', line)
        line = line.rstrip(';').strip()
        
        parts = line.split()
        if len(parts) >= 2:
            java_type = parts[0]
            field_name = parts[1]
            
            # Map Java types to SQL types
            sql_type = CodeStructureParser._map_java_type_to_sql(java_type)
            
            return Field(field_name, sql_type)
        
        return None
    
    @staticmethod
    def _map_java_type_to_sql(java_type: str) -> DataType:
        """Map Java data types to SQL data types."""
        type_mapping = {
            'int': DataType('INT'),
            'Integer': DataType('INT'),
            'long': DataType('BIGINT'),
            'Long': DataType('BIGINT'),
            'short': DataType('SMALLINT'),
            'Short': DataType('SMALLINT'),
            'char': DataType('CHAR', 1),
            'Character': DataType('CHAR', 1),
            'float': DataType('FLOAT'),
            'Float': DataType('FLOAT'),
            'double': DataType('DOUBLE'),
            'Double': DataType('DOUBLE'),
            'String': DataType('VARCHAR', 255),
            'boolean': DataType('BOOLEAN'),
            'Boolean': DataType('BOOLEAN'),
            'byte': DataType('TINYINT'),
            'Byte': DataType('TINYINT'),
            'BigDecimal': DataType('DECIMAL', 10),
            'Date': DataType('DATE'),
            'Timestamp': DataType('TIMESTAMP'),
        }
        
        return type_mapping.get(java_type, DataType('TEXT'))

class SQLGenerator:
    """Generator for SQL DDL statements from table definitions."""
    
    @staticmethod
    def generate_mysql_schema(tables: List[Table], database_name: str = None) -> str:
        """
        Generate MySQL/MariaDB schema SQL from table definitions.
        
        Args:
            tables (List[Table]): List of table definitions
            database_name (str, optional): Name of the database
            
        Returns:
            str: Complete SQL DDL script
        """
        sql_lines = []
        
        # Database creation
        if database_name:
            sql_lines.append(f"-- Database: {database_name}")
            sql_lines.append(f"CREATE DATABASE IF NOT EXISTS `{database_name}`;")
            sql_lines.append(f"USE `{database_name}`;")
            sql_lines.append("")
        
        # Table creation
        for table in tables:
            sql_lines.append(f"-- Table: {table.name}")
            if table.comment:
                sql_lines.append(f"-- {table.comment}")
            
            sql_lines.append(f"CREATE TABLE IF NOT EXISTS `{table.name}` (")
            
            # Fields
            field_lines = []
            for field in table.fields:
                field_sql = SQLGenerator._generate_mysql_field(field)
                field_lines.append(f"    {field_sql}")
            
            # Primary keys
            primary_keys = [f.name for f in table.fields if f.is_primary_key]
            if primary_keys:
                field_lines.append(f"    PRIMARY KEY (`{'`, `'.join(primary_keys)}`)")
            
            # Foreign keys
            for field in table.fields:
                if field.is_foreign_key and field.foreign_table:
                    field_lines.append(f"    FOREIGN KEY (`{field.name}`) REFERENCES `{field.foreign_table}`(`{field.name}`)")
            
            sql_lines.append(",\n".join(field_lines))
            sql_lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
            sql_lines.append("")
        
        return "\n".join(sql_lines)
    
    @staticmethod
    def _generate_mysql_field(field: Field) -> str:
        """Generate MySQL field definition."""
        field_sql = f"`{field.name}` {field.data_type.name}"
        
        if field.data_type.size:
            field_sql += f"({field.data_type.size})"
        
        if not field.data_type.nullable:
            field_sql += " NOT NULL"
        
        if field.default_value:
            field_sql += f" DEFAULT {field.default_value}"
        
        if field.is_primary_key:
            field_sql += " AUTO_INCREMENT"
        
        if field.comment:
            field_sql += f" COMMENT '{field.comment}'"
        
        return field_sql

def get_database_options() -> Dict[str, Any]:
    """
    Get database schema generation options from user input.
    
    Returns:
        Dict[str, Any]: Database configuration options
    """
    print("\n" + "=" * 60)
    print("Database Schema Generation Configuration")
    print("=" * 60)
    
    options = {}
    
    # Database type
    print("\nSelect database type:")
    print("1. MySQL")
    print("2. MariaDB")
    
    while True:
        db_choice = input("Choice [1]: ").strip()
        if not db_choice or db_choice == '1':
            options['db_type'] = DatabaseType.MYSQL
            break
        elif db_choice == '2':
            options['db_type'] = DatabaseType.MARIADB
            break
        else:
            print("Invalid choice! Please enter 1 or 2.")
    
    # Database name
    db_name = input("Enter database name [myproject_db]: ").strip()
    options['database_name'] = db_name if db_name else 'myproject_db'
    
    # Language selection
    print("\nSelect source language:")
    print("1. C (parse structs from .h files)")
    print("2. C++ (parse classes from .hpp/.h files)")
    print("3. Java (parse classes from .java files)")
    
    while True:
        lang_choice = input("Choice [1]: ").strip()
        if not lang_choice or lang_choice == '1':
            options['language'] = 'C'
            break
        elif lang_choice == '2':
            options['language'] = 'C++'
            break
        elif lang_choice == '3':
            options['language'] = 'Java'
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")
    
    # Output file
    output_file = input("Enter output SQL file name [schema.sql]: ").strip()
    options['output_file'] = output_file if output_file else 'schema.sql'
    
    # Include sample data
    include_sample = input("Include sample INSERT statements? [y/N]: ").strip().lower()
    options['include_sample_data'] = include_sample in ['y', 'yes']
    
    return options

def generate_database_schema(options: Dict[str, Any]):
    """
    Generate database schema from code structures.
    
    Args:
        options (Dict[str, Any]): Database generation options
    """
    print(f"\nGenerating {options['db_type']} schema from {options['language']} code...")
    
    # Discover source files
    if options['language'] == 'C':
        source_files = glob.glob("**/*.h", recursive=True)
    elif options['language'] == 'C++':
        source_files = glob.glob("**/*.hpp", recursive=True) + glob.glob("**/*.h", recursive=True)
    else:  # Java
        source_files = glob.glob("**/*.java", recursive=True)
    
    # Filter out build directories
    source_files = [f for f in source_files if not f.startswith(('obj/', 'build/', 'target/'))]
    
    if not source_files:
        print(f"No {options['language']} source files found!")
        return
    
    print(f"Found {len(source_files)} source files to analyze...")
    
    # Parse structures/classes
    all_tables = []
    
    for file_path in source_files:
        print(f"Parsing {file_path}...")
        
        if options['language'] == 'C':
            tables = CodeStructureParser.parse_c_structs(file_path)
        elif options['language'] == 'C++':
            tables = CodeStructureParser.parse_cpp_classes(file_path)
        else:  # Java
            tables = CodeStructureParser.parse_java_classes(file_path)
        
        all_tables.extend(tables)
    
    if not all_tables:
        print("No structures/classes found to convert to database schema!")
        return
    
    print(f"Found {len(all_tables)} tables to generate:")
    for table in all_tables:
        print(f"  - {table.name} ({len(table.fields)} fields)")
    
    # Generate SQL
    sql_content = SQLGenerator.generate_mysql_schema(all_tables, options['database_name'])
    
    # Add sample data if requested
    if options['include_sample_data']:
        sql_content += "\n-- Sample INSERT statements\n"
        for table in all_tables:
            sample_values = []
            for field in table.fields:
                if field.data_type.name.upper() in ['INT', 'BIGINT', 'SMALLINT']:
                    sample_values.append('1')
                elif field.data_type.name.upper() in ['VARCHAR', 'TEXT', 'CHAR']:
                    sample_values.append(f"'sample_{field.name}'")
                elif field.data_type.name.upper() == 'BOOLEAN':
                    sample_values.append('TRUE')
                elif field.data_type.name.upper() in ['FLOAT', 'DOUBLE']:
                    sample_values.append('1.0')
                else:
                    sample_values.append('NULL')
            
            field_names = [f.name for f in table.fields]
            sql_content += f"INSERT INTO `{table.name}` (`{'`, `'.join(field_names)}`) VALUES ({', '.join(sample_values)});\n"
    
    # Write to file
    with open(options['output_file'], 'w') as f:
        f.write(sql_content)
    
    print(f"\nDatabase schema generated successfully!")
    print(f"Output file: {options['output_file']}")
    print(f"Database: {options['database_name']}")
    print(f"Tables: {len(all_tables)}")


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
        4. Generate advanced Java Makefile - Create enhanced Java Makefile
        5. Start new project - Create project template
        6. Configuration Management - Modify settings
        7. Generate database schema - Generate database schema from code
        8. Exit - Quit the application
    
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
        4. Generate advanced Java Makefile
        5. Start new project
        6. Configuration Management
        7. Generate database schema
        8. Exit
    """
    while True:
        clear_screen()
        print_header()
        
        print("Main Menu:")
        print("1. Show source files summary")
        print("2. Generate traditional Makefile")
        print("3. Generate CMake files")
        print("4. Generate advanced Java Makefile")
        print("5. Start new project")
        print("6. Configuration Management")
        print("7. Generate database schema")
        print("8. Exit")
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
        
        if choice == '4':
            # Advanced Java Makefile generation
            src_files, header_files = get_source_files('Java')
            
            if not src_files:
                print("\nError: No Java source files found in the current directory!")
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
            target_name = get_target_name()
            java_options = get_java_build_options()
            generate_advanced_java_makefile(target_name, java_options)
            show_success_message('make', target_name, 'Java')
        elif choice == '5':
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
        elif choice == '6':
            manage_config()
        elif choice == '7':
            options = get_database_options()
            generate_database_schema(options)
            print("\nPress Enter to return to main menu...")
            input()
        elif choice == '8':
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