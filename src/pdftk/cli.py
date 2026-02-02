"""Command-line interface for pdftk"""

import argparse
import sys
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for pdftk CLI

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="pdftk",
        description="PDF Toolkit - manipulate PDF documents",
        epilog="For more information and examples, see README.md",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.1.1")

    # Subcommands for operations
    subparsers = parser.add_subparsers(
        dest="operation",
        help="PDF operation to perform",
        required=True,
        metavar="OPERATION",
    )

    # burst operation
    burst_parser = subparsers.add_parser(
        "burst",
        help="Split PDF into individual page files",
        description="Split a PDF into individual page files",
    )
    burst_parser.add_argument(
        "input", type=Path, metavar="INPUT", help="Input PDF file"
    )
    burst_parser.add_argument(
        "-p",
        "--pattern",
        dest="output_pattern",
        default="pg_%04d.pdf",
        help="Output filename pattern (default: pg_%%04d.pdf)",
    )
    burst_parser.add_argument(
        "-d",
        "--dir",
        dest="output_dir",
        type=Path,
        default=Path("."),
        help="Output directory (default: current directory)",
    )

    # cat operation
    cat_parser = subparsers.add_parser(
        "cat",
        help="Concatenate/merge PDFs with page ranges",
        description="Concatenate and merge PDFs with optional page selection",
        epilog="""
Examples:
  # Extract pages 1-3 from a.pdf and pages 5, 7 from b.pdf
  pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-3 B5 B7

  # Multiple ranges from each file
  pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-3 A10 B5 B7 B8-10

  # With rotation (pages 1-3 from A rotated 90° clockwise)
  pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-3east B5 B7

  # With even/odd qualifiers
  pdftk cat A=a.pdf B=b.pdf -o out.pdf -r A1-10even B5-10odd

  # Merge all pages (no ranges specified)
  pdftk cat A=a.pdf B=b.pdf -o merged.pdf

  # Single file without handles
  pdftk cat input.pdf -o output.pdf -r 1-5
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    cat_parser.add_argument(
        "inputs",
        nargs="+",
        metavar="INPUT",
        help="Input PDF files, optionally with handles (A=file.pdf)",
    )
    cat_parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="Output PDF file",
    )
    cat_parser.add_argument(
        "-r",
        "--ranges",
        nargs="*",
        default=[],
        metavar="RANGE",
        help="Page ranges (e.g., 1-5, A1-10east, Bend-1odd). "
        "If omitted, merges all input files. Ranges are space-separated.",
    )

    # rotate operation
    rotate_parser = subparsers.add_parser(
        "rotate",
        help="Rotate specific pages in a PDF",
        description="Rotate specific pages in a PDF document",
    )
    rotate_parser.add_argument(
        "input", type=Path, metavar="INPUT", help="Input PDF file"
    )
    rotate_parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="Output PDF file",
    )
    rotate_parser.add_argument(
        "-r",
        "--ranges",
        nargs="+",
        required=True,
        metavar="RANGE",
        help="Page ranges with rotation (e.g., 1east, 5-10south)",
    )

    # shuffle operation
    shuffle_parser = subparsers.add_parser(
        "shuffle",
        help="Collate pages from multiple inputs",
        description="Collate pages from multiple PDFs in round-robin fashion",
    )
    shuffle_parser.add_argument(
        "inputs",
        nargs="+",
        metavar="INPUT",
        help="Input PDF files with handles (A=file.pdf B=file.pdf)",
    )
    shuffle_parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="Output PDF file",
    )
    shuffle_parser.add_argument(
        "-r",
        "--ranges",
        nargs="+",
        required=True,
        metavar="RANGE",
        help="Page ranges to shuffle (e.g., A1-10 B1-10)",
    )

    return parser


def main(args=None):
    """Main CLI entry point

    Args:
        args: Command-line arguments (default: sys.argv[1:])
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # Import here to avoid circular imports
    from pdftk.core import burst, cat, rotate, shuffle
    from pdftk.utils import parse_input_files, validate_pdf_exists

    try:
        if parsed_args.operation == "burst":
            # Burst: single input file
            validate_pdf_exists(parsed_args.input)
            pages = burst(
                parsed_args.input, parsed_args.output_pattern, parsed_args.output_dir
            )
            print(f"Successfully split {pages} pages from {parsed_args.input}")

        elif parsed_args.operation == "cat":
            # Cat: multiple inputs, optional page ranges
            handles, files = parse_input_files(parsed_args.inputs)

            # Validate input files exist
            for file in files:
                validate_pdf_exists(file)

            # If no handles were specified, assign default handles (A, B, C, ...)
            if not handles:
                for i, file in enumerate(files):
                    handle = chr(ord("A") + i)
                    handles[handle] = file

            cat(handles, parsed_args.ranges, parsed_args.output)
            print(f"Successfully created {parsed_args.output}")

        elif parsed_args.operation == "rotate":
            # Rotate: single input, required page ranges
            validate_pdf_exists(parsed_args.input)
            rotate(parsed_args.input, parsed_args.ranges, parsed_args.output)
            print(f"Successfully created {parsed_args.output}")

        elif parsed_args.operation == "shuffle":
            # Shuffle: multiple inputs with handles, required page ranges
            handles, files = parse_input_files(parsed_args.inputs)

            # Validate input files exist
            for file in files:
                validate_pdf_exists(file)

            # Shuffle requires handles
            if not handles:
                print(
                    "Error: shuffle requires input files with handles "
                    "(e.g., A=file1.pdf B=file2.pdf)",
                    file=sys.stderr,
                )
                sys.exit(1)

            shuffle(handles, parsed_args.ranges, parsed_args.output)
            print(f"Successfully created {parsed_args.output}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
