"""Integration tests for core PDF operations"""

import pytest
from pathlib import Path
from pypdf import PdfReader
from pdftk.core import burst, cat, rotate, shuffle
import tempfile
import shutil


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir)


class TestBurst:
    """Test burst operation"""

    def test_burst_basic(self, fixtures_dir, temp_output_dir):
        """Test basic burst operation"""
        input_pdf = fixtures_dir / "10page.pdf"
        page_count = burst(input_pdf, output_dir=temp_output_dir)

        assert page_count == 10

        # Verify all output files exist
        for i in range(1, 11):
            output_file = temp_output_dir / f"pg_{i:04d}.pdf"
            assert output_file.exists()

            # Verify each output has exactly 1 page
            reader = PdfReader(output_file)
            assert len(reader.pages) == 1

    def test_burst_custom_pattern(self, fixtures_dir, temp_output_dir):
        """Test burst with custom output pattern"""
        input_pdf = fixtures_dir / "10page.pdf"
        page_count = burst(
            input_pdf, output_pattern="page_%02d.pdf", output_dir=temp_output_dir
        )

        assert page_count == 10

        # Verify custom pattern was used
        output_file = temp_output_dir / "page_01.pdf"
        assert output_file.exists()


class TestCat:
    """Test cat operation"""

    def test_cat_merge_all(self, fixtures_dir, temp_output_dir):
        """Test merging all pages from multiple PDFs"""
        input_files = {
            "A": fixtures_dir / "1page.pdf",
            "B": fixtures_dir / "10page.pdf",
        }
        output = temp_output_dir / "merged.pdf"

        cat(input_files, [], output)

        # Verify output exists and has correct page count
        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 11  # 1 + 10

    def test_cat_simple_range(self, fixtures_dir, temp_output_dir):
        """Test extracting pages with simple range"""
        input_files = {"A": fixtures_dir / "10page.pdf"}
        output = temp_output_dir / "subset.pdf"

        cat(input_files, ["1-5"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_cat_multiple_ranges(self, fixtures_dir, temp_output_dir):
        """Test multiple page ranges"""
        input_files = {"A": fixtures_dir / "10page.pdf"}
        output = temp_output_dir / "multiple.pdf"

        cat(input_files, ["1-3", "7-9"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 6  # 3 + 3

    def test_cat_with_handles(self, fixtures_dir, temp_output_dir):
        """Test using handle-based references"""
        input_files = {
            "A": fixtures_dir / "10page.pdf",
            "B": fixtures_dir / "20page.pdf",
        }
        output = temp_output_dir / "handles.pdf"

        cat(input_files, ["A1-5", "B1-3"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 8  # 5 + 3

    def test_cat_reverse_range(self, fixtures_dir, temp_output_dir):
        """Test reverse page range"""
        input_files = {"A": fixtures_dir / "10page.pdf"}
        output = temp_output_dir / "reverse.pdf"

        cat(input_files, ["10-1"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 10

    def test_cat_even_odd(self, fixtures_dir, temp_output_dir):
        """Test even/odd qualifiers"""
        input_files = {"A": fixtures_dir / "10page.pdf"}

        # Test even pages
        output_even = temp_output_dir / "even.pdf"
        cat(input_files, ["1-10even"], output_even)
        reader_even = PdfReader(output_even)
        assert len(reader_even.pages) == 5  # 2,4,6,8,10

        # Test odd pages
        output_odd = temp_output_dir / "odd.pdf"
        cat(input_files, ["1-10odd"], output_odd)
        reader_odd = PdfReader(output_odd)
        assert len(reader_odd.pages) == 5  # 1,3,5,7,9

    def test_cat_with_rotation(self, fixtures_dir, temp_output_dir):
        """Test page rotation during cat"""
        input_files = {"A": fixtures_dir / "10page.pdf"}
        output = temp_output_dir / "rotated.pdf"

        cat(input_files, ["1-5east"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 5

        # Verify rotation was applied (rotation is cumulative in pypdf)
        # First page should have rotation
        first_page = reader.pages[0]
        assert first_page.rotation % 360 == 90

    def test_cat_complex_combination(self, fixtures_dir, temp_output_dir):
        """Test complex combination of features"""
        input_files = {
            "A": fixtures_dir / "10page.pdf",
            "B": fixtures_dir / "20page.pdf",
        }
        output = temp_output_dir / "complex.pdf"

        cat(input_files, ["A1-5", "B10-15", "A6-10"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 16  # 5 + 6 + 5

    def test_cat_end_keyword(self, fixtures_dir, temp_output_dir):
        """Test 'end' keyword"""
        input_files = {"A": fixtures_dir / "10page.pdf"}
        output = temp_output_dir / "end.pdf"

        cat(input_files, ["5-end"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 6  # pages 5-10

    def test_cat_reverse_numbering(self, fixtures_dir, temp_output_dir):
        """Test reverse numbering (r1, r2, etc.)"""
        input_files = {"A": fixtures_dir / "10page.pdf"}
        output = temp_output_dir / "rlast.pdf"

        cat(input_files, ["r3-r1"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 3  # last 3 pages


class TestRotate:
    """Test rotate operation"""

    def test_rotate_single_page(self, fixtures_dir, temp_output_dir):
        """Test rotating a single page"""
        input_file = fixtures_dir / "10page.pdf"
        output = temp_output_dir / "rotated.pdf"

        rotate(input_file, ["1east"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 10  # All pages preserved

        # First page should be rotated
        assert reader.pages[0].rotation % 360 == 90

        # Other pages should not be rotated
        assert reader.pages[1].rotation % 360 == 0

    def test_rotate_range(self, fixtures_dir, temp_output_dir):
        """Test rotating a range of pages"""
        input_file = fixtures_dir / "10page.pdf"
        output = temp_output_dir / "range_rotated.pdf"

        rotate(input_file, ["1-5south"], output)

        assert output.exists()
        reader = PdfReader(output)

        # First 5 pages should be rotated 180°
        for i in range(5):
            assert reader.pages[i].rotation % 360 == 180

        # Remaining pages should not be rotated
        for i in range(5, 10):
            assert reader.pages[i].rotation % 360 == 0

    def test_rotate_multiple_ranges(self, fixtures_dir, temp_output_dir):
        """Test rotating multiple ranges with different rotations"""
        input_file = fixtures_dir / "10page.pdf"
        output = temp_output_dir / "multi_rotated.pdf"

        rotate(input_file, ["1-3east", "7-9west"], output)

        assert output.exists()
        reader = PdfReader(output)

        # Pages 1-3 should be 90°
        for i in range(3):
            assert reader.pages[i].rotation % 360 == 90

        # Pages 4-6 should be 0°
        for i in range(3, 6):
            assert reader.pages[i].rotation % 360 == 0

        # Pages 7-9 should be 270°
        for i in range(6, 9):
            assert reader.pages[i].rotation % 360 == 270

    def test_rotate_all_directions(self, fixtures_dir, temp_output_dir):
        """Test all rotation directions"""
        input_file = fixtures_dir / "10page.pdf"

        # Test each rotation direction
        rotations = {
            "north": 0,
            "east": 90,
            "south": 180,
            "west": 270,
            "right": 90,
            "down": 180,
            "left": -90,  # -90 = 270
        }

        for direction, expected_rotation in rotations.items():
            output = temp_output_dir / f"rotate_{direction}.pdf"
            rotate(input_file, [f"1{direction}"], output)

            reader = PdfReader(output)
            actual_rotation = reader.pages[0].rotation % 360
            expected_normalized = expected_rotation % 360

            assert actual_rotation == expected_normalized


class TestShuffle:
    """Test shuffle operation"""

    def test_shuffle_two_files(self, fixtures_dir, temp_output_dir):
        """Test basic shuffle of two files"""
        input_files = {
            "A": fixtures_dir / "10page.pdf",
            "B": fixtures_dir / "10page.pdf",
        }
        output = temp_output_dir / "shuffled.pdf"

        shuffle(input_files, ["A1-5", "B1-5"], output)

        assert output.exists()
        reader = PdfReader(output)
        # Should alternate: A1, B1, A2, B2, A3, B3, A4, B4, A5, B5
        assert len(reader.pages) == 10

    def test_shuffle_reverse(self, fixtures_dir, temp_output_dir):
        """Test shuffle with reverse range"""
        input_files = {
            "A": fixtures_dir / "10page.pdf",
            "B": fixtures_dir / "10page.pdf",
        }
        output = temp_output_dir / "shuffle_reverse.pdf"

        shuffle(input_files, ["A1-5", "B5-1"], output)

        assert output.exists()
        reader = PdfReader(output)
        # Should alternate: A1, B5, A2, B4, A3, B3, A4, B2, A5, B1
        assert len(reader.pages) == 10

    def test_shuffle_unequal_lengths(self, fixtures_dir, temp_output_dir):
        """Test shuffle with unequal page counts"""
        input_files = {
            "A": fixtures_dir / "10page.pdf",
            "B": fixtures_dir / "10page.pdf",
        }
        output = temp_output_dir / "shuffle_unequal.pdf"

        # A has 3 pages, B has 7 pages
        shuffle(input_files, ["A1-3", "B1-7"], output)

        assert output.exists()
        reader = PdfReader(output)
        # Should be: A1, B1, A2, B2, A3, B3, B4, B5, B6, B7
        assert len(reader.pages) == 10

    def test_shuffle_all_pages(self, fixtures_dir, temp_output_dir):
        """Test shuffle using handle only (all pages)"""
        input_files = {"A": fixtures_dir / "1page.pdf", "B": fixtures_dir / "1page.pdf"}
        output = temp_output_dir / "shuffle_all.pdf"

        shuffle(input_files, ["A", "B"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 2

    def test_shuffle_with_rotation(self, fixtures_dir, temp_output_dir):
        """Test shuffle with rotation"""
        input_files = {
            "A": fixtures_dir / "10page.pdf",
            "B": fixtures_dir / "10page.pdf",
        }
        output = temp_output_dir / "shuffle_rotated.pdf"

        shuffle(input_files, ["A1-3east", "B1-3"], output)

        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 6

        # Pages from A (even indices in round-robin) should be rotated
        assert reader.pages[0].rotation % 360 == 90  # A1
        assert reader.pages[1].rotation % 360 == 0  # B1
        assert reader.pages[2].rotation % 360 == 90  # A2
        assert reader.pages[3].rotation % 360 == 0  # B2


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_cat_empty_ranges_single_file(self, fixtures_dir, temp_output_dir):
        """Test cat with empty ranges and single file"""
        input_files = {"A": fixtures_dir / "10page.pdf"}
        output = temp_output_dir / "all.pdf"

        cat(input_files, [], output)

        reader = PdfReader(output)
        assert len(reader.pages) == 10

    def test_cat_single_page_pdf(self, fixtures_dir, temp_output_dir):
        """Test cat with single page PDF"""
        input_files = {"A": fixtures_dir / "1page.pdf"}
        output = temp_output_dir / "single.pdf"

        cat(input_files, ["1"], output)

        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_rotate_no_rotation_specified(self, fixtures_dir, temp_output_dir):
        """Test rotate with pages but no rotation keyword"""
        input_file = fixtures_dir / "10page.pdf"
        output = temp_output_dir / "no_rotation.pdf"

        # Pages without rotation keywords should remain unrotated
        rotate(input_file, ["1-5"], output)

        reader = PdfReader(output)
        for i in range(10):
            assert reader.pages[i].rotation % 360 == 0
