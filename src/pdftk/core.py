"""Core PDF operations for pdftk

This module implements the main PDF manipulation operations:
- burst: Split PDF into individual pages
- cat: Concatenate/merge PDFs with page ranges
- rotate: Rotate specific pages
- shuffle: Collate pages from multiple inputs
"""

from pathlib import Path
from pypdf import PdfReader, PdfWriter


def burst(input_file: Path, output_pattern: str = "pg_%04d.pdf", output_dir: Path = None) -> int:
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
        with open(output_file, 'wb') as f:
            writer.write(f)

        print(f"Created: {output_file}")

    return total_pages


def cat(input_files: dict[str, Path], page_ranges: list[str], output: Path) -> None:
    """Concatenate PDFs with page ranges (stub for now)

    Args:
        input_files: Dictionary mapping handles to file paths
        page_ranges: List of page range specifications
        output: Output PDF path
    """
    raise NotImplementedError("cat operation not yet implemented")


def rotate(input_file: Path, page_ranges: list[str], output: Path) -> None:
    """Rotate specific pages (stub for now)

    Args:
        input_file: Input PDF path
        page_ranges: List of page ranges with rotation
        output: Output PDF path
    """
    raise NotImplementedError("rotate operation not yet implemented")


def shuffle(input_files: dict[str, Path], page_ranges: list[str], output: Path) -> None:
    """Collate pages from multiple inputs (stub for now)

    Args:
        input_files: Dictionary mapping handles to file paths
        page_ranges: List of page ranges to shuffle
        output: Output PDF path
    """
    raise NotImplementedError("shuffle operation not yet implemented")
