# Python Setup Actions

Actions for setting up Python environments with different package managers.

## Available Actions

### uv (`actions/python-setup/uv`)
Setup Python with uv package manager.

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    python-version: '3.12'
    install-groups: 'dev docs'  # Dependency groups from [dependency-groups]
    verify-lock: 'true'
```

#### Installing Optional Dependencies (Extras)

You can also install optional dependencies from `[project.optional-dependencies]` by prefixing them with `extra:`:

```yaml
# Install only optional dependencies
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    install-groups: 'extra:aws extra:viz'

# Mix dependency groups and optional dependencies
- uses: Serapieum-of-alex/github-actions/actions/python-setup/uv@v1
  with:
    install-groups: 'dev test extra:aws extra:viz'
```

#### Inputs

- `python-version`: Python version to install (default: '3.12')
- `install-groups`: Space or comma-separated list of dependency groups and/or optional dependencies to install
  - Dependency groups: Use plain names like `dev`, `test`, `docs`
  - Optional dependencies: Prefix with `extra:` like `extra:aws`, `extra:viz`
  - Leave empty to install only core dependencies
- `verify-lock`: Whether to verify the lock file is up to date (default: 'true')

## Usage Patterns

### For General Development
Use `actions/python-setup/uv` for most development workflows.

### For Documentation
Use `actions/mkdocs-deploy/setup` which supports multiple package managers.

### For Cross-Project Compatibility
Use `actions/python-setup/uv` for general Python setup needs.

## Example pyproject.toml

```toml
[project]
name = "my-package"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["requests", "pydantic"]

# Optional dependencies - published with package
[project.optional-dependencies]
aws = ["boto3", "s3fs"]
viz = ["matplotlib", "seaborn"]
api = ["fastapi", "uvicorn"]

# Development dependencies - not published
[dependency-groups]
dev = ["ruff", "mypy", "pre-commit"]
test = ["pytest", "pytest-cov", "pytest-mock"]
docs = ["mkdocs", "mkdocs-material"]
```