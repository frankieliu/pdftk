# GitHub Release v0.1.1

## Release Information

**Tag:** `v0.1.1`
**Title:** `v0.1.1 - CLI Help Examples`
**Target:** `main` branch

## Release Description

```markdown
## What's New in v0.1.1

Enhanced CLI help text with comprehensive examples for multi-file operations.

### Added
- **Comprehensive examples** in `pdftk cat --help` showing real-world usage patterns
- **Multi-file operation examples**: Extract pages from multiple PDFs (e.g., `A1-3 B5 B7`)
- **Examples with rotation**: Apply rotation during page extraction (e.g., `A1-3east`)
- **Even/odd qualifier examples**: Extract even or odd pages (e.g., `A1-10even B5-10odd`)
- **Test suite for multi-PDF operations** with labeled test PDFs for verification
- **UV Tool Management Guide** (UV_TOOL_GUIDE.md) - Complete guide for uv tool installation and updates
- **PyPI Update Guide** (UPDATING_PYPI.md) - Step-by-step guide for publishing updates

### Changed
- Improved `--ranges` help text to clarify **space-separated syntax** (not comma-separated)
- Enhanced documentation for combining multiple files with handles
- Updated `.gitignore` to exclude generated test PDFs

### Fixed
- **Clarified page range syntax**: Use `B5 B7` not `B5,7` (spaces, not commas)

### Example Usage

```bash
# Extract pages 1-3 from a.pdf and pages 5, 7 from b.pdf
pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-3 B5 B7

# Multiple ranges from each file
pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-3 A10 B5 B7 B8-10

# With rotation (pages 1-3 from A rotated 90° clockwise)
pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-3east B5 B7

# With even/odd qualifiers
pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-10even B5-10odd
```

### Installation

```bash
# Install from PyPI
pip install pdftk-python

# Or with uv
uv tool install pdftk-python

# Upgrade existing installation
pip install --upgrade pdftk-python
# or
uv tool upgrade pdftk-python
```

### Documentation
- Full changelog: [CHANGELOG.md](https://github.com/frankieliu/pdftk/blob/main/CHANGELOG.md)
- UV tool guide: [UV_TOOL_GUIDE.md](https://github.com/frankieliu/pdftk/blob/main/UV_TOOL_GUIDE.md)
- PyPI update guide: [UPDATING_PYPI.md](https://github.com/frankieliu/pdftk/blob/main/UPDATING_PYPI.md)

### Links
- **PyPI**: https://pypi.org/project/pdftk-python/
- **GitHub**: https://github.com/frankieliu/pdftk
- **Issues**: https://github.com/frankieliu/pdftk/issues

---

**Full Changelog**: https://github.com/frankieliu/pdftk/compare/v0.1.0...v0.1.1
```

## Files to Attach (Optional)

- `dist/pdftk_python-0.1.1-py3-none-any.whl`
- `dist/pdftk_python-0.1.1.tar.gz`

## Steps to Create Release

1. Go to: https://github.com/frankieliu/pdftk/releases/new
2. Click "Choose a tag" and type: `v0.1.1` (will create on publish)
3. Set Release title: `v0.1.1 - CLI Help Examples`
4. Copy the Release Description from above into the description field
5. Optionally attach the wheel and tar.gz files from dist/
6. Click "Publish release"
