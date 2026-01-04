# Python Setup with pip - Complete Guide

Composite GitHub Action for setting up Python environments with pip package manager, designed for projects using `pyproject.toml` for dependency management.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Inputs Reference](#inputs-reference)
- [Features](#features)
- [Usage Scenarios](#usage-scenarios)
- [Cache Configuration](#cache-configuration)
- [Dependency Groups](#dependency-groups)
- [Testing Guide](#testing-guide)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

This action wraps `actions/setup-python@v6` with additional functionality for managing pip-based Python projects. It provides:

- Automatic Python installation and configuration
- Optional dependency caching for faster CI runs
- Support for `pyproject.toml` optional dependency groups
- Automatic pip upgrade
- Cross-platform support (Linux, Windows, macOS)
- Architecture selection (x64, x86)

**Location**: `Serapieum-of-alex/github-actions/actions/python-setup/pip@v1`

## Quick Start

### Basic Usage (No Cache)

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
```

This sets up Python 3.12 (default) without caching. Suitable for projects without `pyproject.toml` or `requirements.txt`.

### With Caching

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
    with:
      cache: 'pip'
```

**Important**: Caching requires either `pyproject.toml` or `requirements.txt` in your repository root.

### With Optional Dependencies (Extras)

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
    with:
      install-groups: 'extras: dev test'
```

Installs your package with `pip install .[dev,test]`.

## Inputs Reference

| Input | Description | Required | Default | Valid Values |
|-------|-------------|----------|---------|--------------|
| `python-version` | Python version to install | No | `'3.12'` | Any valid Python version (e.g., `'3.10'`, `'3.11'`, `'3.12'`) |
| `cache` | Enable dependency caching | No | `''` (disabled) | `''`, `'pip'`, `'pipenv'`, `'poetry'` |
| `architecture` | Target CPU architecture | No | `'x64'` | `'x64'`, `'x86'` |
| `install-groups` | Dependency groups and/or optional dependencies to install | No | `''` (none) | Format: `'groups: name1 name2, extras: extra1 extra2'` |

### Input Details

#### `python-version`
Specifies which Python version to install. Supports:
- Major.minor versions: `'3.11'`, `'3.12'`, `'3.13'`
- Full versions: `'3.11.5'`
- Version ranges: `'3.x'`, `'>=3.11'`

#### `cache`
Controls dependency caching via `actions/setup-python@v6`:
- `''` (empty string, default): No caching. Use when no `pyproject.toml` or `requirements.txt` exists.
- `'pip'`: Cache pip dependencies from `pyproject.toml` or `requirements.txt`
- `'pipenv'`: Cache pipenv dependencies from `Pipfile.lock`
- `'poetry'`: Cache poetry dependencies from `poetry.lock`

**Cache Validation**: If `cache` is non-empty, the action validates that `pyproject.toml` or `requirements.txt` exists. If neither file is found, the action fails with a clear error message.

#### `architecture`
Selects CPU architecture (mainly relevant for Windows):
- `'x64'`: 64-bit Python (default, recommended)
- `'x86'`: 32-bit Python (legacy systems)

#### `install-groups`
Specifies dependency groups from `[dependency-groups]` and/or optional dependencies from `[project.optional-dependencies]` in `pyproject.toml`.

**Format**: `'groups: group1 group2, extras: extra1 extra2'`

**Examples**:
- Only dependency groups: `'groups: dev test'`
- Only optional dependencies: `'extras: aws viz'`
- Mixed: `'groups: dev test, extras: aws viz'`
- Legacy format (still works): `'dev test'` (interpreted as extras for backward compatibility)

**Behavior**:
- Optional dependencies (extras) use `pip install .[extra1,extra2]`
- Dependency groups use `pip install --dependency-groups group1,group2` (requires pip with PEP 735 support)
- If pip doesn't support `--dependency-groups`, a warning is shown and only extras are installed

If `install-groups` is empty and `pyproject.toml` exists, runs `pip install .` (installs only core dependencies).

## Features

### 1. Cache Validation

The action validates cache requirements **before** running `actions/setup-python@v6`:

```yaml
# This will FAIL with a clear error
- uses: ./actions/python-setup/pip
  with:
    cache: 'pip'  # No pyproject.toml or requirements.txt exists

# Error message:
# Cache is enabled (cache='pip') but no pyproject.toml or requirements.txt found.
# Either create a pyproject.toml/requirements.txt file or set cache: '' to disable caching.
```

### 2. Smart Dependency Installation

The action intelligently handles different scenarios:

| Scenario | `pyproject.toml` exists? | `install-groups` | Command Executed |
|----------|--------------------------|------------------|------------------|
| No file | No | Any | Skipped (message logged) |
| Basic install | Yes | Empty | `pip install .` |
| With groups | Yes | `'dev test'` | `pip install .[dev,test]` |

### 3. Automatic Pip Upgrade

Always runs `python -m pip install --upgrade pip` after Python setup to ensure the latest pip version.

### 4. Package Summary

Lists installed packages after installation for debugging:
```
pip list
```

### 5. Grouped Output

All actions are grouped in GitHub Actions logs for better readability:
- "Validating cache requirements"
- "Upgrading pip"
- "Installing dependencies"
- "Installed packages summary"

## Usage Scenarios

### Scenario 1: No Dependency Files (Development/Testing)

**Use Case**: Testing the action itself, or simple scripts without dependencies.

```yaml
- uses: actions/checkout@v5
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
# No cache needed, no pyproject.toml required
```

**What Happens**:
- Python installed
- Pip upgraded
- No dependencies installed (logs "No pyproject.toml found - skipping package installation")

### Scenario 2: Basic Project with pyproject.toml

**Use Case**: Standard Python package with core dependencies.

```yaml
# pyproject.toml
[project]
name = "my-package"
version = "1.0.0"
dependencies = ["requests", "numpy"]
```

```yaml
- uses: actions/checkout@v5
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'pip'
```

**What Happens**:
- Python installed with caching
- Pip upgraded
- `pip install .` executed (installs requests, numpy, and your package)

### Scenario 3: Development with Optional Dependencies

**Use Case**: Running tests and linters that require dev dependencies.

```yaml
# pyproject.toml
[project]
name = "my-package"
dependencies = ["requests"]

[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]
test = ["pytest-cov", "pytest-mock"]
docs = ["mkdocs", "mkdocs-material"]

[dependency-groups]
lint = ["ruff", "flake8"]
build = ["build", "twine"]
```

```yaml
- uses: actions/checkout@v5
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'pip'
    install-groups: 'extras: dev test'
```

**What Happens**:
- Python installed with caching
- `pip install .[dev,test]` executed
- Installs: requests (core), pytest, black, mypy (dev), pytest-cov, pytest-mock (test)

### Scenario 4: Matrix Testing Across Python Versions

**Use Case**: Testing compatibility with multiple Python versions.

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
    os: [ubuntu-latest, windows-latest, macos-latest]

steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
    with:
      python-version: ${{ matrix.python-version }}
      cache: 'pip'
```

**What Happens**:
- Tests run on 9 combinations (3 Python versions × 3 OS platforms)
- Each uses cached dependencies for faster runs

### Scenario 5: Using requirements.txt Instead

**Use Case**: Legacy project using `requirements.txt`.

```yaml
# requirements.txt
requests==2.31.0
numpy==1.26.0
```

```yaml
- uses: actions/checkout@v5
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'pip'
```

**What Happens**:
- Python installed with caching (validates `requirements.txt` exists)
- Pip upgraded
- No automatic installation (you must run `pip install -r requirements.txt` separately)

### Scenario 6: Windows 32-bit Architecture

**Use Case**: Supporting legacy Windows systems.

```yaml
- uses: actions/checkout@v5
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    architecture: 'x86'
    cache: 'pip'
```

### Scenario 7: Poetry/Pipenv Projects

**Use Case**: Using alternative package managers.

```yaml
- uses: actions/checkout@v5
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'poetry'  # or 'pipenv'

- name: Install with Poetry
  run: poetry install
```

## Cache Configuration

### When to Enable Cache

**Enable cache (`cache: 'pip'`) when:**
- You have `pyproject.toml` or `requirements.txt`
- Your dependencies don't change frequently
- You want faster CI runs (caching can save 30-60 seconds per run)

**Disable cache (`cache: ''`) when:**
- No `pyproject.toml` or `requirements.txt` exists
- Dependencies change on every commit
- Testing the action itself
- Debugging dependency issues

### Cache Validation Flow

```
User sets cache: 'pip'
    ↓
Action checks for pyproject.toml or requirements.txt
    ↓
Found? → Yes → Continue to setup-python (cache enabled)
       → No  → FAIL with error message
```

### Cache Example: Before and After

**Without Cache** (60-90 seconds):
```
Set up Python: 10s
Install dependencies: 50-80s
Total: 60-90s
```

**With Cache** (20-30 seconds):
```
Set up Python: 10s
Restore cache: 5s
Install dependencies: 5-15s (only new/changed packages)
Total: 20-30s
```

## Dependency Groups

### Optional Dependencies vs Dependency Groups

**Key Differences**:

1. **Optional Dependencies** (`[project.optional-dependencies]`):
   - Part of PEP 621 standard, widely supported
   - Published with your package on PyPI
   - Installed using `pip install package[extra]` syntax
   - Use prefix `extras:` in this action

2. **Dependency Groups** (`[dependency-groups]`):
   - Part of PEP 735 standard (newer, limited support)
   - Development-only, not published with package
   - Installed using `pip install --dependency-groups group` (requires recent pip)
   - Use prefix `groups:` in this action

**Note**: If your pip version doesn't support `--dependency-groups`, the action will show a warning and suggest using the uv action instead.

### Understanding Optional Dependencies

`pyproject.toml` supports optional dependency groups:

```toml
[project]
name = "myapp"
dependencies = ["requests"]  # Core dependencies (always installed)

[project.optional-dependencies]
dev = ["pytest", "black"]      # Development tools
test = ["pytest-cov"]          # Testing tools
docs = ["mkdocs"]              # Documentation tools
all = ["pytest", "black", "pytest-cov", "mkdocs"]  # Everything
```

### Installing Groups

| `install-groups` Value | Commands Generated | What Gets Installed |
|------------------------|-------------------|---------------------|
| `''` (empty) | `pip install .` | Core dependencies only |
| `'extras: dev'` | `pip install .[dev]` | Core + dev extras |
| `'extras: dev test'` | `pip install .[dev,test]` | Core + dev + test extras |
| `'groups: lint'` | `pip install .` then `pip install --dependency-groups lint` | Core + lint group (if supported) |
| `'groups: lint build, extras: dev'` | `pip install .[dev]` then `pip install --dependency-groups lint,build` | Core + dev extras + lint/build groups |

### Common Patterns

**Test Workflow**:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    install-groups: 'extras: test'
- run: pytest
```

**Lint Workflow**:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    install-groups: 'extras: dev'
- run: black --check .
- run: mypy src/
```

**Documentation Workflow**:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    install-groups: 'extras: docs'
- run: mkdocs build
```

## Testing Guide

This action is tested across multiple scenarios. Reference the test workflow at `.github/workflows/test-actions.yml`.

### Test Coverage

| Test Job | Purpose | Key Validations |
|----------|---------|-----------------|
| `test-pip-basic` | Default behavior without cache | Python installed, no cache validation |
| `test-pip-with-groups` | Dependency groups installation | Multiple groups installed correctly |
| `test-pip-matrix` | Cross-platform compatibility | Works on Linux/Windows/macOS with Python 3.10/3.11/3.12 |
| `test-pip-cache` | Cache functionality | Dependencies cached and restored |
| `test-pip-cache-validation-error` | Cache validation error handling | Fails gracefully when cache enabled without files |
| `test-pip-cache-with-requirements` | requirements.txt support | Cache validation passes with requirements.txt |
| `test-pip-no-dependency-file` | No dependency files | Works without pyproject.toml/requirements.txt when cache disabled |
| `test-pip-architecture` | Architecture selection | x64 and x86 work correctly on Windows |

### Running Tests Locally

Use `act` to test locally:

```bash
# Install act (if needed)
# Windows: choco install act-cli

# Run all tests
act -j test-pip-basic
act -j test-pip-with-groups
act -j test-pip-matrix
```

### Testing in Your Own Workflow

```yaml
# .github/workflows/test-pip-action.yml
name: Test pip action

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@main
        with:
          cache: 'pip'
          install-groups: 'dev test'
      - run: pytest
```

## Troubleshooting

### Error: "No file matched to [**/requirements.txt or **/pyproject.toml]"

**Cause**: `cache: 'pip'` is enabled but no `pyproject.toml` or `requirements.txt` exists.

**Solution**:
```yaml
# Option 1: Disable cache
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: ''  # Explicitly disable

# Option 2: Create pyproject.toml
- name: Create pyproject.toml
  run: |
    cat > pyproject.toml << 'EOF'
    [project]
    name = "myproject"
    version = "0.1.0"
    EOF

- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'pip'
```

### Error: "Invalid requirement: '.[dev][test]'"

**Cause**: This was a bug in earlier versions (now fixed). Multiple groups were generating `.[dev][test]` instead of `.[dev,test]`.

**Solution**: Use the latest version of the action (`@v1` or later).

### Error: "UnicodeEncodeError: 'charmap' codec can't encode character"

**Cause**: Windows default encoding (cp1252) doesn't support Unicode characters in Python print statements.

**Solution**: Use `shell: bash` and avoid Unicode characters:
```yaml
- name: Test
  shell: bash
  run: python -c "print('[OK] Test passed')"  # Not: print('✓ Test passed')
```

### Dependencies Not Installing

**Symptoms**: Action succeeds but packages are missing.

**Debug Steps**:

1. Check if `pyproject.toml` exists:
```yaml
- run: ls -la
- run: cat pyproject.toml
```

2. Verify action output in logs (look for "Installing dependencies" group):
```
Found pyproject.toml, installing package...
Installing with dependency groups: dev test
Running: pip install .[dev,test]
```

3. Check installed packages:
```yaml
- run: pip list
- run: pip show pytest  # Check specific package
```

### Cache Not Working

**Symptoms**: Dependencies reinstall on every run.

**Debug Steps**:

1. Verify cache is enabled:
```yaml
with:
  cache: 'pip'  # Must be explicitly set
```

2. Check cache hit in logs:
```
Cache restored from key: ...
```

3. Ensure dependencies file hasn't changed (cache key is based on file hash).

## Best Practices

### 1. Use Cache for Stable Dependencies

```yaml
# Good: Stable project with versioned dependencies
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'pip'
```

### 2. Pin Dependency Versions in pyproject.toml

```toml
# Good: Specific versions for reproducible builds
dependencies = [
  "requests==2.31.0",
  "numpy>=1.26.0,<2.0.0"
]

# Avoid: Unpinned versions can break builds
dependencies = ["requests", "numpy"]
```

### 3. Separate Dependency Groups by Purpose

```toml
[project.optional-dependencies]
# Good: Logical separation
dev = ["black", "mypy", "ruff"]
test = ["pytest", "pytest-cov", "pytest-mock"]
docs = ["mkdocs", "mkdocs-material"]

# Avoid: Single group for everything
dev = ["black", "mypy", "pytest", "mkdocs"]
```

### 4. Use Matrix Testing for Library Projects

```yaml
# Libraries should test against multiple Python versions
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']

steps:
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
    with:
      python-version: ${{ matrix.python-version }}
```

### 5. Disable Cache for Dynamic Dependencies

```yaml
# If dependencies change frequently (e.g., from git branches)
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  # No cache parameter (defaults to '')
```

### 6. Use Specific Action Versions

```yaml
# Good: Pin to major version (gets bug fixes)
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1

# Acceptable: Pin to exact commit (maximum stability)
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@abc1234

# Avoid: Using @main (unpredictable)
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@main
```

### 7. Combine with Other Actions

```yaml
- uses: actions/checkout@v5
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'pip'
    install-groups: 'test'

- name: Run tests with coverage
  run: pytest --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v4
```

## Comparison with Other Actions

| Feature | This Action | actions/setup-python | astral-sh/setup-uv |
|---------|-------------|---------------------|-------------------|
| Python Installation | ✓ | ✓ | ✓ |
| Pip Caching | ✓ | ✓ | ✗ |
| Auto Pip Upgrade | ✓ | ✗ | N/A |
| Dependency Groups | ✓ | ✗ | ✓ |
| Cache Validation | ✓ | ✗ | ✗ |
| pyproject.toml Auto-install | ✓ | ✗ | ✓ |
| Package Summary | ✓ | ✗ | ✗ |
| Cross-platform | ✓ | ✓ | ✓ |

**When to use this action:**
- Standard pip-based projects
- Need dependency groups with pip
- Want automatic validation and error messages
- Need clear GitHub Actions log output

**When to use alternatives:**
- `actions/setup-python` alone: Minimal setup, no extras needed
- `astral-sh/setup-uv`: Modern projects wanting faster dependency resolution

## Migration Guide

### From actions/setup-python

**Before**:
```yaml
- uses: actions/setup-python@v6
  with:
    python-version: '3.12'
    cache: 'pip'
- run: pip install .
- run: pip install .[dev,test]
```

**After**:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    python-version: '3.12'
    cache: 'pip'
    install-groups: 'dev test'
```

### From Manual Pip Commands

**Before**:
```yaml
- uses: actions/setup-python@v6
- run: python -m pip install --upgrade pip
- run: |
    if [ -f pyproject.toml ]; then
      pip install .[dev,test]
    fi
```

**After**:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    cache: 'pip'
    install-groups: 'dev test'
```

## Additional Resources

- [GitHub Actions: actions/setup-python](https://github.com/actions/setup-python)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 621: pyproject.toml metadata](https://peps.python.org/pep-0621/)
- [pip documentation](https://pip.pypa.io/)

## Support

For issues, questions, or contributions:
- Repository: https://github.com/Serapieum-of-alex/github-actions
- Issues: https://github.com/Serapieum-of-alex/github-actions/issues
