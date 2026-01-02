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
        prog='pdftk',
        description='PDF Toolkit - manipulate PDF documents',
        epilog='For detailed documentation, see pdftk.md'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )

    # Input files
    parser.add_argument(
        'inputs',
        nargs='+',
        metavar='INPUT',
        help='Input PDF files, optionally with handles (A=file.pdf)'
    )

    # Subcommands for operations
    subparsers = parser.add_subparsers(
        dest='operation',
        help='PDF operation to perform',
        required=False
    )

    # burst operation
    burst_parser = subparsers.add_parser(
        'burst',
        help='Split PDF into individual page files'
    )
    burst_parser.add_argument(
        '--output',
        '-o',
        dest='output_pattern',
        default='pg_%04d.pdf',
        help='Output filename pattern (default: pg_%%04d.pdf)'
    )
    burst_parser.add_argument(
        '--output-dir',
        dest='output_dir',
        type=Path,
        default=Path('.'),
        help='Output directory (default: current directory)'
    )

    # cat operation (stub)
    cat_parser = subparsers.add_parser(
        'cat',
        help='Concatenate/merge PDFs with page ranges'
    )
    cat_parser.add_argument(
        'ranges',
        nargs='*',
        help='Page ranges (e.g., 1-5, A1-10east, Bend-1odd)'
    )
    cat_parser.add_argument(
        'output',
        help='Output PDF file'
    )

    # rotate operation (stub)
    rotate_parser = subparsers.add_parser(
        'rotate',
        help='Rotate specific pages'
    )
    rotate_parser.add_argument(
        'ranges',
        nargs='+',
        help='Page ranges with rotation (e.g., 1east, 5-10south)'
    )
    rotate_parser.add_argument(
        'output',
        help='Output PDF file'
    )

    # shuffle operation (stub)
    shuffle_parser = subparsers.add_parser(
        'shuffle',
        help='Collate pages from multiple inputs'
    )
    shuffle_parser.add_argument(
        'ranges',
        nargs='+',
        help='Page ranges to shuffle'
    )
    shuffle_parser.add_argument(
        'output',
        help='Output PDF file'
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
        # Parse input files
        handles, files = parse_input_files(parsed_args.inputs)

        # Validate input files exist
        for file in files:
            validate_pdf_exists(file)

        # Dispatch to operation
        if parsed_args.operation == 'burst':
            if len(files) \!= 1:
                parser.error("burst operation requires exactly one input PDF")

            pages = burst(
                files[0],
                parsed_args.output_pattern,
                parsed_args.output_dir
            )
            print(f"\nSuccessfully split {pages} pages from {files[0]}")

        elif parsed_args.operation == 'cat':
            cat(handles, parsed_args.ranges, Path(parsed_args.output))
            print(f"\nSuccessfully created {parsed_args.output}")

        elif parsed_args.operation == 'rotate':
            if len(files) \!= 1:
                parser.error("rotate operation requires exactly one input PDF")

            rotate(files[0], parsed_args.ranges, Path(parsed_args.output))
            print(f"\nSuccessfully created {parsed_args.output}")

        elif parsed_args.operation == 'shuffle':
            shuffle(handles, parsed_args.ranges, Path(parsed_args.output))
            print(f"\nSuccessfully created {parsed_args.output}")

        else:
            # No operation specified - show help
            parser.print_help()
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NotImplementedError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
