# pdftk Python - Context & Handoff Documentation

**Last Updated:** 2026-01-02  
**Version:** 0.1.0  
**Current Sprint:** Sprint 1 Complete, Ready for Sprint 2

## Quick Start for New Developer

```bash
# Navigate to project
cd /Users/frankliu/Library/CloudStorage/Box-Box/Work/pdftk

# Install dependencies
pip install -e .
# or
uv sync

# Test the working burst operation
python -m pdftk test.pdf burst

# Run tests (when created)
pytest tests/

# View documentation
cat IMPLEMENTATION.md  # Implementation plan
cat README.md          # User documentation
cat pdftk.md           # Original pdftk reference
```

---

## Project Overview

### What This Is

A Python reimplementation of **pdftk** (PDF Toolkit) as a command-line tool for manipulating PDF documents. This is a **CLI-only** implementation (not a library), focusing on core page manipulation operations first.

### Why This Exists

- Original pdftk requires Java runtime and has complex dependencies
- Need a pure Python solution that's easy to install and use
- Learning project to understand PDF manipulation
- Part of a larger effort (related to Zenith card processing project)

### What's Different from Original pdftk

- **Python-based** (not Java/C++)
- **Gradual rollout** (implementing features in phases)
- **pypdf library** (not iText)
- **Modern Python practices** (type hints, dataclasses, pytest)
- **CLI-only** (library API can be added later)

---

## Current State (Sprint 1 Complete ✅)

### What Works Right Now

1. **burst operation** - Fully functional\!
   ```bash
   pdftk document.pdf burst
   pdftk document.pdf burst --output page_%02d.pdf --output-dir ./pages/
   ```

2. **Project infrastructure**
   - Clean module structure
   - CLI argument parsing with argparse
   - Input file parsing (handles like `A=file.pdf`)
   - Error handling and validation
   - Package installable with pip/uv

### File Structure

```
pdftk/
├── .gitignore              # Git ignore patterns
├── IMPLEMENTATION.md       # Detailed sprint-by-sprint plan
├── CONTEXT.md              # This file - handoff documentation
├── README.md               # User-facing documentation
├── pdftk.md                # Complete pdftk reference (man page style)
├── pyproject.toml          # Project config, dependencies
│
├── src/pdftk/
│   ├── __init__.py         # Package initialization, version
│   ├── __main__.py         # CLI entry point (imports cli.main)
│   ├── cli.py              # Argument parsing (155 lines)
│   ├── core.py             # Core operations (88 lines)
│   └── utils.py            # Helper functions (58 lines)
│
└── tests/
    └── __init__.py         # Test package (empty for now)
```

### Dependencies

**Runtime:**
- `pypdf>=3.0.0` - PDF manipulation library

**Development:**
- `pytest>=7.0.0` - Testing framework
- `black>=23.0.0` - Code formatter
- `flake8>=6.0.0` - Linter

---

## Architecture & Design Patterns

### Key Design Decisions

1. **pypdf over pikepdf**
   - Pure Python (no C dependencies)
   - Already familiar from related Zenith project
   - Sufficient for Phase 1 operations
   - Easier installation and portability

2. **argparse over Click/Typer**
   - Standard library (no extra dependencies)
   - Mature and well-documented
   - Sufficient for our needs

3. **CLI-only (no library API yet)**
   - Simpler to implement
   - Focused scope
   - Can add library API later if needed

4. **Phased implementation**
   - Sprint 1: Foundation + burst ✅
   - Sprint 2: Page range parser (most complex)
   - Sprint 3: cat, rotate, shuffle
   - Sprint 4: Testing and polish

### Code Patterns

#### Input File Parsing

Files can be specified with or without handles:
```python
# Without handles
['file1.pdf', 'file2.pdf']

# With handles (for page range references)
['A=file1.pdf', 'B=file2.pdf']
```

Parsed by `utils.parse_input_files()`:
```python
handles, files = parse_input_files(['A=in1.pdf', 'B=in2.pdf'])
# handles = {'A': Path('in1.pdf'), 'B': Path('in2.pdf')}
# files = [Path('in1.pdf'), Path('in2.pdf')]
```

#### Error Handling

All operations should:
1. Validate inputs (file exists, is PDF)
2. Raise specific exceptions
3. Be caught in `cli.py` and converted to user-friendly messages
4. Exit with appropriate status codes

```python
try:
    operation()
except FileNotFoundError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

#### Operation Signatures

All core operations follow consistent patterns:
```python
# Single input operations
def burst(input_file: Path, output_pattern: str, output_dir: Path) -> int:
    """Returns number of pages processed"""

# Multi-input operations
def cat(input_files: dict[str, Path], page_ranges: list[str], output: Path) -> None:
    """No return value, writes to output"""
```

---

## Code Walkthrough

### src/pdftk/cli.py

**Purpose:** Parse command-line arguments and dispatch to operations

**Key Functions:**
- `create_parser()` - Build argparse parser with subcommands
- `main(args=None)` - Entry point, handles errors

**Structure:**
```python
parser = ArgumentParser()
parser.add_argument('inputs', nargs='+')  # Input files

subparsers = parser.add_subparsers(dest='operation')

# Each operation gets a subparser
burst_parser = subparsers.add_parser('burst')
burst_parser.add_argument('--output', ...)

# Dispatch
if args.operation == 'burst':
    burst(...)
elif args.operation == 'cat':
    cat(...)
```

**Important:**
- Operations are subcommands, not flags
- Input files come before the operation
- Handles error conversion for user-friendly output

### src/pdftk/core.py

**Purpose:** Implement PDF manipulation operations

**Current State:**
- `burst()` - **IMPLEMENTED** ✅
- `cat()` - Stub (raises NotImplementedError)
- `rotate()` - Stub (raises NotImplementedError)
- `shuffle()` - Stub (raises NotImplementedError)

**burst() Implementation:**
```python
def burst(input_file: Path, output_pattern: str = "pg_%04d.pdf", 
          output_dir: Path = None) -> int:
    """Split PDF into individual pages
    
    Key steps:
    1. Create output directory if needed
    2. Read input PDF with PdfReader
    3. For each page:
       - Create new PdfWriter
       - Add single page
       - Write to file with formatted name
    4. Return total page count
    """
```

**Key pypdf APIs used:**
```python
from pypdf import PdfReader, PdfWriter

# Reading
reader = PdfReader(input_file)
pages = reader.pages  # List-like access
total = len(reader.pages)

# Writing
writer = PdfWriter()
writer.add_page(page)
with open(output, 'wb') as f:
    writer.write(f)
```

### src/pdftk/utils.py

**Purpose:** Helper functions for parsing and validation

**Functions:**
- `parse_input_files(inputs)` - Parse handle syntax like `A=file.pdf`
- `validate_pdf_exists(path)` - Check file exists and is PDF

**Usage:**
```python
# Parse inputs
handles, files = parse_input_files(['A=in1.pdf', 'file2.pdf'])

# Validate each file
for file in files:
    validate_pdf_exists(file)  # Raises FileNotFoundError or ValueError
```

---

## What Needs to Be Built Next (Sprint 2)

### The Page Range Parser (CRITICAL COMPONENT)

**File:** `src/pdftk/parser.py` (needs to be created)

**Why It's Critical:**
- Required for `cat`, `rotate`, and `shuffle`
- Most complex part of the project (40% of Phase 1 effort)
- Handles pdftk's powerful but complex page range syntax

### Page Range Syntax Examples

```bash
# Simple ranges
1-5              # Pages 1,2,3,4,5
10-20            # Pages 10-20

# Reverse ranges  
10-1             # Pages 10,9,8,...,1

# Special keywords
1-end            # Page 1 to last page
5-end            # Page 5 to last page
end              # Last page only

# Reverse page numbering
r1               # Last page
r2               # Second-to-last page
rend             # First page
r3-r1            # Last 3 pages

# Qualifiers (even/odd)
1-10even         # Pages 2,4,6,8,10
1-10odd          # Pages 1,3,5,7,9
10-1even         # Pages 10,8,6,4,2 (reverse + even)

# Rotation
1-5east          # Pages 1-5, rotated 90° clockwise
10west           # Page 10, rotated 270° clockwise
1-endsouth       # All pages, rotated 180°

# Handle-based (with multiple input files)
A                # All pages from file A
A1-10            # Pages 1-10 from file A
Bend-1           # All pages from file B, in reverse
B5-20odd         # Odd pages 5-20 from file B

# Combined
A1-10east B5-20odd Awest
```

### Parser Architecture

**Recommended Structure:**
```python
# parser.py

from dataclasses import dataclass
from pypdf import PdfReader
from pathlib import Path

@dataclass
class PageSpec:
    """Specification for pages to extract"""
    handle: str | None      # Handle reference (e.g., 'A', 'B', None)
    pages: list[int]        # Resolved page numbers (1-indexed)
    rotation: int           # Rotation in degrees: 0, 90, 180, 270

class PageRangeParser:
    """Parse pdftk-style page range specifications"""
    
    def __init__(self, readers: dict[str, PdfReader]):
        """Initialize with handle-to-reader mapping
        
        Args:
            readers: {'A': PdfReader('a.pdf'), 'B': PdfReader('b.pdf')}
        """
        self.readers = readers
        
    def parse(self, range_str: str) -> list[PageSpec]:
        """Parse entire page range string
        
        Args:
            range_str: e.g., "A1-10east B5-20odd"
            
        Returns:
            List of PageSpec objects
        """
        # Split by whitespace, parse each part
        parts = range_str.split()
        specs = []
        for part in parts:
            specs.append(self._parse_single(part))
        return specs
        
    def _parse_single(self, part: str) -> PageSpec:
        """Parse single range like 'A1-10east'"""
        # 1. Extract handle (optional): [A-Z]+
        # 2. Extract page spec: number | range | 'end' | 'r' number
        # 3. Extract qualifier (optional): 'even' | 'odd'
        # 4. Extract rotation (optional): 'north' | 'east' | ...
        # 5. Resolve page numbers
        # 6. Apply qualifier filter
        # 7. Return PageSpec
        pass
        
    def _resolve_page_number(self, spec: str, total_pages: int) -> int:
        """Resolve page number (handles 'end', 'r1', etc.)"""
        if spec == 'end':
            return total_pages
        elif spec.startswith('r'):
            if spec == 'rend':
                return 1
            else:
                offset = int(spec[1:])
                return total_pages - offset + 1
        else:
            return int(spec)
            
    def _apply_qualifier(self, pages: list[int], qualifier: str | None) -> list[int]:
        """Apply even/odd filter"""
        if qualifier == 'even':
            return [p for p in pages if p % 2 == 0]
        elif qualifier == 'odd':
            return [p for p in pages if p % 2 == 1]
        else:
            return pages
            
    def _rotation_to_degrees(self, rotation: str | None) -> int:
        """Convert rotation keyword to degrees"""
        rotations = {
            'north': 0, 'east': 90, 'south': 180, 'west': 270,
            'left': -90, 'right': 90, 'down': 180
        }
        return rotations.get(rotation, 0)
```

### Implementation Strategy for Parser

**Step 1: Simple ranges (EASIEST)**
```python
# Test cases
"1-5"     → [1,2,3,4,5]
"10-20"   → [10,11,...,20]
"5"       → [5]
"10-1"    → [10,9,8,...,1]
```

**Step 2: Special keywords**
```python
# Test cases (assume 10-page document)
"end"     → [10]
"1-end"   → [1,2,...,10]
"5-end"   → [5,6,...,10]
```

**Step 3: Reverse page numbering**
```python
# Test cases (assume 10-page document)
"r1"      → [10]
"r2"      → [9]
"rend"    → [1]
"r3-r1"   → [8,9,10]
```

**Step 4: Qualifiers**
```python
# Test cases
"1-10even"   → [2,4,6,8,10]
"1-10odd"    → [1,3,5,7,9]
"10-1even"   → [10,8,6,4,2]
```

**Step 5: Rotation**
```python
# Test cases
"1-5east"    → PageSpec(pages=[1,2,3,4,5], rotation=90)
"10west"     → PageSpec(pages=[10], rotation=270)
```

**Step 6: Handles**
```python
# Test cases (with A=10 pages, B=20 pages)
"A"          → All pages from A
"A1-5"       → Pages 1-5 from A
"Bend-1"     → All pages from B in reverse
"A1-10 B5-10"→ Pages 1-10 from A, then 5-10 from B
```

### Testing Strategy

**Create:** `tests/test_parser.py`

```python
import pytest
from pdftk.parser import PageRangeParser, PageSpec
from pypdf import PdfReader

@pytest.fixture
def mock_readers():
    """Create mock PDF readers for testing"""
    # You'll need test PDF files in tests/fixtures/
    return {
        'A': PdfReader('tests/fixtures/10page.pdf'),
        'B': PdfReader('tests/fixtures/20page.pdf')
    }

def test_simple_range(mock_readers):
    parser = PageRangeParser(mock_readers)
    specs = parser.parse("1-5")
    assert len(specs) == 1
    assert specs[0].pages == [1,2,3,4,5]
    assert specs[0].rotation == 0

def test_reverse_range(mock_readers):
    parser = PageRangeParser(mock_readers)
    specs = parser.parse("10-1")
    assert specs[0].pages == [10,9,8,7,6,5,4,3,2,1]

def test_even_qualifier(mock_readers):
    parser = PageRangeParser(mock_readers)
    specs = parser.parse("1-10even")
    assert specs[0].pages == [2,4,6,8,10]

def test_end_keyword(mock_readers):
    parser = PageRangeParser(mock_readers)
    # Assumes mock_readers['A'] has 10 pages
    specs = parser.parse("5-end")
    assert specs[0].pages == [5,6,7,8,9,10]

def test_rotation(mock_readers):
    parser = PageRangeParser(mock_readers)
    specs = parser.parse("1-5east")
    assert specs[0].rotation == 90

def test_handle_based(mock_readers):
    parser = PageRangeParser(mock_readers)
    specs = parser.parse("A1-5")
    assert specs[0].handle == 'A'
    assert specs[0].pages == [1,2,3,4,5]

def test_combined(mock_readers):
    parser = PageRangeParser(mock_readers)
    specs = parser.parse("A1-10east B5-20odd")
    assert len(specs) == 2
    assert specs[0].handle == 'A'
    assert specs[0].rotation == 90
    assert specs[1].handle == 'B'
    assert specs[1].pages == [5,7,9,11,13,15,17,19]
```

---

## How to Use the Parser in Operations

### cat operation

```python
def cat(input_files: dict[str, Path], 
        page_ranges: list[str], 
        output: Path) -> None:
    """Concatenate PDFs with page ranges"""
    
    # 1. Load all input PDFs
    readers = {}
    for handle, filepath in input_files.items():
        readers[handle] = PdfReader(filepath)
    
    # Also load files without handles (if any)
    # Assign default handle or allow no-handle syntax
    
    # 2. Parse page ranges
    parser = PageRangeParser(readers)
    all_specs = []
    for range_str in page_ranges:
        all_specs.extend(parser.parse(range_str))
    
    # 3. Extract pages and build output
    writer = PdfWriter()
    for spec in all_specs:
        reader = readers[spec.handle]
        for page_num in spec.pages:
            page = reader.pages[page_num - 1]  # Convert 1-indexed to 0-indexed
            if spec.rotation \!= 0:
                page.rotate(spec.rotation)
            writer.add_page(page)
    
    # 4. Write output
    with open(output, 'wb') as f:
        writer.write(f)
```

### rotate operation

```python
def rotate(input_file: Path, 
           page_ranges: list[str], 
           output: Path) -> None:
    """Rotate specific pages"""
    
    # 1. Load input PDF
    reader = PdfReader(input_file)
    
    # 2. Parse rotation specifications
    # (For rotate, we only care about which pages and rotation amount)
    parser = PageRangeParser({'': reader})  # No handle needed
    specs = []
    for range_str in page_ranges:
        specs.extend(parser.parse(range_str))
    
    # 3. Build rotation map: page_num → rotation_degrees
    rotation_map = {}
    for spec in specs:
        for page_num in spec.pages:
            rotation_map[page_num] = spec.rotation
    
    # 4. Process all pages
    writer = PdfWriter()
    for i, page in enumerate(reader.pages, start=1):
        if i in rotation_map:
            page.rotate(rotation_map[i])
        writer.add_page(page)
    
    # 5. Write output
    with open(output, 'wb') as f:
        writer.write(f)
```

---

## pypdf API Reference

### Reading PDFs

```python
from pypdf import PdfReader

reader = PdfReader('input.pdf')

# Get page count
num_pages = len(reader.pages)

# Access pages (0-indexed)
page = reader.pages[0]  # First page
page = reader.pages[-1]  # Last page

# Iterate pages
for page in reader.pages:
    # process page
    pass

# Get metadata
metadata = reader.metadata
# Returns: {'/Title': 'My PDF', '/Author': 'John Doe', ...}

# Get bookmarks (outlines)
outlines = reader.outline
```

### Writing PDFs

```python
from pypdf import PdfWriter

writer = PdfWriter()

# Add pages from reader
writer.add_page(reader.pages[0])

# Add multiple pages
for page in reader.pages:
    writer.add_page(page)

# Clone page with modifications
page = reader.pages[0]
page.rotate(90)  # Rotate 90° clockwise
writer.add_page(page)

# Write to file
with open('output.pdf', 'wb') as f:
    writer.write(f)

# Add metadata
writer.add_metadata({
    '/Title': 'My Output PDF',
    '/Author': 'pdftk-python'
})
```

### Page Rotation

```python
# Rotation methods
page.rotate(90)    # Rotate 90° clockwise
page.rotate(180)   # Rotate 180°
page.rotate(270)   # Rotate 270° clockwise (= 90° counter-clockwise)
page.rotate(-90)   # Rotate 90° counter-clockwise

# Rotations are cumulative
page.rotate(90)
page.rotate(90)   # Total: 180°

# Get current rotation
rotation = page.rotation  # Returns 0, 90, 180, or 270
```

### Page Merging/Overlays (for future stamp/watermark operations)

```python
# Merge two pages (overlay)
page1 = reader1.pages[0]
page2 = reader2.pages[0]

page1.merge_page(page2)  # page2 overlaid on top of page1
writer.add_page(page1)
```

---

## Common Patterns and Gotchas

### 1. Page Numbering: 1-indexed vs 0-indexed

**pdftk uses 1-indexed pages** (first page is 1)
**pypdf uses 0-indexed** (first page is 0)

Always convert:
```python
# User specifies page 5 (1-indexed)
user_page = 5
pypdf_page = user_page - 1
page = reader.pages[pypdf_page]
```

### 2. Handle Resolution

When no handle is specified, use the first (or only) input file:
```python
# User: pdftk input.pdf cat 1-5 output out.pdf
# No handle specified, use first file

if not spec.handle:
    # Use first file in files list
    reader = readers[list(readers.keys())[0]]
```

### 3. Rotation is Cumulative

Don't rotate the same page object multiple times:
```python
# WRONG: page gets rotated twice
page = reader.pages[0]
page.rotate(90)
writer.add_page(page)
page.rotate(90)  # DON'T DO THIS
writer.add_page(page)

# RIGHT: Get fresh page each time or clone
page1 = reader.pages[0]
page1.rotate(90)
writer.add_page(page1)

page2 = reader.pages[0]  # Fresh copy
page2.rotate(180)
writer.add_page(page2)
```

### 4. Printf-Style Output Patterns

```python
# User specifies: "page_%02d.pdf"
output_pattern = "page_%02d.pdf"

for i in range(1, 11):
    filename = output_pattern % i
    # page_01.pdf, page_02.pdf, ..., page_10.pdf
```

Format specifiers:
- `%d` - Integer
- `%02d` - Zero-padded to 2 digits
- `%04d` - Zero-padded to 4 digits
- `%3d` - Space-padded to 3 digits

---

## Testing Approach

### Test PDF Fixtures

Create in `tests/fixtures/`:
```bash
tests/fixtures/
├── 1page.pdf       # Single page for basic tests
├── 10page.pdf      # 10 pages for range tests
├── 20page.pdf      # 20 pages for multi-file tests
└── rotated.pdf     # Pre-rotated pages for rotation tests
```

Generate test PDFs:
```python
# Script to create test PDFs
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf(num_pages: int, output: str):
    """Create a test PDF with numbered pages"""
    writer = PdfWriter()
    
    for i in range(1, num_pages + 1):
        # Create page with page number on it
        c = canvas.Canvas(f"/tmp/page{i}.pdf", pagesize=letter)
        c.drawString(100, 400, f"Page {i}")
        c.save()
        
        # Add to writer
        reader = PdfReader(f"/tmp/page{i}.pdf")
        writer.add_page(reader.pages[0])
    
    with open(output, 'wb') as f:
        writer.write(f)

# Create fixtures
create_test_pdf(1, 'tests/fixtures/1page.pdf')
create_test_pdf(10, 'tests/fixtures/10page.pdf')
create_test_pdf(20, 'tests/fixtures/20page.pdf')
```

### Test Categories

1. **Unit Tests** - Individual functions
   - `test_parser.py` - Page range parser
   - `test_utils.py` - Helper functions
   - `test_core.py` - Individual operations

2. **Integration Tests** - End-to-end
   - `test_cli.py` - CLI argument parsing
   - `test_integration.py` - Full command execution

3. **Regression Tests** - Known issues
   - Add tests for any bugs found

---

## Performance Considerations

### Current (Phase 1)

- Focus on **correctness** over performance
- pypdf is fast enough for typical use (documents with <1000 pages)
- Most operations are I/O bound (reading/writing PDFs)

### Future Optimizations (if needed)

1. **Lazy loading** - Don't load all pages into memory
2. **Streaming** - Process pages one at a time for large documents
3. **Parallel processing** - Use multiprocessing for independent operations
4. **pikepdf** - Consider switching for better performance

**Don't optimize prematurely\!** Profile first.

---

## Known Limitations

### Current (v0.1.0)

- Only `burst` operation works
- No encryption support
- No form filling
- No watermark/stamp operations
- No bookmark manipulation
- No attachment handling

### pypdf Limitations

- Slower than pikepdf for very large PDFs (1000+ pages)
- Some edge cases with complex PDFs
- XFA forms not supported
- Some advanced PDF features not implemented

### Design Limitations

- CLI-only (no programmatic API yet)
- No streaming/incremental processing
- Loads entire PDFs into memory

---

## Development Workflow

### Adding a New Feature

1. **Update IMPLEMENTATION.md** with detailed plan
2. **Write tests first** (TDD approach)
3. **Implement feature** incrementally
4. **Run tests** frequently
5. **Update README.md** with usage examples
6. **Manual testing** with real PDFs

### Code Style

- **Type hints** everywhere
- **Docstrings** for all public functions (Google style)
- **Black** for formatting
- **Flake8** for linting
- **Line length:** 100 characters

Example:
```python
def parse_range(range_str: str, total_pages: int) -> list[int]:
    """Parse a page range string into page numbers.
    
    Args:
        range_str: Page range specification (e.g., "1-5", "1-end")
        total_pages: Total number of pages in document
        
    Returns:
        List of page numbers (1-indexed)
        
    Raises:
        ValueError: If range is invalid
        
    Examples:
        >>> parse_range("1-5", 10)
        [1, 2, 3, 4, 5]
        >>> parse_range("5-end", 10)
        [5, 6, 7, 8, 9, 10]
    """
```

### Commit Messages

Follow conventional commits:
```
feat: add page range parser for simple ranges
fix: handle edge case in burst when output dir doesn't exist
docs: update README with rotate examples
test: add tests for even/odd qualifiers
refactor: extract rotation logic to separate function
```

---

## Troubleshooting

### pypdf Installation Issues

```bash
# If pypdf install fails
pip install --upgrade pip
pip install pypdf

# Or use uv
uv pip install pypdf
```

### Import Errors

```bash
# If "No module named 'pdftk'" error
pip install -e .

# Or
python -m pip install -e .
```

### Tests Not Found

```bash
# Make sure you're in project root
cd /Users/frankliu/Library/CloudStorage/Box-Box/Work/pdftk

# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

---

## Resources

### Documentation

- [pypdf docs](https://pypdf.readthedocs.io/) - Primary PDF library
- [argparse tutorial](https://docs.python.org/3/howto/argparse.html) - CLI parsing
- [Original pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) - Reference implementation

### PDF Specifications

- [PDF Reference 1.7](https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/PDF32000_2008.pdf) - Official spec
- [PDF Explained](https://zlib.pub/book/pdf-explained-50mr9uflda6g) - Beginner-friendly book

### Related Projects

- [pikepdf](https://github.com/pikepdf/pikepdf) - Alternative PDF library (faster, requires C++)
- [PyPDF2](https://github.com/py-pdf/pypdf) - Older name for pypdf
- [pdfrw](https://github.com/pmaupin/pdfrw) - Another Python PDF library

---

## Questions & Answers

### Q: Why not use the original pdftk?

A: Original pdftk requires Java runtime and has complex dependencies. This is a learning project and provides a pure Python alternative.

### Q: Why pypdf and not pikepdf?

A: pypdf is pure Python (easier installation), and we're already familiar with it from the Zenith project. pikepdf requires qpdf C++ library which adds complexity.

### Q: Will this be feature-complete with original pdftk?

A: Eventually, yes. We're implementing features in phases, starting with the most commonly used operations.

### Q: Can I use this as a library?

A: Not yet. Phase 1 focuses on CLI. Library API can be added later.

### Q: Why not use Click or Typer for CLI?

A: argparse is sufficient and has no dependencies. We can switch later if needed.

---

## Quick Command Reference

```bash
# Current working commands
pdftk input.pdf burst
pdftk input.pdf burst --output page_%02d.pdf --output-dir ./pages/

# Planned commands (not yet implemented)
pdftk A=in1.pdf B=in2.pdf cat A1-10 B output out.pdf
pdftk input.pdf cat 1-5 10-15 output subset.pdf
pdftk input.pdf cat 1-endeast output rotated.pdf
pdftk input.pdf rotate 1east 5-10south output rotated.pdf
pdftk A=front.pdf B=back.pdf shuffle A Bend-1 output book.pdf
```

---

## Contact & Handoff

**Project Owner:** Frank Liu  
**Started:** 2026-01-02  
**Current Sprint:** Sprint 1 Complete, Ready for Sprint 2  

**Next Developer:** Start with Sprint 2 (Page Range Parser)
- Read IMPLEMENTATION.md for detailed sprint plan
- Create `src/pdftk/parser.py`
- Start with simple ranges, add complexity incrementally
- Write tests as you go

**Critical Files:**
- `IMPLEMENTATION.md` - Sprint-by-sprint plan
- `CONTEXT.md` - This file
- `pdftk.md` - Complete pdftk reference

Good luck\! 🚀
