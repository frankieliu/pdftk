"""Core PDF operations for pdftk

This module implements the main PDF manipulation operations:
- burst: Split PDF into individual pages
- cat: Concatenate/merge PDFs with page ranges
- rotate: Rotate specific pages
- shuffle: Collate pages from multiple inputs
"""

from pathlib import Path
from typing import Optional
from pypdf import PdfReader, PdfWriter
from pdftk.parser import PageRangeParser


def burst(
    input_file: Path,
    output_pattern: str = "pg_%04d.pdf",
    output_dir: Optional[Path] = None,
) -> int:
    """Split a PDF into individual page files

    Args:
        input_file: Path to input PDF
        output_pattern: Printf-style format string for output filenames
        output_dir: Directory for output files (default: current directory)

    Returns:
        Number of pages processed

    Example:
        burst('document.pdf', 'page_%02d.pdf', Path('output/'))
    """
    if output_dir is None:
        output_dir = Path(".")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(input_file)
    total_pages = len(reader.pages)

    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)

        output_file = output_dir / (output_pattern % i)
        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Created: {output_file}")

    return total_pages


def cat(input_files: dict[str, Path], page_ranges: list[str], output: Path) -> None:
    """Concatenate PDFs with page ranges

    Args:
        input_files: Dictionary mapping handles to file paths
                    e.g., {'A': Path('in1.pdf'), 'B': Path('in2.pdf')}
        page_ranges: List of page range specifications
                    e.g., ['A1-10east', 'B5-20odd']
                    If empty, merges all input files
        output: Output PDF path

    Examples:
        # Merge all PDFs
        cat({'A': 'in1.pdf', 'B': 'in2.pdf'}, [], 'out.pdf')

        # Extract specific pages with rotation
        cat({'A': 'in.pdf'}, ['1-5east', '10-20'], 'out.pdf')

        # Complex ranges with handles
        cat({'A': 'in1.pdf', 'B': 'in2.pdf'},
            ['A1-10east', 'B5-20odd'],
            'out.pdf')
    """
    # Load all input PDFs into readers
    readers = {}
    for handle, filepath in input_files.items():
        readers[handle] = PdfReader(filepath)

    # Determine default reader (if only one file and no page ranges specified)
    default_reader = None
    if len(readers) == 1:
        default_reader = list(readers.values())[0]

    writer = PdfWriter()

    # If no page ranges specified, merge all input files in order
    if not page_ranges:
        for handle in sorted(readers.keys()):
            reader = readers[handle]
            for page in reader.pages:
                writer.add_page(page)
    else:
        # Parse page ranges and extract pages
        parser = PageRangeParser(readers, default_reader)

        for range_str in page_ranges:
            specs = parser.parse(range_str)

            for spec in specs:
                # Get the appropriate reader
                if spec.handle:
                    reader = readers[spec.handle]
                else:
                    if default_reader is None:
                        raise ValueError("No default reader available")
                    reader = default_reader

                # Extract and add pages
                for page_num in spec.pages:
                    page = reader.pages[page_num - 1]  # Convert 1-indexed to 0-indexed

                    # Apply rotation if specified
                    if spec.rotation != 0:
                        page.rotate(spec.rotation)

                    writer.add_page(page)

    # Write output
    with open(output, "wb") as f:
        writer.write(f)

    print(f"Created: {output}")


def rotate(input_file: Path, page_ranges: list[str], output: Path) -> None:
    """Rotate specific pages in a PDF

    Args:
        input_file: Input PDF path
        page_ranges: List of page ranges with rotation
                    e.g., ['1east', '5-10south', '20west']
        output: Output PDF path

    Examples:
        # Rotate first page 90° clockwise
        rotate('in.pdf', ['1east'], 'out.pdf')

        # Rotate multiple ranges
        rotate('in.pdf', ['1-5south', '10-20east'], 'out.pdf')

    Note:
        Pages not specified in page_ranges remain unrotated.
        Page order is preserved.
    """
    # Load input PDF
    reader = PdfReader(input_file)

    # Parse rotation specifications
    # Use empty handle for single-file operations
    parser = PageRangeParser({}, default_reader=reader)

    rotation_map = {}
    for range_str in page_ranges:
        specs = parser.parse(range_str)

        # Build rotation map: page_num → rotation_degrees
        for spec in specs:
            for page_num in spec.pages:
                rotation_map[page_num] = spec.rotation

    # Process all pages
    writer = PdfWriter()
    for i, page in enumerate(reader.pages, start=1):
        # Apply rotation if specified for this page
        if i in rotation_map:
            page.rotate(rotation_map[i])
        writer.add_page(page)

    # Write output
    with open(output, "wb") as f:
        writer.write(f)

    print(f"Created: {output}")


def shuffle(input_files: dict[str, Path], page_ranges: list[str], output: Path) -> None:
    """Collate pages from multiple inputs in round-robin fashion

    Args:
        input_files: Dictionary mapping handles to file paths
                    e.g., {'A': Path('front.pdf'), 'B': Path('back.pdf')}
        page_ranges: List of page ranges to shuffle
                    e.g., ['A', 'Bend-1']
        output: Output PDF path

    Examples:
        # Interleave front and back scans
        shuffle({'A': 'front.pdf', 'B': 'back.pdf'},
                ['A', 'Bend-1'],
                'book.pdf')
        # Result: A1, B-last, A2, B-second-to-last, ...

        # Shuffle specific pages
        shuffle({'A': 'a.pdf', 'B': 'b.pdf'},
                ['A1-10', 'B1-10'],
                'out.pdf')
        # Result: A1, B1, A2, B2, A3, B3, ...

    Note:
        Takes one page from each page range in turn (round-robin).
        Continues until all page ranges are exhausted.
    """
    # Load all input PDFs
    readers = {}
    for handle, filepath in input_files.items():
        readers[handle] = PdfReader(filepath)

    # Parse all page ranges
    parser = PageRangeParser(readers)
    all_specs = []

    for range_str in page_ranges:
        specs = parser.parse(range_str)
        all_specs.extend(specs)

    # Create iterators for each spec's pages
    # Each iterator yields (reader, page_num, rotation) tuples
    page_iterators = []
    for spec in all_specs:
        if spec.handle is None:
            raise ValueError("Shuffle requires handle-based file references")
        reader = readers[spec.handle]
        # Create list of tuples (not generator) to avoid closure bug
        pages_list = [(reader, page_num, spec.rotation) for page_num in spec.pages]
        page_iter = iter(pages_list)
        page_iterators.append(page_iter)

    # Round-robin through iterators
    writer = PdfWriter()
    while page_iterators:
        for page_iter in page_iterators[
            :
        ]:  # Copy list to allow removal during iteration
            try:
                reader, page_num, rotation = next(page_iter)

                # Get the page (convert 1-indexed to 0-indexed)
                page = reader.pages[page_num - 1]

                # Apply rotation if specified
                if rotation != 0:
                    page.rotate(rotation)

                writer.add_page(page)

            except StopIteration:
                # This iterator is exhausted, remove it
                page_iterators.remove(page_iter)

    # Write output
    with open(output, "wb") as f:
        writer.write(f)

    print(f"Created: {output}")
