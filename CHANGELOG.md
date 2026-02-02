# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-02-02

### Added
- Enhanced CLI help text for `cat` operation with comprehensive examples
- Examples showing multi-file operations with different page ranges
- Examples demonstrating space-separated range syntax (A1-3 B5 B7)
- Examples with rotation (A1-3east) and even/odd qualifiers
- Test suite for multi-PDF operations with labeled test PDFs
- UV tool management guide (UV_TOOL_GUIDE.md)
- PyPI update guide (UPDATING_PYPI.md)

### Changed
- Improved `--ranges` help text to clarify space-separated syntax
- Enhanced documentation for combining multiple files with handles

### Fixed
- Clarified that page ranges use spaces, not commas (B5 B7, not B5,7)

## [0.1.0] - 2026-01-02

### Added
- Initial release
- Core PDF operations:
  - `burst` - Split PDF into individual page files
  - `cat` - Concatenate/merge PDFs with page ranges and rotation
  - `rotate` - Rotate specific pages
  - `shuffle` - Collate pages from multiple inputs
- Comprehensive page range parser supporting:
  - Simple ranges (1-5, 10-20)
  - Reverse ranges (10-1)
  - Special keywords (end, r1, rend)
  - Qualifiers (even, odd)
  - Rotation (north, east, south, west, left, right, down)
  - Handle-based file references (A=file.pdf)
- Python-friendly CLI with argparse
- Comprehensive test suite (80 tests)
- Full documentation with examples
- Code quality tooling (black, flake8, mypy)

### Status
- Beta release
- Production-ready for basic PDF manipulation

[0.1.0]: https://github.com/frankieliu/pdftk/releases/tag/v0.1.0
