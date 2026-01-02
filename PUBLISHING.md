# Publishing to PyPI - Next Steps

This document outlines the remaining steps to publish pdftk-python to PyPI.

## Prerequisites

All preparation is complete:
- ✅ pyproject.toml configured with metadata
- ✅ LICENSE file (MIT)
- ✅ CHANGELOG.md
- ✅ README.md with badges
- ✅ CI/CD workflow (.github/workflows/ci.yml)
- ✅ All tests passing (80/80)

## Step 1: Install Build Tools

```bash
# In the project directory
uv pip install build twine
```

## Step 2: Build Distribution Packages

```bash
# Clean any previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build

# This creates:
# - dist/pdftk_python-0.1.0.tar.gz (source distribution)
# - dist/pdftk_python-0.1.0-py3-none-any.whl (wheel)
```

## Step 3: Test the Package Locally

```bash
# Create a test virtual environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install from local wheel
pip install dist/pdftk_python-0.1.0-py3-none-any.whl

# Test the installation
pdftk --help
pdftk --version

# Test basic operations
pdftk burst tests/fixtures/10page.pdf
pdftk cat tests/fixtures/10page.pdf -o test.pdf -r 1-5

# Deactivate and cleanup
deactivate
rm -rf test-env
```

## Step 4: Upload to Test PyPI (Optional but Recommended)

```bash
# Register for Test PyPI account: https://test.pypi.org/account/register/

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ pdftk-python
```

## Step 5: Upload to Production PyPI

```bash
# Register for PyPI account: https://pypi.org/account/register/

# Upload to production PyPI
python -m twine upload dist/*

# You'll be prompted for username and password
# Or configure ~/.pypirc for authentication
```

## Step 6: Create GitHub Release

1. Go to https://github.com/frankieliu/pdftk/releases
2. Click "Create a new release"
3. Tag: `v0.1.0`
4. Title: `v0.1.0 - Initial Release`
5. Description: Copy from CHANGELOG.md
6. Attach the dist/ files
7. Publish release

## Step 7: Verify Installation

```bash
# Fresh install from PyPI
pip install pdftk-python

# Test
pdftk --version
pdftk --help
```

## Step 8: Update README Badge

After publishing, add PyPI badges to README.md:

```markdown
[![PyPI version](https://badge.fury.io/py/pdftk-python.svg)](https://badge.fury.io/py/pdftk-python)
[![PyPI downloads](https://img.shields.io/pypi/dm/pdftk-python.svg)](https://pypi.org/project/pdftk-python/)
```

## Troubleshooting

### Authentication
- Use API tokens instead of passwords for security
- Generate token at: https://pypi.org/manage/account/token/
- Configure in ~/.pypirc:
  ```ini
  [pypi]
  username = __token__
  password = pypi-YourTokenHere
  ```

### Build Errors
- Ensure setuptools is up to date: `pip install --upgrade setuptools wheel`
- Check MANIFEST.in includes all necessary files
- Verify pyproject.toml syntax

### Upload Errors
- Ensure version number is unique (can't re-upload same version)
- Check package name isn't already taken
- Verify all required metadata is present

## Post-Publication

1. Announce on social media (see ANNOUNCEMENT.md)
2. Monitor GitHub Issues for user feedback
3. Watch PyPI download stats
4. Plan next release (Phase 2 features)
