# pdftk-python

A Python implementation of pdftk (PDF Toolkit) for manipulating PDF documents from the command line.

## Status

**Alpha**: Currently implements `burst` operation. Additional operations (`cat`, `rotate`, `shuffle`) coming soon.

## Features

### Implemented

- ✅ **burst** - Split PDF into individual page files

### Planned (Phase 1)

- ⏳ **cat** - Concatenate/merge PDFs with page ranges and rotation
- ⏳ **rotate** - Rotate specific pages
- ⏳ **shuffle** - Collate pages from multiple inputs

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

## Usage

### burst - Split PDF into Individual Pages

Split a PDF into individual page files:

```bash
# Default naming (pg_0001.pdf, pg_0002.pdf, etc.)
pdftk document.pdf burst

# Custom output pattern
pdftk document.pdf burst --output page_%02d.pdf

# Output to specific directory
pdftk document.pdf burst --output-dir output/pages/

# Combined
pdftk document.pdf burst --output page_%03d.pdf --output-dir ./split_pages/
```

**Output pattern** uses printf-style format:
- `%d` - Page number
- `%02d` - Page number, zero-padded to 2 digits
- `%04d` - Page number, zero-padded to 4 digits

### cat - Concatenate/Merge PDFs (Coming Soon)

```bash
# Merge all PDFs
pdftk file1.pdf file2.pdf file3.pdf cat output merged.pdf

# Extract specific pages
pdftk input.pdf cat 1-5 10-15 output subset.pdf

# With handles for complex operations
pdftk A=in1.pdf B=in2.pdf cat A1-10 B5-20 output combined.pdf

# Rotate pages
pdftk input.pdf cat 1-endeast output rotated.pdf
```

### rotate - Rotate Specific Pages (Coming Soon)

```bash
# Rotate first page 90° clockwise
pdftk input.pdf rotate 1east output rotated.pdf

# Rotate multiple page ranges
pdftk input.pdf rotate 1-5south 10-20east output rotated.pdf
```

### shuffle - Collate Pages (Coming Soon)

```bash
# Interleave two PDFs (perfect binding)
pdftk A=front.pdf B=back.pdf shuffle A Bend-1 output book.pdf
```

## Examples

### Split a document for review

```bash
pdftk report.pdf burst --output-dir ./review_pages/
# Creates review_pages/pg_0001.pdf, review_pages/pg_0002.pdf, ...
```

### Extract a single page

```bash
# Using burst with a single page PDF (coming soon with cat)
pdftk document.pdf cat 5 output page5.pdf  # Future feature
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
│       ├── core.py          # Core PDF operations
│       ├── parser.py        # Page range parser (planned)
│       └── utils.py         # Helper functions
├── tests/
│   └── test_*.py           # Unit tests
├── pyproject.toml          # Project configuration
├── pdftk.md                # Full pdftk documentation
└── README.md               # This file
```

### Running Tests

```bash
pytest tests/
```

### Running from Source

```bash
# Using Python module
python -m pdftk document.pdf burst

# After installation
pdftk document.pdf burst
```

## Implementation Plan

The project follows a phased approach:

### Phase 1: Basic Operations (Current)

1. ✅ **Foundation** - Project structure, pypdf integration
2. ✅ **burst** - Simple page splitting (implemented)
3. ⏳ **Page Range Parser** - Complex syntax for page selection
4. ⏳ **cat** - Concatenation with page ranges and rotation
5. ⏳ **rotate** - Selective page rotation
6. ⏳ **shuffle** - Page collation

### Phase 2: Advanced Features (Future)

- Watermark and stamp operations
- Form filling and data extraction
- Metadata manipulation
- PDF encryption and permissions

## Complexity Assessment

Based on implementation analysis:

- **Easy**: burst (✅ complete), basic rotate
- **Medium**: shuffle, CLI parsing, handle resolution
- **Hard**: Page range parser, cat with all features, rotation directions

## Requirements

- Python 3.9 or higher
- pypdf >= 3.0.0

## Documentation

See [pdftk.md](pdftk.md) for complete pdftk command reference and syntax documentation.

## Differences from Original pdftk

This is a Python reimplementation focused on:
- Core page manipulation operations
- Pure Python (no C dependencies)
- Modern Python practices
- Gradual feature rollout

Not all original pdftk features are implemented yet. See the roadmap above for planned features.

## License

MIT

## Credits

Based on the original [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) by Sid Steward.
