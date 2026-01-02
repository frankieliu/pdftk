# pdftk Python Implementation Plan

## Project Overview

**Goal:** Create a command-line pdftk clone in Python focusing on core page manipulation operations

**Status:** Sprint 1 Complete ✅

**Current Version:** 0.1.0

## Implementation Phases

### ✅ Sprint 1: Foundation (COMPLETED)

**Status:** Complete

**Delivered:**
- [x] Project structure (`src/pdftk/`, `tests/`)
- [x] `pyproject.toml` with pypdf dependency
- [x] `__init__.py`, `__main__.py` - Package and entry point
- [x] `cli.py` - Argument parsing with argparse
- [x] `utils.py` - Helper functions (input parsing, validation)
- [x] `core.py` - Core operations module
- [x] `burst` operation - Fully functional
- [x] `README.md` - Documentation
- [x] CLI registered as `pdftk` command

**Working Commands:**
```bash
pdftk document.pdf burst
pdftk document.pdf burst --output page_%02d.pdf --output-dir ./pages/
```

---

### ✅ Sprint 2: Page Range Parser (COMPLETED)

**Goal:** Implement the complex page range parser that unlocks cat, rotate, and shuffle operations

**Complexity:** HIGH (40% of Phase 1 effort)

**Status:** Complete

#### 2.1 Parser Implementation

**File:** `src/pdftk/parser.py`

**Classes:**
```python
@dataclass
class PageSpec:
    """Specification for a single page or range of pages"""
    handle: str | None      # Handle reference (e.g., 'A', 'B')
    pages: list[int]        # Resolved page numbers (1-indexed)
    rotation: int           # Rotation in degrees: 0, 90, 180, 270

class PageRangeParser:
    """Parse pdftk-style page range specifications"""
    
    def __init__(self, handles: dict[str, PdfReader]):
        """Initialize with handle-to-reader mapping"""
    
    def parse(self, range_str: str) -> list[PageSpec]:
        """Parse a page range string into PageSpec objects"""
    
    def parse_single_range(self, range_str: str) -> PageSpec:
        """Parse a single range like 'A1-10east' or '5-20odd'"""
```

#### 2.2 Syntax Support (Implementation Order)

1. **Simple Ranges** (Easy)
   - `1-5` → pages [1, 2, 3, 4, 5]
   - `10-20` → pages [10, 11, ..., 20]
   - `5` → page [5]

2. **Reverse Ranges** (Easy)
   - `10-1` → pages [10, 9, 8, ..., 1]

3. **Special Keywords** (Medium)
   - `end` → last page of document
   - `r1` → last page (reverse numbering)
   - `r2` → second-to-last page
   - `rend` → first page
   - `1-end` → all pages

4. **Qualifiers** (Medium)
   - `1-10even` → pages [2, 4, 6, 8, 10]
   - `1-10odd` → pages [1, 3, 5, 7, 9]
   - `10-1even` → pages [10, 8, 6, 4, 2] (reverse + even)

5. **Rotation** (Medium)
   - `1-5east` → pages 1-5 rotated 90° clockwise
   - `10west` → page 10 rotated 270° clockwise
   - `1-endnorth` → all pages, no rotation
   - `5south` → page 5 rotated 180°
   
   **Rotation mapping:**
   - `north`: 0° (no change)
   - `east`: 90° clockwise
   - `south`: 180°
   - `west`: 270° clockwise
   - `left`: -90° relative
   - `right`: +90° relative
   - `down`: +180° relative

6. **Handle-Based References** (Hard)
   - `A` → all pages from handle A
   - `A1-10` → pages 1-10 from handle A
   - `Bend-1` → all pages from B in reverse
   - `B5-20odd` → odd pages 5-20 from B
   - `A1-10east Bend-1odd` → combination

#### 2.3 Grammar Definition

```
page_range_list := page_range (' ' page_range)*
page_range := [handle] [page_spec] [rotation]

handle := [A-Z]+
page_spec := single_page | range
single_page := number | reverse_page
range := start '-' end [qualifier]

start := number | 'end' | reverse_page
end := number | 'end' | reverse_page
reverse_page := 'r' (number | 'end')

qualifier := 'even' | 'odd'
rotation := 'north' | 'east' | 'south' | 'west' | 'left' | 'right' | 'down'

number := [0-9]+
```

#### 2.4 Test Cases (Critical\!)

**File:** `tests/test_parser.py`

```python
def test_simple_range():
    # "1-5" with 10-page document → [1,2,3,4,5]
    
def test_reverse_range():
    # "10-1" with 10-page document → [10,9,8,...,1]
    
def test_even_odd():
    # "1-10even" → [2,4,6,8,10]
    # "1-10odd" → [1,3,5,7,9]
    
def test_end_keyword():
    # "5-end" with 10-page document → [5,6,7,8,9,10]
    
def test_reverse_numbering():
    # "r1" with 10-page document → [10]
    # "r3-r1" → [8,9,10]
    
def test_rotation():
    # "1-5east" → rotation=90
    
def test_handles():
    # "A1-10" → pages from A
    # "B" → all pages from B
    
def test_combined():
    # "A1-10east B5-20odd Awest"
```

#### 2.5 Deliverables

- [x] `parser.py` (258 lines) ✅
- [x] `test_parser.py` (407 lines) ✅
- [x] Test fixtures created (1page.pdf, 10page.pdf, 20page.pdf) ✅
- [x] All 39 test cases passing ✅
- [x] Documentation in docstrings ✅

**Completed:** 2026-01-02

---

### ✅ Sprint 3: Core Operations (COMPLETED)

**Goal:** Implement cat, rotate, and shuffle using the page range parser

**Status:** Complete

#### 3.1 cat - Concatenate/Merge

**Complexity:** HIGH (uses page range parser extensively)

**File:** `src/pdftk/core.py` (update existing function)

**Implementation:**
```python
def cat(input_files: dict[str, Path], 
        page_ranges: list[str], 
        output: Path) -> None:
    """Concatenate PDFs with page ranges
    
    Examples:
        # Merge all PDFs
        cat({}, [], 'out.pdf')  # Empty ranges = merge all
        
        # Extract pages
        cat({}, ['1-5', '10-15'], 'out.pdf')
        
        # With handles
        cat({'A': 'in1.pdf', 'B': 'in2.pdf'}, 
            ['A1-10east', 'B5-20odd'], 
            'out.pdf')
    """
    # 1. Load all input PDFs into readers
    # 2. Parse page ranges
    # 3. For each page spec:
    #    - Get correct reader
    #    - Extract pages
    #    - Apply rotation
    #    - Add to writer
    # 4. Write output
```

**Features:**
- [x] Basic merge (if page_ranges is empty)
- [ ] Page selection with ranges
- [ ] Handle-based file references
- [ ] Page rotation
- [ ] Odd/even filtering
- [ ] Bookmark preservation (bonus)

**Test Cases:**
```python
def test_cat_merge_all():
    # cat(['a.pdf', 'b.pdf'], [], 'out.pdf')
    
def test_cat_extract_pages():
    # cat(['in.pdf'], ['1-5', '10-15'], 'out.pdf')
    
def test_cat_with_rotation():
    # cat(['in.pdf'], ['1-5east'], 'out.pdf')
    
def test_cat_with_handles():
    # cat({'A': 'a.pdf', 'B': 'b.pdf'}, ['A1-5', 'B'], 'out.pdf')
```

#### 3.2 rotate - Rotate Specific Pages

**Complexity:** MEDIUM

**File:** `src/pdftk/core.py` (update existing function)

**Implementation:**
```python
def rotate(input_file: Path, 
           page_ranges: list[str], 
           output: Path) -> None:
    """Rotate specific pages
    
    Examples:
        # Rotate first page 90° clockwise
        rotate('in.pdf', ['1east'], 'out.pdf')
        
        # Rotate multiple ranges
        rotate('in.pdf', ['1-5south', '10-20east'], 'out.pdf')
    """
    # 1. Load input PDF
    # 2. Parse rotation specifications
    # 3. Create rotation map: page_num → rotation_degrees
    # 4. Iterate all pages:
    #    - Apply rotation if in map
    #    - Add to writer
    # 5. Write output
```

**Features:**
- [ ] Rotate specific pages
- [ ] Multiple rotation ranges
- [ ] Keep page order unchanged
- [ ] All rotation directions

**Test Cases:**
```python
def test_rotate_single_page():
    # rotate('in.pdf', ['1east'], 'out.pdf')
    
def test_rotate_range():
    # rotate('in.pdf', ['1-5south'], 'out.pdf')
    
def test_rotate_multiple():
    # rotate('in.pdf', ['1east', '5-10west'], 'out.pdf')
```

#### 3.3 shuffle - Collate Pages

**Complexity:** MEDIUM

**File:** `src/pdftk/core.py` (update existing function)

**Implementation:**
```python
def shuffle(input_files: dict[str, Path], 
            page_ranges: list[str], 
            output: Path) -> None:
    """Collate pages round-robin
    
    Examples:
        # Interleave front and back scans
        shuffle({'A': 'front.pdf', 'B': 'back.pdf'}, 
                ['A', 'Bend-1'], 
                'book.pdf')
                
        # Result: A1, B-last, A2, B-second-to-last, ...
    """
    # 1. Load all input PDFs
    # 2. Parse all page ranges into iterators
    # 3. Round-robin through iterators:
    #    - Take one page from each iterator
    #    - Add to writer
    #    - Remove exhausted iterators
    # 4. Write output
```

**Features:**
- [ ] Round-robin page selection
- [ ] Multiple input files
- [ ] Handle-based references
- [ ] Page rotation support

**Test Cases:**
```python
def test_shuffle_two_pdfs():
    # shuffle({'A': 'a.pdf', 'B': 'b.pdf'}, ['A', 'B'], 'out.pdf')
    
def test_shuffle_reverse():
    # shuffle({'A': 'a.pdf', 'B': 'b.pdf'}, ['A', 'Bend-1'], 'out.pdf')
```

#### 3.4 Deliverables

- [x] `cat` implementation (68 lines) ✅
- [x] `rotate` implementation (48 lines) ✅
- [x] `shuffle` implementation (74 lines) ✅
- [x] Integration tests (24 tests, all passing) ✅
- [x] Demonstration script showing all operations ✅

**Completed:** 2026-01-02

**Test Results:**
- 63 total tests passing (39 parser + 24 core operations)
- All operations verified working with complex page ranges
- Rotation, even/odd filtering, reverse ranges all functional

**Known Issues:**
- CLI argument parsing has limitations with argparse and positional arguments
- Workaround: Operations work perfectly via Python API
- Will be addressed in Sprint 4

---

### ⏳ Sprint 4: Polish & Testing (PENDING)

**Goal:** Comprehensive testing, documentation, and CLI improvements

#### 4.1 Test Suite

**Unit Tests:**
- [ ] `test_parser.py` - Page range parser (critical\!)
- [ ] `test_core.py` - Core operations
- [ ] `test_utils.py` - Utility functions
- [ ] `test_cli.py` - CLI argument parsing

**Integration Tests:**
- [ ] End-to-end CLI tests
- [ ] Test with real PDF files
- [ ] Error handling tests
- [ ] Edge cases (empty PDFs, single-page PDFs, etc.)

**Test PDF Fixtures:**
- [ ] Create `tests/fixtures/` directory
- [ ] Single-page PDF
- [ ] Multi-page PDF (10 pages)
- [ ] PDF with bookmarks
- [ ] Rotated PDF

#### 4.2 Error Handling

- [ ] Better error messages
- [ ] Invalid page range detection
- [ ] File not found handling
- [ ] Invalid PDF handling
- [ ] Handle conflicts
- [ ] Out-of-range page numbers

#### 4.3 Documentation

- [ ] Update README with all operations
- [ ] Add usage examples
- [ ] Document page range syntax
- [ ] Add troubleshooting section
- [ ] CLI help text improvements

#### 4.4 CLI Improvements

- [ ] Verbose mode (`--verbose` flag)
- [ ] Quiet mode (`--quiet` flag)
- [ ] Progress indicators for long operations
- [ ] Better help messages
- [ ] Examples in `--help` output

#### 4.5 Code Quality

- [ ] Type hints throughout
- [ ] Docstrings for all functions
- [ ] Code formatting (black)
- [ ] Linting (flake8)
- [ ] 80%+ test coverage

#### 4.6 Deliverables

- [ ] Complete test suite (500+ lines)
- [ ] Updated documentation
- [ ] Code quality checks passing
- [ ] All operations tested end-to-end

**Estimated Time:** 1 week

---

## Phase 1 Summary

**Total Estimated Time:** 3-4 weeks

**Success Criteria:**
- ✅ CLI accepts pdftk-style commands
- ✅ `burst` splits PDFs into individual pages (DONE)
- [ ] `cat` works with page ranges and rotation
- [ ] `rotate` rotates specific pages
- [ ] `shuffle` collates pages from multiple inputs
- [ ] Page range parser handles all syntax variations
- [ ] Test suite covers critical functionality
- [ ] README documents installation and usage

---

## Future Phases (Post-Phase 1)

### Phase 2: Watermark/Stamp Operations

**Complexity:** Medium

**Operations:**
- `background` - Apply PDF as background (watermark behind content)
- `multibackground` - Apply each background page to corresponding input page
- `stamp` - Overlay stamp PDF on top of input pages
- `multistamp` - Apply each stamp page to corresponding input page

**Requirements:**
- PDF composition/layering system
- Transparency handling
- Page scaling and positioning

**Estimated Time:** 1-2 weeks

### Phase 3: Form Operations

**Complexity:** High

**Operations:**
- `fill_form` - Fill PDF form fields from FDF/XFDF
- `generate_fdf` - Extract form field data to FDF
- `dump_data_fields` - Report form field statistics

**Requirements:**
- FDF/XFDF parser
- Form field identification and mapping
- Data injection into form fields
- Rich text handling

**Estimated Time:** 2-3 weeks

### Phase 4: Metadata Operations

**Complexity:** Medium

**Operations:**
- `dump_data` - Extract metadata, bookmarks, page metrics
- `update_info` - Update PDF metadata from data file
- `attach_files` - Attach files to PDF
- `unpack_files` - Extract attachments from PDF
- `dump_data_annots` - Report annotation information

**Requirements:**
- Metadata extraction and modification
- Bookmark tree traversal
- File attachment handling
- XML entity encoding

**Estimated Time:** 1-2 weeks

### Phase 5: Security Operations

**Complexity:** Very High

**Operations:**
- `encrypt_40bit` / `encrypt_128bit` - Set encryption strength
- `owner_pw` / `user_pw` - Set passwords
- `allow` - Set PDF permissions
- `input_pw` - Handle encrypted input PDFs

**Requirements:**
- Cryptographic library (RC4/AES)
- Permission bitmap system
- Password handling and hashing
- Key derivation

**Estimated Time:** 2-3 weeks

---

## Technical Decisions

### Libraries

**pypdf** (formerly PyPDF2)
- ✅ Pure Python, no C dependencies
- ✅ Active maintenance (3.x series)
- ✅ Sufficient for basic operations
- ✅ Already familiar from Zenith project
- ❌ Performance not as good as pikepdf

**Alternative:** pikepdf
- Requires qpdf C++ library
- Better performance
- More complex setup
- Overkill for Phase 1

### Architecture

**CLI-only (no library API)**
- ✅ Simpler to implement
- ✅ Focused scope
- ✅ Can add library API later if needed

**argparse (not Click/Typer)**
- ✅ Standard library
- ✅ No extra dependencies
- ✅ Mature and well-documented

**Phased approach**
- ✅ Start with basic operations
- ✅ Validate architecture before expanding
- ✅ Each sprint delivers working features

---

## File Structure

```
pdftk/
├── pyproject.toml              # Project configuration
├── README.md                   # User documentation
├── IMPLEMENTATION.md           # This file
├── pdftk.md                    # Complete pdftk reference
├── .gitignore                  # Git ignore patterns
├── src/
│   └── pdftk/
│       ├── __init__.py         # Package initialization (✅)
│       ├── __main__.py         # CLI entry point (✅)
│       ├── cli.py              # Argument parsing (✅)
│       ├── core.py             # Core operations (✅ burst, ⏳ others)
│       ├── parser.py           # Page range parser (⏳)
│       └── utils.py            # Helper functions (✅)
└── tests/
    ├── __init__.py             # Test package (✅)
    ├── fixtures/               # Test PDF files (⏳)
    ├── test_parser.py          # Parser tests (⏳)
    ├── test_core.py            # Core operation tests (⏳)
    ├── test_utils.py           # Utility tests (⏳)
    └── test_cli.py             # CLI tests (⏳)
```

**Legend:**
- ✅ Complete
- ⏳ Planned/In Progress
- ❌ Blocked/Deferred

---

## Current Status

**Sprint 1:** ✅ Complete
**Sprint 2:** ⏳ Ready to start (Page Range Parser)

**Next Action:** Begin implementing `parser.py` with simple range support, then incrementally add complexity.

---

## Contributing Guidelines

When implementing features:

1. **Write tests first** (TDD approach for parser)
2. **Start simple** (basic ranges before complex syntax)
3. **Incremental complexity** (add features one at a time)
4. **Document as you go** (docstrings and examples)
5. **Test with real PDFs** (integration tests)

---

## Performance Considerations

For Phase 1:
- Focus on correctness over performance
- pypdf is sufficient for typical use cases
- Profile before optimizing

For future phases:
- Consider pikepdf for large-scale operations
- Implement caching for frequently accessed pages
- Parallelize page processing if needed

---

## Known Limitations

**Phase 1 (Current):**
- No encryption support yet
- No form filling yet
- No watermark/stamp operations yet
- Limited to basic page operations

**pypdf limitations:**
- Slower than pikepdf for large PDFs
- Some advanced PDF features not fully supported
- XFA forms not supported

---

## Resources

- [pypdf documentation](https://pypdf.readthedocs.io/)
- [Original pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/)
- [PDF Reference 1.7](https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/PDF32000_2008.pdf)

---

**Last Updated:** 2026-01-02
**Version:** 0.1.0
**Sprint:** 1 of 4 (Phase 1)
