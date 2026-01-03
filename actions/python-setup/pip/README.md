# Python Setup with pip

Setup Python environment with pip package manager for pyproject.toml projects using the standard GitHub `actions/setup-python@v4` action.

## Usage

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
  with:
    python-version: '3.12'
    cache: 'pip'
    architecture: 'x64'
    install-groups: 'dev test'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | No | `3.12` |
| `cache` | Cache packages dependencies (pip, pipenv, poetry) | No | `pip` |
| `architecture` | Target architecture for Python to use (x64, x86) | No | `x64` |
| `install-groups` | Dependency groups to install (e.g., "dev", "test docs") | No | `''` |

## Features

- **pyproject.toml Support**: Automatically detects and installs dependencies from `pyproject.toml` with optional dependency groups support
- **Package Caching**: Built-in support for caching pip, pipenv, or poetry dependencies
- **Cross-Platform**: Supports different architectures and operating systems
- **Pip Upgrade**: Automatically upgrades pip to the latest version
- **Package Listing**: Shows installed packages for debugging

## Example Workflows

### Basic Python Setup
```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
```

### Specific Python Version with Poetry Caching
```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
    with:
      python-version: '3.11'
      cache: 'poetry'
```

### pyproject.toml with Dependency Groups
```yaml
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
    with:
      python-version: '3.12'
      install-groups: 'dev test docs'
```

### Multiple Python Versions Matrix
```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
    
steps:
  - uses: actions/checkout@v5
  - uses: Serapieum-of-alex/github-actions/actions/python-setup/pip@v1
    with:
      python-version: ${{ matrix.python-version }}
```

## When to Use

Use this action when:
- You want standard Python setup without additional package managers
- Your project uses `pyproject.toml` for dependency management
- You need dependency groups support with standard pip
- You don't require advanced dependency management features like uv

For projects using modern package managers like `uv`, consider using `actions/python-setup/uv` instead.