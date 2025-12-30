# MkDocs Deploy Action

Deploy MkDocs documentation to GitHub Pages with versioning support using Mike. Supports multiple package managers and deployment strategies.

## Usage

This action is designed to be used in a workflow that handles different deployment scenarios. You'll typically want separate jobs for each trigger type.

### Complete Workflow Example

```yaml
name: Deploy MkDocs

permissions:
  contents: write
  pages: write

on:
  push:
    branches: [main]
  pull_request:
    branches: ['**']
  release:
    types: [published]

jobs:
  deploy-pr:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
        with:
          trigger: 'pull_request'
          package-manager: 'uv'
          deploy-token: ${{ secrets.ACTIONS_DEPLOY_TOKEN }}

  deploy-main:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
        with:
          trigger: 'main'
          package-manager: 'uv'
          deploy-token: ${{ secrets.ACTIONS_DEPLOY_TOKEN }}

  deploy-release:
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    steps:
      - uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
        with:
          trigger: 'release'
          package-manager: 'uv'
          deploy-token: ${{ secrets.ACTIONS_DEPLOY_TOKEN }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `trigger` | Deployment trigger type (`pull_request`, `main`, `release`) | Yes | - |
| `package-manager` | Package manager to use (`pip`, `uv`, `pixi`) | No | `uv` |
| `python-version` | Python version to install | No | `3.12` |
| `install-groups` | Dependency groups to install | No | `docs` |
| `deploy-token` | GitHub token for deployment | Yes | - |
| `release-tag` | Release tag version (for release trigger) | No | `''` |
| `mike-alias` | Mike alias for releases (e.g., latest) | No | `latest` |

## Deployment Strategies

### Pull Request
- Deploys to `develop` branch in gh-pages
- Used for preview deployments

### Main Branch
- Deploys to `main` branch in gh-pages
- Sets as default version
- Used for stable documentation

### Release
- Deploys with release tag and alias
- Sets alias as default (typically `latest`)
- Used for versioned releases

## Package Manager Support

### UV (Default)
```yaml
- uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
  with:
    package-manager: 'uv'
```

### Pip
```yaml
- uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
  with:
    package-manager: 'pip'
```

### Pixi
```yaml
- uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
  with:
    package-manager: 'pixi'
```

## Advanced Configuration

### Custom Python Version and Groups
```yaml
- uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
  with:
    trigger: 'main'
    python-version: '3.11'
    install-groups: 'docs dev'
    package-manager: 'pip'
    deploy-token: ${{ secrets.ACTIONS_DEPLOY_TOKEN }}
```

### Custom Release Configuration
```yaml
- uses: Serapieum-of-alex/github-actions/actions/mkdocs-deploy@v1
  with:
    trigger: 'release'
    release-tag: 'v2.0.0'
    mike-alias: 'stable'
    deploy-token: ${{ secrets.ACTIONS_DEPLOY_TOKEN }}
```

## Requirements

1. **Dependencies**: Your project should have MkDocs and Mike configured with the specified dependency groups
2. **Token**: The `ACTIONS_DEPLOY_TOKEN` secret must be configured in your repository
3. **Permissions**: The workflow needs `contents: write` and `pages: write` permissions

Note: The action automatically checks out the repository with full git history (`fetch-depth: 0`) which is required for Mike's versioning functionality.

## Mike Integration

This action uses [Mike](https://github.com/jimporter/mike) for version management:
- **Pull Request**: `mike deploy --push develop`
- **Main**: `mike deploy --push main && mike set-default --push main`
- **Release**: `mike deploy --push --update-aliases {tag} {alias} && mike set-default --push {alias}`

## When to Use

Use this action when:
- You want consistent MkDocs deployment across multiple repositories
- You need support for different package managers
- You want versioned documentation with Mike
- You need different deployment strategies for PR/main/release

For simpler setups, you might prefer using the individual python-setup actions directly.