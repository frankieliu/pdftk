"""Page range parser for pdftk

Parses pdftk-style page range specifications like:
- Simple ranges: 1-5, 10-20
- Reverse ranges: 10-1
- Special keywords: end, r1, rend
- Qualifiers: 1-10even, 5-20odd
- Rotation: 1-5east, 10west
- Handles: A1-10, Bend-1odd
"""

from dataclasses import dataclass, field
from typing import Optional
from pypdf import PdfReader
import re


@dataclass
class PageSpec:
    """Specification for pages to extract

    Attributes:
        handle: Handle reference (e.g., 'A', 'B') or None for default
        pages: List of page numbers (1-indexed)
        rotation: Rotation in degrees (0, 90, 180, 270)
    """

    handle: Optional[str] = None
    pages: list[int] = field(default_factory=list)
    rotation: int = 0


class PageRangeParser:
    """Parse pdftk-style page range specifications

    Examples:
        >>> readers = {'A': PdfReader('a.pdf')}
        >>> parser = PageRangeParser(readers)
        >>> specs = parser.parse("1-5")
        >>> specs[0].pages
        [1, 2, 3, 4, 5]
    """

    # Rotation keywords to degrees
    ROTATIONS = {
        "north": 0,
        "east": 90,
        "south": 180,
        "west": 270,
        "left": -90,
        "right": 90,
        "down": 180,
    }

    def __init__(
        self, readers: dict[str, PdfReader], default_reader: Optional[PdfReader] = None
    ):
        """Initialize parser with PDF readers

        Args:
            readers: Dictionary mapping handles to PdfReader objects
                    e.g., {'A': PdfReader('a.pdf'), 'B': PdfReader('b.pdf')}
            default_reader: Optional default reader for ranges without handles
        """
        self.readers = readers
        self.default_reader = default_reader

        # If only one reader and no default, use it as default
        if default_reader is None and len(readers) == 1:
            self.default_reader = list(readers.values())[0]

    def parse(self, range_str: str) -> list[PageSpec]:
        """Parse page range string into PageSpec objects

        Args:
            range_str: Page range specification (e.g., "1-5 10-20east A1-5")

        Returns:
            List of PageSpec objects

        Examples:
            >>> parser.parse("1-5")
            [PageSpec(handle=None, pages=[1,2,3,4,5], rotation=0)]

            >>> parser.parse("1-5east 10-20odd")
            [PageSpec(pages=[1,2,3,4,5], rotation=90),
             PageSpec(pages=[11,13,15,17,19], rotation=0)]
        """
        if not range_str.strip():
            return []

        # Split by whitespace
        parts = range_str.split()
        specs = []

        for part in parts:
            spec = self._parse_single(part)
            if spec:
                specs.append(spec)

        return specs

    def _parse_single(self, part: str) -> Optional[PageSpec]:
        """Parse a single range specification

        Args:
            part: Single range (e.g., "1-5east", "A1-10", "Bend-1odd")

        Returns:
            PageSpec object or None if invalid
        """
        # Extract handle (uppercase letters at start)
        handle = None
        remaining = part

        if part and part[0].isupper():
            match = re.match(r"^([A-Z]+)", part)
            if match:
                handle = match.group(1)
                remaining = part[len(handle) :]

        # If only handle and nothing else (e.g., "A" or "B")
        if not remaining and handle:
            return self._handle_only(handle)

        # Extract rotation (at the end)
        rotation = 0
        for rot_keyword, rot_degrees in self.ROTATIONS.items():
            if remaining.endswith(rot_keyword):
                rotation = rot_degrees
                remaining = remaining[: -len(rot_keyword)]
                break

        # Extract qualifier (even/odd before rotation)
        qualifier = None
        if remaining.endswith("even"):
            qualifier = "even"
            remaining = remaining[:-4]
        elif remaining.endswith("odd"):
            qualifier = "odd"
            remaining = remaining[:-3]

        # Now remaining should be the page specification
        # Examples: "1-5", "10", "5-end", "r1-r3", "end"
        pages = self._parse_page_spec(remaining, handle)

        # Apply qualifier filter
        if qualifier:
            pages = self._apply_qualifier(pages, qualifier)

        return PageSpec(handle=handle, pages=pages, rotation=rotation)

    def _handle_only(self, handle: str) -> PageSpec:
        """Handle case where only a handle is specified (e.g., "A")

        Returns all pages from that handle's PDF
        """
        if handle not in self.readers:
            raise ValueError(f"Unknown handle: {handle}")

        reader = self.readers[handle]
        pages = list(range(1, len(reader.pages) + 1))
        return PageSpec(handle=handle, pages=pages, rotation=0)

    def _parse_page_spec(self, spec: str, handle: Optional[str]) -> list[int]:
        """Parse page specification (without qualifier or rotation)

        Args:
            spec: Page spec like "1-5", "10", "5-end", "r1"
            handle: Handle to determine page count

        Returns:
            List of page numbers (1-indexed)
        """
        if not spec:
            return []

        # Get the reader for this spec
        reader = self._get_reader(handle)
        if not reader:
            raise ValueError(f"No PDF reader available for handle: {handle}")

        total_pages = len(reader.pages)

        # Check if it's a range (contains '-')
        if "-" in spec:
            parts = spec.split("-", 1)
            start_str = parts[0]
            end_str = parts[1]

            # Resolve start and end page numbers
            start = self._resolve_page_number(start_str, total_pages)
            end = self._resolve_page_number(end_str, total_pages)

            # Generate range (inclusive)
            if start <= end:
                return list(range(start, end + 1))
            else:
                # Reverse range (e.g., 10-1)
                return list(range(start, end - 1, -1))
        else:
            # Single page
            page = self._resolve_page_number(spec, total_pages)
            return [page]

    def _resolve_page_number(self, spec: str, total_pages: int) -> int:
        """Resolve page number from specification

        Args:
            spec: Page spec like "5", "end", "r1", "rend"
            total_pages: Total number of pages in document

        Returns:
            Page number (1-indexed)
        """
        if spec == "end":
            return total_pages
        elif spec == "rend":
            return 1
        elif spec.startswith("r"):
            # Reverse numbering: r1 = last page, r2 = second-to-last
            offset = int(spec[1:])
            return total_pages - offset + 1
        else:
            return int(spec)

    def _apply_qualifier(self, pages: list[int], qualifier: str) -> list[int]:
        """Apply even/odd filter to page list

        Args:
            pages: List of page numbers
            qualifier: 'even' or 'odd'

        Returns:
            Filtered list of pages
        """
        if qualifier == "even":
            return [p for p in pages if p % 2 == 0]
        elif qualifier == "odd":
            return [p for p in pages if p % 2 == 1]
        else:
            return pages

    def _get_reader(self, handle: Optional[str]) -> Optional[PdfReader]:
        """Get PDF reader for given handle

        Args:
            handle: Handle name or None for default

        Returns:
            PdfReader object or None
        """
        if handle:
            return self.readers.get(handle)
        else:
            return self.default_reader
