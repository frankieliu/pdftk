# pdftk-python

[![CI](https://github.com/frankieliu/pdftk/actions/workflows/ci.yml/badge.svg)](https://github.com/frankieliu/pdftk/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python implementation of pdftk (PDF Toolkit) for manipulating PDF documents from the command line.

## Status

**Beta**: Core page manipulation operations are complete and fully tested. All basic pdftk functionality for burst, cat, rotate, and shuffle is working.

**Test Coverage**: 80 tests passing (39 parser + 24 core + 17 utils)

## Features

### Implemented ✅

- ✅ **burst** - Split PDF into individual page files
- ✅ **cat** - Concatenate/merge PDFs with page ranges and rotation
- ✅ **rotate** - Rotate specific pages
- ✅ **shuffle** - Collate pages from multiple inputs
- ✅ **Page range parser** - Full pdftk-style page range syntax

### Future Phases

- **Watermark/stamp operations** - Apply backgrounds and overlays
- **Form operations** - Fill forms, extract form data
- **Metadata operations** - Extract/update PDF metadata
- **Security operations** - Encrypt PDFs, set permissions

## Installation

### From Source

```bash
cd pdftk
pip install -e .
```

### Using uv (recommended)

```bash
cd pdftk
uv sync
```

## Quick Start

### Command Line

```bash
# Split PDF into individual pages
pdftk document.pdf burst

# Extract pages 1-5 from a PDF
pdftk cat input.pdf -o output.pdf -r 1-5

# Merge two PDFs
pdftk cat file1.pdf file2.pdf -o merged.pdf

# Merge with page selection
pdftk cat A=in1.pdf B=in2.pdf -o out.pdf -r A1-10 B5-15

# Rotate pages
pdftk rotate input.pdf -o output.pdf -r 1east 5-10south

# Shuffle (collate) pages from multiple files
pdftk shuffle A=front.pdf B=back.pdf -o book.pdf -r A Bend-1
```

### Python API

```python
from pathlib import Path
from pdftk.core import burst, cat, rotate, shuffle

# Burst: Split PDF into pages
burst(Path('document.pdf'), output_dir=Path('pages/'))

# Cat: Extract and merge pages
cat(
    {'A': Path('input.pdf')},
    ['1-5', '10-15'],
    Path('output.pdf')
)

# Rotate: Rotate specific pages
rotate(
    Path('input.pdf'),
    ['1east', '5-10south'],
    Path('output.pdf')
)

# Shuffle: Interleave pages
shuffle(
    {'A': Path('front.pdf'), 'B': Path('back.pdf')},
    ['A', 'Bend-1'],
    Path('book.pdf')
)
```

## Usage

### burst - Split PDF into Individual Pages

Split a PDF into individual page files:

```bash
# Default naming (pg_0001.pdf, pg_0002.pdf, etc.)
pdftk burst document.pdf

# Custom output pattern
pdftk burst document.pdf -p page_%02d.pdf

# Output to specific directory
pdftk burst document.pdf -d output/pages/

# Combined
pdftk burst document.pdf -p page_%03d.pdf -d ./split_pages/
```

**Output pattern** uses printf-style format:
- `%d` - Page number
- `%02d` - Page number, zero-padded to 2 digits
- `%04d` - Page number, zero-padded to 4 digits

### cat - Concatenate/Merge PDFs

The `cat` operation supports powerful page range syntax:

```python
from pathlib import Path
from pdftk.core import cat

# Merge all pages from multiple PDFs
cat(
    {'A': Path('file1.pdf'), 'B': Path('file2.pdf')},
    [],  # Empty list = merge all
    Path('merged.pdf')
)

# Extract specific pages
cat(
    {'A': Path('input.pdf')},
    ['1-5', '10-15'],
    Path('subset.pdf')
)

# Reverse pages
cat(
    {'A': Path('input.pdf')},
    ['10-1'],  # Pages in reverse order
    Path('reversed.pdf')
)

# Extract even/odd pages
cat(
    {'A': Path('input.pdf')},
    ['1-10even'],  # Pages 2, 4, 6, 8, 10
    Path('even_pages.pdf')
)

cat(
    {'A': Path('input.pdf')},
    ['1-10odd'],  # Pages 1, 3, 5, 7, 9
    Path('odd_pages.pdf')
)

# Rotate pages during extraction
cat(
    {'A': Path('input.pdf')},
    ['1-5east'],  # Pages 1-5 rotated 90° clockwise
    Path('rotated.pdf')
)

# Complex combinations
cat(
    {'A': Path('in1.pdf'), 'B': Path('in2.pdf')},
    ['A1-10east', 'B5-20odd', 'Aend'],
    Path('complex.pdf')
)
```

### rotate - Rotate Specific Pages

Rotate specific pages while keeping others unchanged:

```python
from pathlib import Path
from pdftk.core import rotate

# Rotate first page 90° clockwise
rotate(
    Path('input.pdf'),
    ['1east'],
    Path('output.pdf')
)

# Rotate multiple ranges with different rotations
rotate(
    Path('input.pdf'),
    ['1-5south', '10-20east'],  # Pages 1-5: 180°, Pages 10-20: 90°
    Path('output.pdf')
)

# All rotation directions available
rotate(
    Path('input.pdf'),
    ['1north'],  # 0° (no rotation)
    Path('output.pdf')
)

rotate(
    Path('input.pdf'),
    ['1east'],  # 90° clockwise
    Path('output.pdf')
)

rotate(
    Path('input.pdf'),
    ['1south'],  # 180°
    Path('output.pdf')
)

rotate(
    Path('input.pdf'),
    ['1west'],  # 270° clockwise (90° counter-clockwise)
    Path('output.pdf')
)
```

### shuffle - Collate Pages

Interleave pages from multiple PDFs in round-robin fashion:

```python
from pathlib import Path
from pdftk.core import shuffle

# Interleave two PDFs page-by-page
# Result: A1, B1, A2, B2, A3, B3, ...
shuffle(
    {'A': Path('front.pdf'), 'B': Path('back.pdf')},
    ['A', 'B'],
    Path('interleaved.pdf')
)

# Perfect binding: front pages + back pages in reverse
# Result: A1, B-last, A2, B-second-to-last, ...
shuffle(
    {'A': Path('front.pdf'), 'B': Path('back.pdf')},
    ['A', 'Bend-1'],
    Path('book.pdf')
)

# Shuffle specific page ranges
shuffle(
    {'A': Path('a.pdf'), 'B': Path('b.pdf')},
    ['A1-10', 'B1-10'],
    Path('shuffled.pdf')
)
```

## Page Range Syntax

The page range parser supports pdftk's powerful syntax:

### Basic Ranges
- `1-5` - Pages 1 through 5
- `10-20` - Pages 10 through 20
- `5` - Single page 5
- `10-1` - Pages 10 through 1 in reverse

### Special Keywords
- `end` - Last page of document
- `1-end` - All pages from 1 to end
- `5-end` - Pages 5 to end
- `r1` - Last page (reverse numbering)
- `r2` - Second-to-last page
- `rend` - First page
- `r3-r1` - Last 3 pages

### Qualifiers
- `1-10even` - Even pages: 2, 4, 6, 8, 10
- `1-10odd` - Odd pages: 1, 3, 5, 7, 9
- `10-1even` - Reverse even pages: 10, 8, 6, 4, 2

### Rotation
- `1-5north` - Pages 1-5, no rotation (0°)
- `1-5east` - Pages 1-5, rotated 90° clockwise
- `1-5south` - Pages 1-5, rotated 180°
- `1-5west` - Pages 1-5, rotated 270° clockwise
- `1-5left` - Pages 1-5, rotated 90° counter-clockwise
- `1-5right` - Pages 1-5, rotated 90° clockwise
- `1-5down` - Pages 1-5, rotated 180°

### Handle-Based References
```python
# When using multiple input files with handles:
handles = {
    'A': Path('file1.pdf'),
    'B': Path('file2.pdf')
}

# A - All pages from file A
# A1-10 - Pages 1-10 from file A
# Bend-1 - All pages from file B in reverse
# B5-20odd - Odd pages 5-20 from file B
# A1-10east B5-20odd - Combined ranges
```

### Complex Examples
```python
# Extract even pages, then odd pages in reverse, then first 5 rotated
cat(
    {'A': Path('input.pdf')},
    ['1-10even', '10-1odd', '1-5east'],
    Path('complex.pdf')
)

# Interleave files with rotation
shuffle(
    {'A': Path('a.pdf'), 'B': Path('b.pdf')},
    ['A1-10east', 'B1-10'],
    Path('shuffled.pdf')
)
```

## Real-World Examples

### Split a Document for Review
```bash
pdftk burst report.pdf -d ./review_pages/
# Creates review_pages/pg_0001.pdf, review_pages/pg_0002.pdf, ...
```

### Extract Specific Chapters
```python
# Extract pages 10-25 and 50-75
cat(
    {'A': Path('book.pdf')},
    ['10-25', '50-75'],
    Path('chapters.pdf')
)
```

### Remove Pages
```python
# Remove pages 5-10 (extract everything else)
cat(
    {'A': Path('document.pdf')},
    ['1-4', '11-end'],
    Path('without_pages_5-10.pdf')
)
```

### Rotate Landscape Pages
```python
# Rotate pages 3, 7, and 12 that are landscape
rotate(
    Path('document.pdf'),
    ['3east', '7east', '12east'],
    Path('corrected.pdf')
)
```

### Assemble Scanned Book
```python
# Front pages scanned normally, back pages scanned in reverse
shuffle(
    {'A': Path('front_scans.pdf'), 'B': Path('back_scans.pdf')},
    ['A', 'Bend-1'],
    Path('complete_book.pdf')
)
```

### Create Booklet
```python
# Rearrange pages for booklet printing (4 pages per sheet)
# Page order: 8,1,2,7,6,3,4,5 for an 8-page document
cat(
    {'A': Path('document.pdf')},
    ['8', '1', '2', '7', '6', '3', '4', '5'],
    Path('booklet.pdf')
)
```

## Development

### Project Structure

```
pdftk/
├── src/
│   └── pdftk/
│       ├── __init__.py      # Package initialization
│       ├── __main__.py      # CLI entry point
│       ├── cli.py           # Argument parsing
│       ├── core.py          # Core PDF operations ✅
│       ├── parser.py        # Page range parser ✅
│       └── utils.py         # Helper functions
├── tests/
│   ├── fixtures/            # Test PDF files
│   ├── test_parser.py       # Parser tests (39 tests) ✅
│   ├── test_core.py         # Core operation tests (24 tests) ✅
│   └── test_utils.py        # Utility tests (17 tests) ✅
├── demo.py                  # Demonstration script
├── pyproject.toml           # Project configuration
├── IMPLEMENTATION.md        # Detailed implementation plan
├── CONTEXT.md               # Handoff documentation
├── pdftk.md                 # Full pdftk documentation
└── README.md                # This file
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_parser.py -v

# Run with coverage
uv run pytest tests/ --cov=pdftk
```

### Running the Demo

```bash
# Demonstrates all 8 operations with real PDFs
uv run python demo.py
```

### Running from Source

```bash
# Using Python module (recommended for now)
uv run python -m pdftk document.pdf burst

# Or import directly in Python
from pdftk.core import burst, cat, rotate, shuffle
```

## Implementation Status

### ✅ Phase 1: Basic Operations (Complete)

1. ✅ **Foundation** - Project structure, pypdf integration
2. ✅ **Sprint 1** - burst operation, CLI framework
3. ✅ **Sprint 2** - Page range parser (full pdftk syntax)
4. ✅ **Sprint 3** - cat, rotate, shuffle operations
5. ⏳ **Sprint 4** - Polish, testing, documentation (in progress)

**Test Coverage:**
- 80 tests passing (39 parser + 24 core + 17 utils)
- All page range features: simple ranges, reverse, end/r1, even/odd, rotation, handles
- All operations: burst, cat, rotate, shuffle

### Phase 2: Advanced Features (Future)

- Watermark and stamp operations
- Form filling and data extraction
- Metadata manipulation
- PDF encryption and permissions

## Requirements

- Python 3.9 or higher
- pypdf >= 3.0.0
- reportlab >= 4.0.0 (dev dependency, for creating test PDFs)

## Documentation

- [pdftk.md](pdftk.md) - Complete pdftk command reference
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Detailed sprint-by-sprint implementation plan
- [CONTEXT.md](CONTEXT.md) - Handoff documentation with architecture details

## Differences from Original pdftk

This is a Python reimplementation focused on:
- **Core page manipulation operations** (implemented)
- **Pure Python** - No C/Java dependencies, easy installation
- **Modern Python practices** - Type hints, dataclasses, pytest
- **Gradual feature rollout** - Basic operations first, advanced features later
- **Python API** - Can be used as a library or CLI tool

**Current Limitation:** CLI has argparse limitations with some command structures. Python API is fully functional.

## Performance

Performance is suitable for typical documents (< 1000 pages). For very large PDFs or high-throughput scenarios, consider:
- Using the Python API directly (lower overhead than CLI)
- Switching to pikepdf backend (future enhancement)
- Parallel processing for batch operations

## License

MIT

## Credits

Based on the original [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) by Sid Steward.

Implemented in Python using [pypdf](https://pypdf.readthedocs.io/).
