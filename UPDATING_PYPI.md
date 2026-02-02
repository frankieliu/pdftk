# How to Update pdftk-python on PyPI

This guide shows how to publish updates to PyPI after making changes.

## Quick Reference

```bash
# 1. Bump version in pyproject.toml
# 2. Update CHANGELOG.md
# 3. Commit changes
# 4. Build and publish
uv run python -m build
uv run python -m twine upload dist/*
# 5. Create GitHub release
# 6. Update local installation
uv tool upgrade pdftk-python
```

## Detailed Steps

### Step 1: Bump Version Number

Edit `pyproject.toml` and increment the version:

```toml
[project]
name = "pdftk-python"
version = "0.1.1"  # Was 0.1.0, increment patch version
```

**Version numbering guide:**
- **Patch (0.1.X)** - Bug fixes, documentation, minor improvements
- **Minor (0.X.0)** - New features, backwards-compatible
- **Major (X.0.0)** - Breaking changes

For adding help text examples, use a patch version (0.1.1).

### Step 2: Update CHANGELOG.md

Add a new section at the top:

```markdown
# Changelog

## [0.1.1] - 2026-02-02

### Added
- Enhanced CLI help text for `cat` operation with examples
- Examples showing multi-file operations with different page ranges
- Test suite for multi-PDF operations

### Changed
- Improved documentation for space-separated page ranges

## [0.1.0] - 2026-01-02
...
```

### Step 3: Commit Your Changes

```bash
# Check what changed
git status
git diff

# Stage changes
git add .

# Commit
git commit -m "v0.1.1: Add CLI help examples for multi-file operations"

# Push to GitHub
git push origin main
```

### Step 4: Clean Previous Build

```bash
# Remove old distribution files
rm -rf dist/ build/ *.egg-info src/*.egg-info
```

### Step 5: Build New Distribution

```bash
# Build source distribution and wheel
uv run python -m build

# This creates:
# - dist/pdftk_python-0.1.1-py3-none-any.whl
# - dist/pdftk_python-0.1.1.tar.gz
```

### Step 6: Test Build Locally (Optional but Recommended)

```bash
# Create test environment
python -m venv test-env
source test-env/bin/activate

# Install from local wheel
pip install dist/pdftk_python-0.1.1-py3-none-any.whl

# Test it works
pdftk --version  # Should show 0.1.1
pdftk cat --help  # Should show new examples

# Cleanup
deactivate
rm -rf test-env
```

### Step 7: Upload to PyPI

```bash
# Upload to PyPI
uv run python -m twine upload dist/*

# You'll be prompted for credentials
# Use API token for authentication (see Authentication section below)
```

### Step 8: Create GitHub Release

1. Go to https://github.com/frankieliu/pdftk/releases/new
2. Fill in:
   - **Tag:** `v0.1.1` (create on publish)
   - **Title:** `v0.1.1 - CLI Help Examples`
   - **Description:**
     ```markdown
     ## What's New in v0.1.1

     Enhanced CLI help text with examples for multi-file operations.

     ### Added
     - Comprehensive examples in `pdftk cat --help`
     - Multi-file operation examples (A1-3 B5 B7)
     - Examples with rotation, even/odd qualifiers
     - Test suite for multi-PDF operations

     ### Documentation
     - Clarified space-separated page ranges
     - Added visual examples for combining files

     Full changelog: [CHANGELOG.md](https://github.com/frankieliu/pdftk/blob/main/CHANGELOG.md)
     ```
3. Attach dist files (optional):
   - `dist/pdftk_python-0.1.1-py3-none-any.whl`
   - `dist/pdftk_python-0.1.1.tar.gz`
4. Click "Publish release"

### Step 9: Verify Update

```bash
# Wait a few minutes for PyPI to process

# In a new terminal/environment, update the package
pip install --upgrade pdftk-python

# Or with uv
uv tool upgrade pdftk-python

# Verify version
pdftk --version  # Should show 0.1.1

# Test new help
pdftk cat --help  # Should show examples
```

### Step 10: Update Local Development Install

```bash
# If you have editable install, no action needed (already pointing to source)
# If you installed from PyPI:
uv tool upgrade pdftk-python

# Or force reinstall editable
uv tool install --force --editable ~/Library/CloudStorage/Box-Box/Work/pdftk
```

## Authentication

### Using API Tokens (Recommended)

1. Generate token at: https://pypi.org/manage/account/token/
2. Create/edit `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-YourActualTokenHere
   ```
3. Permissions: `chmod 600 ~/.pypirc`

### Using Username/Password

When prompted:
```
Enter your username: your-pypi-username
Enter your password: your-pypi-password
```

## Troubleshooting

### "File already exists"
- You can't re-upload the same version
- Bump version number and rebuild
- Each version is permanent on PyPI

### "Invalid distribution"
- Check version in `pyproject.toml`
- Ensure all files are committed
- Rebuild: `rm -rf dist/ && python -m build`

### "Authentication failed"
- Check API token is correct
- Verify `~/.pypirc` format
- Try interactive authentication: `python -m twine upload dist/*` (without config)

### Package not updating
- PyPI can take a few minutes to update
- Clear pip cache: `pip cache purge`
- Use `--no-cache-dir`: `pip install --upgrade --no-cache-dir pdftk-python`

## Complete Example Workflow

Here's the complete workflow for this specific update:

```bash
# 1. Edit version
# Edit pyproject.toml: version = "0.1.1"

# 2. Update changelog
# Edit CHANGELOG.md with new version section

# 3. Commit
git add pyproject.toml CHANGELOG.md src/pdftk/cli.py
git commit -m "v0.1.1: Add CLI help examples for multi-file operations"
git push origin main

# 4. Clean and build
rm -rf dist/ build/ *.egg-info src/*.egg-info
uv run python -m build

# 5. Verify build
ls -lh dist/

# 6. Upload to PyPI
uv run python -m twine upload dist/*

# 7. Create GitHub release (via web UI)
# https://github.com/frankieliu/pdftk/releases/new

# 8. Verify
pip install --upgrade pdftk-python
pdftk --version
pdftk cat --help
```

## Best Practices

1. **Test before publishing**
   - Run all tests: `uv run pytest tests/ -v`
   - Check code quality: `uv run black . && uv run flake8`
   - Test install locally before PyPI

2. **Semantic versioning**
   - Patch (0.0.X): Fixes, docs, non-breaking changes
   - Minor (0.X.0): New features, backwards-compatible
   - Major (X.0.0): Breaking changes

3. **Changelog discipline**
   - Always update CHANGELOG.md
   - Follow Keep a Changelog format
   - Be clear about breaking changes

4. **Git workflow**
   - Commit before building
   - Tag releases: `git tag v0.1.1`
   - Push tags: `git push origin --tags`

5. **Verification**
   - Wait for CI to pass
   - Test fresh install
   - Check PyPI project page

## Current Status

**Current Published Version:** 0.1.0
**Pending Changes:** CLI help examples
**Suggested Next Version:** 0.1.1

**Changes to publish:**
- Enhanced `pdftk cat --help` with examples
- Multi-file operation examples
- Generated test PDFs and verification

## Quick Commands

```bash
# Build
uv run python -m build

# Upload
uv run python -m twine upload dist/*

# Install build/twine if needed
uv pip install build twine

# Upgrade after publishing
uv tool upgrade pdftk-python
```

## See Also

- [PUBLISHING.md](PUBLISHING.md) - Initial publishing guide
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [POST_PUBLICATION_STATUS.md](POST_PUBLICATION_STATUS.md) - Publication status
