"""Utility functions for pdftk"""

from pathlib import Path
from typing import Dict, Tuple


def parse_input_files(inputs: list[str]) -> Tuple[Dict[str, Path], list[Path]]:
    """Parse input file specifications with optional handles

    Args:
        inputs: List of input specifications (e.g., ['A=file1.pdf', 'file2.pdf'])

    Returns:
        Tuple of (handles_dict, files_list)
        handles_dict maps handles to file paths
        files_list contains all files in order

    Examples:
        >>> parse_input_files(['A=in1.pdf', 'B=in2.pdf'])
        ({'A': Path('in1.pdf'), 'B': Path('in2.pdf')}, [Path('in1.pdf'), Path('in2.pdf')])

        >>> parse_input_files(['input.pdf'])
        ({}, [Path('input.pdf')])
    """
    handles = {}
    files = []

    for spec in inputs:
        if '=' in spec:
            # Handle-based input: A=file.pdf
            handle, filepath = spec.split('=', 1)
            path = Path(filepath)
            handles[handle.upper()] = path
            files.append(path)
        else:
            # Simple file path
            path = Path(spec)
            files.append(path)

    return handles, files


def validate_pdf_exists(path: Path) -> None:
    """Validate that a PDF file exists

    Args:
        path: Path to PDF file

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a PDF
    """
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if not path.suffix.lower() == '.pdf':
        raise ValueError(f"File is not a PDF: {path}")
