# Plan to Fix Nuitka Installer Builder

## 1. Data Files Handling Update

New approach options:
- Single files: `--include-data-files=/path/to/file/*.txt=folder_name/some.txt`
- Directory contents: `--include-data-files=/path/to/files/*.txt=folder_name/`
- Recursive directory: `--include-data-files=/path/to/scan=folder_name/=**/*.txt`
- Package data: `--include-package-data=package_name=*.txt`

## 2. Package Handling Improvements

Multiple levels of package inclusion:
- Whole package with all subpackages: `--include-package=package_name`
- Single modules: `--include-module=package_name.module`
- Package data files: `--include-package-data=package_name`
- Package DLLs tracking: `--list-package-dlls=package_name`

## 3. New Features to Add

- Distribution metadata support: `--include-distribution-metadata=DISTRIBUTION`
- Better deployment controls: `--deployment`
- Package configuration: `--user-package-configuration-file=YAML_FILENAME`
- Progress reporting: `--report=REPORT_FILENAME`

## 4. Structure Changes

```python
@define
class InstallerBuilder:
    # Add new fields:
    distribution_metadata: list = field(default=Factory(list))
    package_configs: list = field(default=Factory(list))
    enable_deployment: bool = field(default=True)
    report_file: str = field(default='')
```

## 5. Implementation Plan

### a) Create new data file formatter
```python
def format_data_files(items):
    """
    Handle multiple data file scenarios:
    - Single files
    - Directory contents
    - Recursive directories
    - Package data
    """
```

### b) Create package handler
```python
def handle_package_inclusion(package_name):
    """
    Determine best way to include a package:
    - Check if it's a single module or package
    - Handle data files
    - Handle dependencies
    - Handle metadata if needed
    """
```

### c) Update main compilation method
```python
def compile_distribution(self):
    """
    Enhanced compilation with:
    - Better package handling
    - Progress reporting
    - Deployment controls
    - Configuration file support
    """
```

## 6. Testing Framework

- Test different package inclusion scenarios
- Test data file handling
- Test cross-platform compatibility
- Test deployment scenarios

## 7. Documentation Updates

- Document new package handling capabilities
- Document data file handling options
- Document deployment best practices
- Add examples for common scenarios

## Implementation Order

1. Data file formatter
2. Package handler
3. Compilation method updates
4. Testing framework
5. Documentation

## Dependencies

Required Nuitka version: Latest
Required Python version: 3.7+
