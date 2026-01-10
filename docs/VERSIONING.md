# Versioning Guide for GitHub Actions

This document explains the versioning strategy used in this repository for publishing and maintaining GitHub Actions.

## Table of Contents

- [Overview](#overview)
- [Semantic Versioning](#semantic-versioning)
- [Tag Strategy](#tag-strategy)
- [Release Process](#release-process)
- [Moving Major Version Tags](#moving-major-version-tags)
- [Usage for Consumers](#usage-for-consumers)
- [Breaking Changes](#breaking-changes)
- [Examples](#examples)

## Overview

This repository contains reusable GitHub Actions (composite actions). Unlike traditional software packages, GitHub Actions use a **tag-based versioning system** where users reference specific versions directly in their workflows.

**Key Principles:**
- ✅ Use semantic versioning (e.g., `v1.0.0`, `v1.1.0`, `v2.0.0`)
- ✅ Maintain moving major version tags (e.g., `v1`, `v2`) for convenience
- ✅ Keep specific version tags immutable (e.g., `v1.0.0` never changes)
- ✅ Use `v` prefix for all version tags

## Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/) with the format: `vMAJOR.MINOR.PATCH`

### Version Components

```
v1.2.3
│ │ │
│ │ └── PATCH: Bug fixes, documentation updates (backward compatible)
│ └──── MINOR: New features, improvements (backward compatible)
└────── MAJOR: Breaking changes (NOT backward compatible)
```

### When to Increment

| Version | Increment When | Examples |
|---------|---------------|----------|
| **PATCH** | Bug fixes, docs, internal refactoring | `v1.0.0` → `v1.0.1` |
| **MINOR** | New features, new inputs (optional), deprecations | `v1.0.1` → `v1.1.0` |
| **MAJOR** | Breaking changes, removed features, required inputs changed | `v1.1.0` → `v2.0.0` |

### Examples of Changes

#### PATCH Version (v1.0.0 → v1.0.1)
- 🐛 Fix a bug in cache key generation
- 📝 Update documentation
- 🔧 Internal code refactoring
- ⚡ Performance improvements (no behavior change)

#### MINOR Version (v1.0.1 → v1.1.0)
- ✨ Add new optional input parameter
- 🎉 Add new feature that doesn't affect existing usage
- 📊 Add new logging/output
- ⚠️ Deprecate a feature (but still works)

#### MAJOR Version (v1.1.0 → v2.0.0)
- 💥 Remove or rename an input parameter
- 💥 Change default behavior significantly
- 💥 Remove deprecated features
- 💥 Change required inputs or validation rules
- 💥 Update to incompatible dependency versions

## Tag Strategy

### Two Types of Tags

We maintain two types of Git tags:

#### 1. Specific Version Tags (Immutable)

**Format:** `v1.0.0`, `v1.1.0`, `v1.2.0`, `v2.0.0`

**Characteristics:**
- ✅ Never moved or changed
- ✅ Point to a specific commit forever
- ✅ Used for reproducibility and security
- ✅ Ideal for production workflows

**Example:**
```yaml
# Pin to exact version - never changes
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1.0.0
```

#### 2. Major Version Tags (Moving)

**Format:** `v1`, `v2`, `v3`

**Characteristics:**
- 🔄 Updated with each new release within the major version
- 🔄 Points to the latest compatible version
- 🔄 Used for automatic updates
- ⚠️ May change behavior (but stays backward compatible)

**Example:**
```yaml
# Use major version - gets updates automatically
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1
```

### Visual Representation

```
Timeline of commits and tags:

A ---- B ---- C ---- D ---- E ---- F
       ↑      ↑            ↑      ↑
       │      │            │      │
    v1.0.0  v1.1.0      v1.2.0  v2.0.0
       ↑                   ↑      ↑
       v1 (initially)      │      v2
                           │
                      v1 (moved)
                      
After release flow:
- v1.0.0: Created v1 and v1.0.0 pointing to commit B
- v1.1.0: Created v1.1.0 at commit C, kept v1.0.0 at B
- v1.2.0: Created v1.2.0 at commit E, moved v1 from B to E
- v2.0.0: Created v2 and v2.0.0 pointing to commit F
```

## Release Process

### Step-by-Step Guide

#### 1. Prepare the Release

Make and commit your changes:

```bash
# Make your changes
git add .
git commit -m "feat: add caching support to pixi action"
git push origin main
```

#### 2. Create Specific Version Tag

```bash
# Create an annotated tag
git tag -a v1.1.0 -m "Release v1.1.0

- Add caching support for faster CI runs
- Improve error messages for missing lock files
- Update documentation with caching examples"

# Push the tag
git push origin v1.1.0
```

#### 3. Create or Move Major Version Tag

```bash
# Move the major version tag to the new release
git tag -fa v1 -m "Update v1 to v1.1.0"

# Force push (required because we're overwriting an existing tag)
git push origin v1 --force
```

#### 4. Create GitHub Release

**Option A: Using GitHub CLI**

```bash
gh release create v1.1.0 \
  --title "v1.1.0 - Caching Support" \
  --notes "## 🎉 New Features

- **Caching**: Enable environment caching with \`cache: 'true'\`
- **Improved Errors**: Better error messages for common issues

## 📝 Documentation

- Updated pixi.md with caching examples
- Added troubleshooting section

## 🔧 Internal

- Refactored validation logic
- Added integration tests for caching

## 📦 Upgrade Notes

This is a backward-compatible release. Simply update your action reference from \`@v1.0.0\` to \`@v1.1.0\` or use \`@v1\` for automatic updates."
```

**Option B: Using GitHub Web UI**

1. Go to your repository on GitHub
2. Click **"Releases"** → **"Draft a new release"**
3. Click **"Choose a tag"** → Select `v1.1.0`
4. Set **"Release title"**: `v1.1.0 - Caching Support`
5. Write **release notes** (see format above)
6. Click **"Publish release"**

### Automated Release Workflow

Create `.github/workflows/release.yml` to automate releases:

```yaml
name: Create Release

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get version info
        id: version
        run: |
          TAG=${GITHUB_REF#refs/tags/}
          MAJOR_VERSION=$(echo $TAG | cut -d. -f1)
          echo "tag=$TAG" >> $GITHUB_OUTPUT
          echo "major=$MAJOR_VERSION" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
          draft: false
          prerelease: false

      - name: Update major version tag
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git tag -fa ${{ steps.version.outputs.major }} -m "Update ${{ steps.version.outputs.major }} to ${{ steps.version.outputs.tag }}"
          git push origin ${{ steps.version.outputs.major }} --force
```

**How it works:**
1. Push a version tag: `git push origin v1.1.0`
2. Workflow automatically:
   - Creates a GitHub release
   - Generates release notes from commits
   - Moves the major version tag (`v1`)

## Moving Major Version Tags

### What Does "Moving" Mean?

**Moving a tag** means updating a Git tag to point to a different commit. This is done by:
1. Deleting the old tag (with `-f` flag)
2. Creating a new tag with the same name at a different commit
3. Force-pushing to overwrite the remote tag

### Why Move Major Version Tags?

This allows users to:
- ✅ Get automatic bug fixes and features
- ✅ Stay within a major version (no breaking changes)
- ✅ Avoid updating workflow files for every patch/minor release

### Commands Explained

```bash
# -f  = force (allows overwriting existing tag)
# -a  = annotated (creates tag with metadata)
git tag -fa v1 -m "Update v1 to v1.1.0"

# --force = required to overwrite remote tag
git push origin v1 --force
```

### Example Flow

**Initial Release (v1.0.0):**
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

git tag -a v1 -m "Major version v1 -> v1.0.0"
git push origin v1
```

Result: Both `v1` and `v1.0.0` point to the same commit.

**Bug Fix Release (v1.0.1):**
```bash
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1

# Move v1 to point to v1.0.1
git tag -fa v1 -m "Update v1 -> v1.0.1"
git push origin v1 --force
```

Result: 
- `v1.0.0` → Still points to old commit
- `v1.0.1` → Points to new commit
- `v1` → Now points to new commit (moved)

**New Feature Release (v1.1.0):**
```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# Move v1 again
git tag -fa v1 -m "Update v1 -> v1.1.0"
git push origin v1 --force
```

Result: `v1` now points to v1.1.0 (moved again).

**Breaking Change Release (v2.0.0):**
```bash
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin v2.0.0

# Create NEW major version tag (don't move v1)
git tag -a v2 -m "Major version v2 -> v2.0.0"
git push origin v2
```

Result: 
- `v1` → Still points to v1.1.0
- `v2` → Points to v2.0.0 (new tag)
- Users must explicitly update to `@v2`

## Usage for Consumers

### Referencing Actions

Users can reference your actions in three ways:

#### Option 1: Specific Version (Recommended for Production)

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1.0.0
```

**Pros:**
- ✅ Completely stable and reproducible
- ✅ Never changes unexpectedly
- ✅ Best for security-critical workflows

**Cons:**
- ❌ Doesn't get bug fixes automatically
- ❌ Must manually update for new features

**Best for:** Production, security-sensitive, compliance-required workflows

#### Option 2: Major Version (Recommended for Most Users)

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1
```

**Pros:**
- ✅ Gets bug fixes automatically
- ✅ Gets new features automatically (within v1.x.x)
- ✅ No breaking changes

**Cons:**
- ❌ Behavior may change slightly
- ❌ Requires trust in maintainers

**Best for:** Most workflows, active development, CI/CD pipelines

#### Option 3: Branch (Not Recommended)

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@main
```

**Pros:**
- ✅ Always latest code

**Cons:**
- ❌ Can break at any time
- ❌ Includes breaking changes
- ❌ Not reproducible

**Best for:** Testing unreleased features, development only

### Recommendation Matrix

| Use Case | Recommended Reference | Example |
|----------|----------------------|---------|
| Production workflows | Specific version | `@v1.0.0` |
| CI/CD pipelines | Major version | `@v1` |
| Active development | Major version | `@v1` |
| Security-critical | Specific version | `@v1.0.0` |
| Testing new features | Branch | `@main` |
| Dependabot/Renovate | Major version | `@v1` |

## Breaking Changes

### What Constitutes a Breaking Change?

A breaking change requires a **major version bump** (e.g., v1.x.x → v2.0.0).

#### Breaking Changes (Require v2.0.0):

- ❌ Removing an input parameter
- ❌ Renaming an input parameter
- ❌ Changing an input from optional to required
- ❌ Changing default values that affect behavior
- ❌ Removing or renaming outputs
- ❌ Changing behavior in incompatible ways
- ❌ Dropping support for older versions (e.g., Python 3.7)
- ❌ Changing error handling that could break workflows

#### NOT Breaking Changes (Can be v1.1.0):

- ✅ Adding new optional input parameters
- ✅ Adding new outputs
- ✅ Deprecating features (but still working)
- ✅ Bug fixes that restore intended behavior
- ✅ Performance improvements
- ✅ Documentation updates
- ✅ Adding new features that don't affect existing usage

### Handling Breaking Changes

#### 1. Deprecation Period (Preferred)

Before making a breaking change, deprecate in a minor version:

**v1.5.0 - Deprecation:**
```yaml
inputs:
  old-name:
    description: 'DEPRECATED: Use new-name instead'
    required: false
```

Add warning in action:
```yaml
- name: Deprecation warning
  if: inputs.old-name != ''
  shell: bash
  run: |
    echo "::warning::Input 'old-name' is deprecated and will be removed in v2.0.0. Use 'new-name' instead."
```

**v2.0.0 - Removal:**
```yaml
inputs:
  new-name:
    description: 'Replacement for old-name'
    required: false
```

#### 2. Migration Guide

Always provide a migration guide in the release notes:

```markdown
## 💥 Breaking Changes in v2.0.0

### Removed `cache-key` input

The `cache-key` input has been removed. Caching now uses an automatic key based on `pixi.lock`.

**Migration:**

```diff
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v1
  with:
-   cache-key: custom-key
    cache: 'true'
```

The action will automatically generate an optimal cache key.

### Changed `verify-lock` default

The default for `verify-lock` changed from `'false'` to `'true'`.

**Migration:**

If you want the old behavior:

```yaml
- uses: Serapieum-of-alex/github-actions/actions/python-setup/pixi@v2
  with:
    verify-lock: 'false'  # Explicit old behavior
```
```

## Examples

### Example 1: First Release

```bash
# Initial release
git tag -a v1.0.0 -m "Release v1.0.0: Initial release"
git push origin v1.0.0

git tag -a v1 -m "Major version v1"
git push origin v1

gh release create v1.0.0 --title "v1.0.0 - Initial Release" --generate-notes
```

### Example 2: Bug Fix

```bash
# Bug fix release
git tag -a v1.0.1 -m "Release v1.0.1: Fix cache key generation"
git push origin v1.0.1

# Move v1 to include the fix
git tag -fa v1 -m "Update v1 to v1.0.1"
git push origin v1 --force

gh release create v1.0.1 --title "v1.0.1 - Bug Fixes" --notes "Fix cache key generation for Windows"
```

### Example 3: New Feature

```bash
# New feature release
git tag -a v1.1.0 -m "Release v1.1.0: Add caching support"
git push origin v1.1.0

# Move v1 to include the feature
git tag -fa v1 -m "Update v1 to v1.1.0"
git push origin v1 --force

gh release create v1.1.0 --title "v1.1.0 - Caching Support" --generate-notes
```

### Example 4: Breaking Change

```bash
# Breaking change release
git tag -a v2.0.0 -m "Release v2.0.0: Remove deprecated inputs"
git push origin v2.0.0

# Create NEW major version tag (don't touch v1)
git tag -a v2 -m "Major version v2"
git push origin v2

gh release create v2.0.0 --title "v2.0.0 - Breaking Changes" --notes "See MIGRATION.md for upgrade guide"
```

## Best Practices

### For Maintainers

1. ✅ **Always use annotated tags** (`-a` flag) with meaningful messages
2. ✅ **Test thoroughly** before releasing
3. ✅ **Write clear release notes** explaining what changed
4. ✅ **Pin action dependencies** to specific SHA or version tags
5. ✅ **Document breaking changes** with migration guides
6. ✅ **Use deprecation warnings** before removing features
7. ✅ **Keep v1, v2, etc. updated** with each release
8. ✅ **Never delete or force-push specific version tags** (only major versions)

### For Consumers

1. ✅ **Use major version tags** for most workflows (`@v1`)
2. ✅ **Pin specific versions** for critical/production workflows (`@v1.0.0`)
3. ✅ **Read release notes** when major versions change
4. ✅ **Test in staging** before updating major versions
5. ✅ **Use Dependabot/Renovate** to track updates
6. ✅ **Never use `@main`** in production

## Checklist for Releases

### Pre-Release

- [ ] All changes committed and pushed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] CHANGELOG updated (if applicable)
- [ ] Version number decided (PATCH/MINOR/MAJOR)
- [ ] Breaking changes documented
- [ ] Migration guide written (if breaking changes)

### Release

- [ ] Create specific version tag (e.g., `v1.1.0`)
- [ ] Push specific version tag
- [ ] Move major version tag (e.g., `v1`)
- [ ] Force push major version tag
- [ ] Create GitHub release with notes
- [ ] Test the release in a sample workflow

### Post-Release

- [ ] Verify tags are correct on GitHub
- [ ] Verify release notes are clear
- [ ] Update README if needed
- [ ] Announce in relevant channels
- [ ] Monitor for issues

## References

- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Versioning](https://github.com/actions/toolkit/blob/master/docs/action-versioning.md)
- [Git Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Maintained by**: Serapieum-of-alex

