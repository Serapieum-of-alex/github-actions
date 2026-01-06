# Quick Reference - MkDocs Deploy Test Fixtures

## Adding a New Test

1. **Create directory**:
   ```bash
   mkdir tests/mkdocs-deploy/test-<name>
   mkdir tests/mkdocs-deploy/test-<name>/docs
   ```

2. **Create files**:
   - `pyproject.toml` - Dependencies
   - `mkdocs.yml` - Site config
   - `docs/index.md` - Content

3. **Update workflow**:
   ```yaml
   - name: Copy test fixture files
     run: |
       cp tests/mkdocs-deploy/test-<name>/pyproject.toml .
       cp tests/mkdocs-deploy/test-<name>/mkdocs.yml .
       cp -r tests/mkdocs-deploy/test-<name>/docs .
   ```

## Using Existing Fixtures

### Pip/UV Test
```bash
cd tests/mkdocs-deploy/test-pull-request-pip-uv
pip install -e ".[docs]"
mkdocs build
```

### Pixi Test
```bash
cd tests/mkdocs-deploy/test-pull-request-pixi
pixi install  # Generates pixi.lock
pixi run mkdocs build
```

## File Templates

### Minimal pyproject.toml (pip/uv)
```toml
[project]
name = "test-name"
version = "0.1.0"
dependencies = []

[dependency-groups]
docs = ["mkdocs>=1.5.0", "mike>=2.1.0"]
```

### Minimal pyproject.toml (pixi)
```toml
[project]
name = "test-name"
version = "0.1.0"

[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-64", "win-64"]

[tool.pixi.dependencies]
python = ">=3.11"

[tool.pixi.feature.docs.dependencies]
mkdocs = ">=1.5.0"
mike = ">=2.1.0"

[tool.pixi.environments]
docs = ["docs"]
```

### Minimal mkdocs.yml
```yaml
site_name: Test Name

theme:
  name: material

nav:
  - Home: index.md
```

## Common Commands

```bash
# List all fixtures
ls tests/mkdocs-deploy/test-*/

# Generate pixi locks
cd tests/mkdocs-deploy
python generate-pixi-locks.py

# Test a specific fixture
cd tests/mkdocs-deploy/test-<name>
pip install uv
uv pip install -e ".[docs]"
mkdocs build

# Clean generated files
rm -rf */pixi.lock */site/ */.venv/
```

## Workflow Integration

```yaml
# Matrix test
strategy:
  matrix:
    test: [test-name1, test-name2]
steps:
  - name: Copy fixture
    run: |
      cp tests/mkdocs-deploy/${{ matrix.test }}/pyproject.toml .
      cp tests/mkdocs-deploy/${{ matrix.test }}/mkdocs.yml .
      cp -r tests/mkdocs-deploy/${{ matrix.test }}/docs .
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| pixi.lock missing | Run `pixi install` in the test directory |
| mkdocs not found | Check `[dependency-groups]` or `[tool.pixi.feature.docs.dependencies]` |
| Import errors | Ensure dependencies are in correct section |
| File not found | Check paths are relative to repo root |

## Dependencies Version Requirements

- mkdocs: `>=1.5.0`
- mkdocs-material: `>=9.5.0` (optional)
- mike: `>=2.1.0`
- Python: `>=3.11`

