# Python Setup with pixi

Setup Python environment with pixi package manager and install dependencies.

## Usage

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1
  with:
    environments: 'py312'
    activate-environment: 'py312'
    verify-lock: 'false'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `environments` | Pixi environments to install. For multiple environments, separate with spaces (e.g., "py311", "py312 py313") | No | `default` |
| `activate-environment` | Environment to activate after installation | No | `default` |
| `verify-lock` | Whether to verify the lock file is up to date | No | `false` |

## Examples

### Basic Setup
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1
```

### Multi-environment Setup
When using multiple environments, separate them with spaces. The action will install all specified environments but only activate the one specified in `activate-environment`:

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1
  with:
    environments: 'py311 py312 py313'  # Space-separated environment names
    activate-environment: 'py312'      # Which environment to activate
```

### With Lock File Verification
```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1
  with:
    environments: 'py312'
    verify-lock: 'true'
```


## Features

- Installs and configures pixi package manager
- Sets up specified Python environments
- Activates the target environment
- Provides dependency caching with pixi.lock file
- Optional lock file verification
- Environment and package listing for debugging
- Cross-platform support (Linux, macOS, Windows)

## Notes

- This action uses `prefix-dev/setup-pixi@v0.9.0` under the hood with pixi version v0.49.0
- Cache key is automatically generated based on `pixi.lock` file hash
- Cache writes are automatically enabled only on pushes to the main branch
- The action will list environment information and installed packages for debugging purposes
- Lock file verification is optional and disabled by default (unlike uv action)