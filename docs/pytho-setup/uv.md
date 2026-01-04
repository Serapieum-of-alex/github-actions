# Python Setup with uv - Complete Guide

Composite GitHub Action for setting up Python environments with the uv package manager, designed for modern Python projects using `pyproject.toml` and dependency groups.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Inputs Reference](#inputs-reference)
- [Features](#features)
- [Usage Scenarios](#usage-scenarios)
- [Dependency Groups](#dependency-groups)
- [Lock File Verification](#lock-file-verification)
- [Virtual Environment](#virtual-environment)
- [Testing Guide](#testing-guide)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

This action provides a complete Python environment setup using [uv](https://github.com/astral-sh/uv), the fast Python package installer and resolver. It automatically:

- Installs Python and uv
- Verifies lock file integrity (optional)
- Installs dependencies with group support
- Activates the virtual environment automatically
- Caches dependencies for faster CI runs

**Location**: `Serapieum-of-alex/github-actions/actions/python-setup/uv@v1`

## Quick Start

### Basic Usage (Core Dependencies Only)

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1

  # Virtual environment is automatically activated!
  - run: python --version
  - run: pytest
```

### With Dependency Groups

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      install-groups: 'dev test'

  - run: pytest
  - run: black --check .
```

## Inputs Reference

| Input | Description | Required | Default | Valid Values |
|-------|-------------|----------|---------|--------------|
| `python-version` | Python version to install | No | `'3.12'` | Any valid Python version (e.g., `'3.10'`, `'3.11'`, `'3.12'`) |
| `install-groups` | Dependency groups to install | No | `''` (core only) | Space or comma-separated list (e.g., `'dev'`, `'dev test'`, `'dev,test,docs'`) |
| `verify-lock` | Verify lock file is up to date | No | `'true'` | `'true'`, `'false'` |

### Input Details

#### `python-version`
Specifies which Python version to install via `actions/setup-python@v6`.

**Examples:**
```yaml
python-version: '3.10'  # Python 3.10
python-version: '3.11'  # Python 3.11
python-version: '3.12'  # Python 3.12 (default)
```

#### `install-groups`
Specifies which dependency groups from `[dependency-groups]` in `pyproject.toml` to install.

**Default behavior (`''`)**: Installs only core dependencies (those listed in `dependencies`), no optional groups.

**When specified**: Installs core dependencies + only the specified groups (all other groups are excluded).

**Formats supported:**
- Space-separated: `'dev test'`
- Comma-separated: `'dev,test,docs'`
- Mixed: `'dev, test docs'`

**Important**: The action uses `uv sync --no-default-groups --group <name>` to ensure ONLY the specified groups are installed, preventing unwanted transitive group installations.

#### `verify-lock`
Controls whether to verify the `uv.lock` file is up to date before installation.

**When `'true'` (default)**: Runs `uv lock --check` and fails if lock file is outdated.

**When `'false'`: Skips lock file verification.

## Features

### 1. Automatic Virtual Environment Activation

The action automatically activates the `.venv` virtual environment by:
- Adding `.venv/bin` (Linux/macOS) or `.venv/Scripts` (Windows) to `$GITHUB_PATH`
- Setting `$VIRTUAL_ENV` environment variable

**Result**: All subsequent steps can use `python`, `pytest`, `black`, etc. directly without manual activation or `uv run`.

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    install-groups: 'dev test'

# No activation needed!
- run: python --version  # Uses venv Python
- run: pytest            # Uses venv pytest
- run: black .           # Uses venv black
```

### 2. Smart Dependency Group Management

The action uses `--no-default-groups` flag to ensure clean group isolation:

```yaml
# pyproject.toml
[project]
dependencies = ["requests"]

[dependency-groups]
dev = ["httpx"]
test = ["pytest-cov"]
docs = ["mkdocs"]
```

**Without groups** (`install-groups: ''`):
- Command: `uv sync --frozen --no-default-groups`
- Installs: `requests` only

**With specific groups** (`install-groups: 'test docs'`):
- Command: `uv sync --frozen --no-default-groups --group test --group docs`
- Installs: `requests` + `pytest-cov` + `mkdocs`
- Excludes: `httpx` (dev group not requested)

### 3. Lock File Verification

Ensures reproducible builds by validating `uv.lock` matches `pyproject.toml`:

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    verify-lock: 'true'  # Fails if lock is outdated
```

**Skip verification** (useful for dynamic dependency updates):
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    verify-lock: 'false'
```

### 4. Dependency Caching

The action uses `astral-sh/setup-uv@v4` with:
```yaml
enable-cache: true
cache-dependency-glob: uv.lock
```

This caches dependencies based on `uv.lock` hash, significantly speeding up CI runs.

### 5. Comprehensive Logging

The action provides detailed output:
```
Environment information
  Virtual environment: ACTIVATED

  Virtual environment location:
    /home/runner/work/repo/repo/.venv

  Python executable:
    /home/runner/work/repo/repo/.venv/bin/python

  The virtual environment has been automatically activated.
  You can now use 'python' and installed CLI tools directly in subsequent steps.
```

## Usage Scenarios

### Scenario 1: Core Dependencies Only

**Use Case**: Simple project with only core dependencies, no dev tools needed.

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1

  - name: Run application
    run: python main.py
```

**pyproject.toml**:
```toml
[project]
name = "my-app"
version = "1.0.0"
dependencies = ["requests", "pydantic"]
```

**What gets installed**: `requests`, `pydantic` only

### Scenario 2: Development Environment

**Use Case**: Local-style development with all dev tools.

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      install-groups: 'dev'

  - run: black --check .
  - run: mypy src/
  - run: ruff check .
```

**pyproject.toml**:
```toml
[project]
dependencies = ["requests"]

[dependency-groups]
dev = ["black", "mypy", "ruff"]
```

**What gets installed**: `requests` + `black` + `mypy` + `ruff`

### Scenario 3: Testing Workflow

**Use Case**: Run tests without dev tools to match production environment.

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      install-groups: 'groups: test'

  - run: pytest --cov=src --cov-report=xml
  - run: coverage report
```

**pyproject.toml**:
```toml
[project]
dependencies = ["requests"]

[dependency-groups]
dev = ["black", "mypy"]
test = ["pytest", "pytest-cov", "coverage"]
```

**What gets installed**: `requests` + `pytest` + `pytest-cov` + `coverage` (dev tools excluded)

### Scenario 4: Documentation Build

**Use Case**: Build documentation without test/dev dependencies.

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      install-groups: 'docs'

  - run: mkdocs build
  - run: mkdocs gh-deploy --force
```

**pyproject.toml**:
```toml
[project]
dependencies = ["mylib"]

[dependency-groups]
docs = ["mkdocs", "mkdocs-material"]
```

**What gets installed**: `mylib` + `mkdocs` + `mkdocs-material`

### Scenario 5: Multiple Groups

**Use Case**: CI workflow that needs both testing and linting.

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      install-groups: 'dev test'

  - name: Lint
    run: |
      black --check .
      mypy src/

  - name: Test
    run: pytest --cov=src
```

**pyproject.toml**:
```toml
[project]
dependencies = ["requests"]

[dependency-groups]
dev = ["black", "mypy"]
test = ["pytest", "pytest-cov"]
docs = ["mkdocs"]  # Not installed
```

**What gets installed**: `requests` + `black` + `mypy` + `pytest` + `pytest-cov`

**What's excluded**: `mkdocs` (docs group not requested)

### Scenario 6: Matrix Testing Across Python Versions

**Use Case**: Test compatibility with multiple Python versions.

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']

steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      python-version: ${{ matrix.python-version }}
      install-groups: 'groups: test'

  - run: pytest
```

**Result**: Tests run on Python 3.10, 3.11, and 3.12

### Scenario 7: Cross-Platform Testing

**Use Case**: Ensure application works on all major operating systems.

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]

steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      install-groups: 'test'

  - run: pytest
```

**Result**: Tests run on Linux, Windows, and macOS

### Scenario 8: Skip Lock Verification for Dynamic Dependencies

**Use Case**: Dependencies from Git branches or local paths that change frequently.

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
    with:
      verify-lock: 'false'  # Skip lock check
      install-groups: 'dev'
```

**pyproject.toml**:
```toml
[project]
dependencies = ["mylib @ git+https://github.com/user/repo@main"]
```

**Result**: Installs dependencies without lock file validation

### Scenario 9: No Dependency Groups Section

**Use Case**: Simple project without optional dependency groups.

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1

  - run: python app.py
```

**pyproject.toml**:
```toml
[project]
name = "simple-app"
dependencies = ["requests"]
# No [dependency-groups] section
```

**What gets installed**: `requests` only (action handles missing dependency-groups gracefully)

## Dependency Groups

### Dependency Groups vs Optional Dependencies

**Key Differences**:

1. **Dependency Groups** (`[dependency-groups]`):
   - Part of PEP 735 standard
   - Development-only dependencies, not published with package
   - Installed using `--group` flag with `uv sync`
   - Use prefix `groups:` in this action

2. **Optional Dependencies** (`[project.optional-dependencies]`):
   - Part of PEP 621 standard, widely supported
   - Published with your package, can be installed by end users
   - Installed using `--extra` flag with `uv sync`
   - Use prefix `extras:` in this action

### Understanding Dependency Groups

Dependency groups in `pyproject.toml` allow organizing optional dependencies:

```toml
[project]
name = "myapp"
dependencies = ["requests"]  # Core - always installed

[project.optional-dependencies]
aws = ["boto3", "s3fs"]      # Published extras
viz = ["matplotlib", "seaborn"]  # End-user features

[dependency-groups]
dev = ["black", "mypy"]      # Development tools
test = ["pytest", "pytest-cov"]  # Testing tools
docs = ["mkdocs"]            # Documentation tools
```

### Group Installation Behavior

| `install-groups` Value | Command Generated | What Gets Installed |
|------------------------|-------------------|---------------------|
| `''` (empty/default) | `uv sync --frozen --no-default-groups` | Core only |
| `'dev'` | `uv sync --frozen --no-default-groups --group dev` | Core + dev |
| `'test'` | `uv sync --frozen --no-default-groups --group test` | Core + test |
| `'dev test'` | `uv sync --frozen --no-default-groups --group dev --group test` | Core + dev + test |
| `'dev,test,docs'` | `uv sync --frozen --no-default-groups --group dev --group test --group docs` | Core + dev + test + docs |

### Why `--no-default-groups`?

By default, `uv sync` includes certain groups automatically (like `dev`). Using `--no-default-groups` ensures:
- ✅ Clean group isolation
- ✅ Only requested groups are installed
- ✅ Predictable, reproducible builds
- ✅ No unexpected transitive group installations

### Common Group Patterns

**Development**:
```toml
[dependency-groups]
dev = ["black", "mypy", "ruff", "ipython"]
```

**Testing**:
```toml
[dependency-groups]
test = ["pytest", "pytest-cov", "pytest-mock", "faker"]
```

**Documentation**:
```toml
[dependency-groups]
docs = ["mkdocs", "mkdocs-material", "mkdocstrings"]
```

**Production**:
```toml
[dependency-groups]
prod = ["gunicorn", "psycopg2-binary"]
```

## Lock File Verification

### What is Lock File Verification?

`uv.lock` is a lock file that pins exact versions of all dependencies. Verification ensures the lock file is synchronized with `pyproject.toml`.

### When to Enable (Default)

**Enable verification (`verify-lock: 'true'`) when:**
- Working in a team (ensure everyone uses same dependencies)
- Production deployments (reproducible builds)
- CI/CD pipelines (catch dependency drift early)

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    verify-lock: 'true'  # Fails if lock is outdated
```

**Error if outdated**:
```
error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.
```

**Fix**: Run `uv lock` locally and commit the updated lock file.

### When to Disable

**Disable verification (`verify-lock: 'false'`) when:**
- Dependencies change frequently (Git dependencies)
- Development branches with experimental changes
- Prototyping/testing new dependencies

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    verify-lock: 'false'
```

### Lock File Workflow

**Recommended workflow**:
1. Modify `pyproject.toml` (add/update dependencies)
2. Run `uv lock` locally
3. Commit both `pyproject.toml` and `uv.lock`
4. CI runs with `verify-lock: 'true'` and passes

## Virtual Environment

### Automatic Activation

The action automatically activates the virtual environment created by `uv sync` at `.venv`.

**How it works**:
1. Action runs `uv sync` which creates `.venv/`
2. Action adds `.venv/bin` (or `.venv/Scripts` on Windows) to `$GITHUB_PATH`
3. Action sets `$VIRTUAL_ENV` environment variable
4. All subsequent steps use the activated environment

### Using the Environment

**Direct Python/CLI commands** (recommended):
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    install-groups: 'dev test'

- run: python --version
- run: pytest
- run: black .
- run: mypy src/
```

**Alternative: uv run** (also works):
```yaml
- run: uv run pytest
- run: uv run black .
```

**Manual activation** (unnecessary but possible):
```yaml
- run: |
    source .venv/bin/activate  # Linux/macOS
    python --version
```

### Environment Location

The virtual environment is always at:
- **Linux/macOS**: `$(pwd)/.venv`
- **Windows**: `$(pwd)\.venv`

**Python executable**:
- **Linux/macOS**: `.venv/bin/python`
- **Windows**: `.venv\Scripts\python.exe`

## Testing Guide

This action is comprehensively tested across multiple scenarios. Reference: `.github/workflows/test-python-setup-uv.yml`

### Test Coverage

| Test Job | Purpose | Validates |
|----------|---------|-----------|
| `test-uv-basic` | Default behavior | Core dependencies only, no groups |
| `test-uv-custom-groups` | Specific groups | Only requested groups installed, others excluded |
| `test-uv-no-groups` | Explicit empty groups | Core only with `install-groups: ''` |
| `test-uv-lock-verification` | Lock validation | Lock file check passes |
| `test-uv-lock-verification-disabled` | Skip lock check | Works with `verify-lock: 'false'` |
| `test-uv-lock-verification-fail` | Outdated lock handling | Fails gracefully when lock is outdated |
| `test-uv-matrix` | Cross-platform/version | Works on Linux/Windows/macOS, Python 3.10/3.11/3.12 |
| `test-uv-cache` | Dependency caching | Cache populated and restored |
| `test-uv-comma-separated-groups` | Group parsing | `'dev,test,docs'` format works |
| `test-uv-mixed-separators` | Group parsing | `'dev, test docs'` format works |
| `test-uv-space-separated-groups` | Group parsing | `'dev test docs'` format works |
| `test-uv-no-dependency-groups-section` | Missing groups | Works without `[dependency-groups]` |
| `test-uv-explicit-dev-group` | Specific dev group | Dev group installs when requested |

### Running Tests

**Test in your repository**:
```yaml
name: Test uv action

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
        with:
          install-groups: 'dev test'
      - run: pytest
```

**Local testing with act**:
```bash
# Install act
choco install act-cli  # Windows
brew install act       # macOS

# Run test workflow
act -j test-uv-basic
```

## Troubleshooting

### Error: "The lockfile at `uv.lock` needs to be updated"

**Cause**: Lock file is outdated compared to `pyproject.toml`.

**Solution**:
```bash
# Update lock file locally
uv lock

# Commit the changes
git add pyproject.toml uv.lock
git commit -m "Update dependencies"
git push
```

**Or** disable verification temporarily:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    verify-lock: 'false'
```

### Error: "No such file or directory: uv.lock"

**Cause**: Lock file doesn't exist in repository.

**Solution**:
```bash
# Generate lock file
uv lock

# Commit it
git add uv.lock
git commit -m "Add uv.lock file"
git push
```

### Wrong Python Version

**Issue**: Action installs Python 3.12 but need 3.10.

**Solution**: Specify version explicitly:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    python-version: '3.10'
```

### Dependency Not Found After Installation

**Issue**: `ModuleNotFoundError` even after installation.

**Possible causes**:
1. **Group not specified**: Dependency is in optional group not requested
   ```yaml
   # Wrong: dev group has pytest but not installed
   install-groups: 'test'

   # Fix: Add dev group
   install-groups: 'dev test'
   ```

2. **Wrong import name**: Package name ≠ import name
   ```toml
   # Package: "pyyaml", Import: "yaml"
   dependencies = ["pyyaml"]
   ```
   ```python
   import yaml  # Not: import pyyaml
   ```

### Groups Not Isolated

**Issue**: Unwanted packages installed even though group not specified.

**Cause**: Before the fix, the action used `--group` which included default groups.

**Solution**: Use latest version of the action which uses `--no-default-groups`:
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1  # Latest
```

### Virtual Environment Not Activated

**Issue**: `python: command not found` or wrong Python version.

**Verification**:
```yaml
- run: |
    echo "Python: $(which python)"
    echo "PATH: $PATH"
    echo "VIRTUAL_ENV: $VIRTUAL_ENV"
```

**Expected output**:
```
Python: /home/runner/work/repo/repo/.venv/bin/python
PATH: /home/runner/work/repo/repo/.venv/bin:...
VIRTUAL_ENV: /home/runner/work/repo/repo/.venv
```

**If not working**: Check GitHub Actions runner logs for warnings in "Activate virtual environment" step.

### Cache Not Working

**Symptoms**: Dependencies reinstall on every run.

**Debug**:
1. Check `uv.lock` exists and is committed
2. Verify cache hit in action logs:
   ```
   Restored cache from key: setup-uv-...
   ```
3. Check lock file hasn't changed between runs

**Force cache refresh**:
Change `uv.lock` content (update dependencies).

## Best Practices

### 1. Always Commit Lock File

```bash
# Generate lock file
uv lock

# Always commit both files together
git add pyproject.toml uv.lock
git commit -m "Update dependencies"
```

**Why**: Ensures reproducible builds across all environments.

### 2. Use Specific Python Versions

```yaml
# Good: Explicit version
python-version: '3.11'

# Avoid: Version ranges or latest
python-version: '3.x'  # Too broad
```

### 3. Organize Dependency Groups by Purpose

```toml
# Good: Clear separation
[dependency-groups]
dev = ["black", "mypy", "ruff"]
test = ["pytest", "pytest-cov"]
docs = ["mkdocs"]

# Avoid: Single "dev" group for everything
[dependency-groups]
dev = ["black", "mypy", "pytest", "mkdocs"]  # Too broad
```

### 4. Use Lock Verification in CI

```yaml
# Good: Catch dependency drift early
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    verify-lock: 'true'  # Default, but explicit is clear
```

### 5. Pin Action Versions

```yaml
# Good: Pin to major version (gets updates)
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1

# Good: Pin to exact commit (maximum stability)
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@abc1234

# Avoid: Using @main (unpredictable)
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@main
```

### 6. Separate Workflows by Purpose

```yaml
# lint.yml
- uses: .../actions/python-setup/uv@v1
  with:
    install-groups: 'dev'
- run: black --check .
- run: mypy src/

# test.yml
- uses: .../actions/python-setup/uv@v1
  with:
    install-groups: 'test'
- run: pytest

# docs.yml
- uses: .../actions/python-setup/uv@v1
  with:
    install-groups: 'docs'
- run: mkdocs build
```

### 7. Use Matrix for Multi-Version Testing

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
    os: [ubuntu-latest, windows-latest, macos-latest]

steps:
  - uses: .../actions/python-setup/uv@v1
    with:
      python-version: ${{ matrix.python-version }}
```

## Comparison with Other Actions

| Feature | This Action | actions/setup-python | astral-sh/setup-uv alone |
|---------|-------------|----------------------|--------------------------|
| Python Installation | ✓ | ✓ | ✗ (requires setup-python) |
| uv Installation | ✓ | ✗ | ✓ |
| Dependency Installation | ✓ (automatic) | ✗ (manual) | ✗ (manual) |
| Group Support | ✓ (built-in) | ✗ | ✓ (manual) |
| Lock Verification | ✓ (built-in) | ✗ | ✗ (manual) |
| Auto VEnv Activation | ✓ | ✗ | ✗ |
| Dependency Caching | ✓ | ✓ (pip only) | ✓ |
| Group Isolation | ✓ (`--no-default-groups`) | N/A | ✗ (manual) |

**When to use this action:**
- Modern Python projects using `pyproject.toml`
- Need dependency group support
- Want automatic environment activation
- Prefer uv's speed over pip

**When to use alternatives:**
- `actions/setup-python` alone: Minimal setup, no uv needed
- `astral-sh/setup-uv` alone: Need full control over uv commands

## Additional Resources

- [uv documentation](https://docs.astral.sh/uv/)
- [PEP 735: Dependency Groups](https://peps.python.org/pep-0735/)
- [actions/setup-python](https://github.com/actions/setup-python)
- [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv)

## Support

For issues, questions, or contributions:
- Repository: https://github.com/Serapieum-of-alex/github-actions
- Issues: https://github.com/Serapieum-of-alex/github-actions/issues
