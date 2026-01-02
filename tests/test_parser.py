"""Tests for page range parser"""

import pytest
from pathlib import Path
from pypdf import PdfReader
from pdftk.parser import PageRangeParser, PageSpec


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_readers(fixtures_dir):
    """Create mock PDF readers for testing"""
    return {
        'A': PdfReader(fixtures_dir / "10page.pdf"),
        'B': PdfReader(fixtures_dir / "20page.pdf")
    }


@pytest.fixture
def default_reader(fixtures_dir):
    """Create default reader for handle-less tests"""
    return PdfReader(fixtures_dir / "10page.pdf")


class TestSimpleRanges:
    """Test basic page range parsing"""

    def test_simple_forward_range(self, mock_readers, default_reader):
        """Test simple forward range like 1-5"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-5")

        assert len(specs) == 1
        assert specs[0].pages == [1, 2, 3, 4, 5]
        assert specs[0].rotation == 0
        assert specs[0].handle is None

    def test_single_page(self, mock_readers, default_reader):
        """Test single page selection"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("5")

        assert len(specs) == 1
        assert specs[0].pages == [5]
        assert specs[0].rotation == 0

    def test_multiple_ranges(self, mock_readers, default_reader):
        """Test multiple ranges separated by spaces"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-3 7-9")

        assert len(specs) == 2
        assert specs[0].pages == [1, 2, 3]
        assert specs[1].pages == [7, 8, 9]


class TestReverseRanges:
    """Test reverse page ranges"""

    def test_reverse_range(self, mock_readers, default_reader):
        """Test reverse range like 10-1"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("10-1")

        assert len(specs) == 1
        assert specs[0].pages == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    def test_short_reverse_range(self, mock_readers, default_reader):
        """Test short reverse range like 5-3"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("5-3")

        assert len(specs) == 1
        assert specs[0].pages == [5, 4, 3]


class TestSpecialKeywords:
    """Test special keywords like end, r1, rend"""

    def test_end_keyword(self, mock_readers, default_reader):
        """Test 'end' keyword for last page"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("end")

        assert len(specs) == 1
        assert specs[0].pages == [10]  # default_reader has 10 pages

    def test_range_to_end(self, mock_readers, default_reader):
        """Test range to end like 5-end"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("5-end")

        assert len(specs) == 1
        assert specs[0].pages == [5, 6, 7, 8, 9, 10]

    def test_1_to_end(self, mock_readers, default_reader):
        """Test 1-end for all pages"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-end")

        assert len(specs) == 1
        assert specs[0].pages == list(range(1, 11))  # 1-10

    def test_reverse_numbering_r1(self, mock_readers, default_reader):
        """Test r1 for last page"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("r1")

        assert len(specs) == 1
        assert specs[0].pages == [10]

    def test_reverse_numbering_r2(self, mock_readers, default_reader):
        """Test r2 for second-to-last page"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("r2")

        assert len(specs) == 1
        assert specs[0].pages == [9]

    def test_reverse_numbering_rend(self, mock_readers, default_reader):
        """Test rend for first page"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("rend")

        assert len(specs) == 1
        assert specs[0].pages == [1]

    def test_reverse_range_r3_to_r1(self, mock_readers, default_reader):
        """Test reverse range r3-r1 for last 3 pages"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("r3-r1")

        assert len(specs) == 1
        assert specs[0].pages == [8, 9, 10]


class TestQualifiers:
    """Test even/odd qualifiers"""

    def test_even_qualifier(self, mock_readers, default_reader):
        """Test even qualifier like 1-10even"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-10even")

        assert len(specs) == 1
        assert specs[0].pages == [2, 4, 6, 8, 10]

    def test_odd_qualifier(self, mock_readers, default_reader):
        """Test odd qualifier like 1-10odd"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-10odd")

        assert len(specs) == 1
        assert specs[0].pages == [1, 3, 5, 7, 9]

    def test_reverse_even_qualifier(self, mock_readers, default_reader):
        """Test reverse range with even qualifier"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("10-1even")

        assert len(specs) == 1
        assert specs[0].pages == [10, 8, 6, 4, 2]

    def test_reverse_odd_qualifier(self, mock_readers, default_reader):
        """Test reverse range with odd qualifier"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("10-1odd")

        assert len(specs) == 1
        assert specs[0].pages == [9, 7, 5, 3, 1]


class TestRotation:
    """Test rotation keywords"""

    def test_east_rotation(self, mock_readers, default_reader):
        """Test east rotation (90° clockwise)"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-5east")

        assert len(specs) == 1
        assert specs[0].pages == [1, 2, 3, 4, 5]
        assert specs[0].rotation == 90

    def test_west_rotation(self, mock_readers, default_reader):
        """Test west rotation (270° clockwise)"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("10west")

        assert len(specs) == 1
        assert specs[0].pages == [10]
        assert specs[0].rotation == 270

    def test_south_rotation(self, mock_readers, default_reader):
        """Test south rotation (180°)"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-10south")

        assert len(specs) == 1
        assert specs[0].pages == list(range(1, 11))
        assert specs[0].rotation == 180

    def test_north_rotation(self, mock_readers, default_reader):
        """Test north rotation (0°, no change)"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-5north")

        assert len(specs) == 1
        assert specs[0].pages == [1, 2, 3, 4, 5]
        assert specs[0].rotation == 0

    def test_left_rotation(self, mock_readers, default_reader):
        """Test left rotation (-90°)"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("5left")

        assert len(specs) == 1
        assert specs[0].pages == [5]
        assert specs[0].rotation == -90

    def test_right_rotation(self, mock_readers, default_reader):
        """Test right rotation (90°)"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("5right")

        assert len(specs) == 1
        assert specs[0].pages == [5]
        assert specs[0].rotation == 90

    def test_down_rotation(self, mock_readers, default_reader):
        """Test down rotation (180°)"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("5down")

        assert len(specs) == 1
        assert specs[0].pages == [5]
        assert specs[0].rotation == 180


class TestHandles:
    """Test handle-based file references"""

    def test_handle_only(self, mock_readers):
        """Test handle only (all pages from that file)"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A")

        assert len(specs) == 1
        assert specs[0].handle == 'A'
        assert specs[0].pages == list(range(1, 11))  # A has 10 pages

    def test_handle_with_range(self, mock_readers):
        """Test handle with range like A1-5"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A1-5")

        assert len(specs) == 1
        assert specs[0].handle == 'A'
        assert specs[0].pages == [1, 2, 3, 4, 5]

    def test_handle_with_reverse(self, mock_readers):
        """Test handle with reverse range like Bend-1"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("Bend-1")

        assert len(specs) == 1
        assert specs[0].handle == 'B'
        assert specs[0].pages == list(range(20, 0, -1))  # B has 20 pages, reversed

    def test_handle_with_odd_qualifier(self, mock_readers):
        """Test handle with odd qualifier like B5-20odd"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("B5-20odd")

        assert len(specs) == 1
        assert specs[0].handle == 'B'
        assert specs[0].pages == [5, 7, 9, 11, 13, 15, 17, 19]

    def test_handle_with_rotation(self, mock_readers):
        """Test handle with rotation like A1-5east"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A1-5east")

        assert len(specs) == 1
        assert specs[0].handle == 'A'
        assert specs[0].pages == [1, 2, 3, 4, 5]
        assert specs[0].rotation == 90

    def test_multiple_handles(self, mock_readers):
        """Test multiple handle-based ranges"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A1-5 B10-15")

        assert len(specs) == 2
        assert specs[0].handle == 'A'
        assert specs[0].pages == [1, 2, 3, 4, 5]
        assert specs[1].handle == 'B'
        assert specs[1].pages == [10, 11, 12, 13, 14, 15]


class TestCombinedComplexRanges:
    """Test complex combined ranges"""

    def test_combined_with_rotation_and_qualifier(self, mock_readers):
        """Test A1-10east B5-20odd"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A1-10east B5-20odd")

        assert len(specs) == 2

        # First spec: A1-10east
        assert specs[0].handle == 'A'
        assert specs[0].pages == list(range(1, 11))
        assert specs[0].rotation == 90

        # Second spec: B5-20odd
        assert specs[1].handle == 'B'
        assert specs[1].pages == [5, 7, 9, 11, 13, 15, 17, 19]
        assert specs[1].rotation == 0

    def test_complex_three_part(self, mock_readers):
        """Test A1-5 B Aend"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A1-5 B Aend")

        assert len(specs) == 3

        # First spec: A1-5
        assert specs[0].handle == 'A'
        assert specs[0].pages == [1, 2, 3, 4, 5]

        # Second spec: B (all pages)
        assert specs[1].handle == 'B'
        assert specs[1].pages == list(range(1, 21))  # B has 20 pages

        # Third spec: Aend (last page of A)
        assert specs[2].handle == 'A'
        assert specs[2].pages == [10]

    def test_reverse_with_qualifier_and_rotation(self, mock_readers):
        """Test Bend-1evensouth"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("Bend-1evensouth")

        assert len(specs) == 1
        assert specs[0].handle == 'B'
        assert specs[0].pages == [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
        assert specs[0].rotation == 180

    def test_mixed_handles_and_qualifiers(self, mock_readers):
        """Test A1-10even Br3-r1 B5west"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A1-10even Br3-r1 B5west")

        assert len(specs) == 3

        # First spec: A1-10even
        assert specs[0].handle == 'A'
        assert specs[0].pages == [2, 4, 6, 8, 10]

        # Second spec: Br3-r1 (last 3 pages of B)
        assert specs[1].handle == 'B'
        assert specs[1].pages == [18, 19, 20]

        # Third spec: B5west
        assert specs[2].handle == 'B'
        assert specs[2].pages == [5]
        assert specs[2].rotation == 270


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_string(self, mock_readers, default_reader):
        """Test empty range string"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("")

        assert specs == []

    def test_whitespace_only(self, mock_readers, default_reader):
        """Test whitespace-only string"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("   ")

        assert specs == []

    def test_unknown_handle(self, mock_readers):
        """Test unknown handle raises error"""
        parser = PageRangeParser(mock_readers)

        with pytest.raises(ValueError, match="No PDF reader available for handle"):
            parser.parse("C1-5")

    def test_no_default_reader_and_no_handle(self, mock_readers):
        """Test no default reader with handle-less range"""
        parser = PageRangeParser(mock_readers, default_reader=None)

        with pytest.raises(ValueError, match="No PDF reader available"):
            parser.parse("1-5")


class TestDocumentationExamples:
    """Test examples from documentation"""

    def test_readme_example_1(self, mock_readers, default_reader):
        """Test example: 1-5"""
        parser = PageRangeParser(mock_readers, default_reader)
        specs = parser.parse("1-5")

        assert specs[0].pages == [1, 2, 3, 4, 5]

    def test_readme_example_2(self, mock_readers):
        """Test example: A1-10east B5-20odd"""
        parser = PageRangeParser(mock_readers)
        specs = parser.parse("A1-10east B5-20odd")

        assert len(specs) == 2
        assert specs[0].rotation == 90
        assert specs[1].pages == [5, 7, 9, 11, 13, 15, 17, 19]
