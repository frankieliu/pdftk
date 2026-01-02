"""Tests for utility functions"""

import pytest
from pathlib import Path
from pdftk.utils import parse_input_files, validate_pdf_exists
import tempfile


class TestParseInputFiles:
    """Test parse_input_files function"""

    def test_parse_with_handles(self):
        """Test parsing files with handle syntax"""
        inputs = ["A=file1.pdf", "B=file2.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {"A": Path("file1.pdf"), "B": Path("file2.pdf")}
        assert files == [Path("file1.pdf"), Path("file2.pdf")]

    def test_parse_without_handles(self):
        """Test parsing files without handles"""
        inputs = ["file1.pdf", "file2.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {}
        assert files == [Path("file1.pdf"), Path("file2.pdf")]

    def test_parse_mixed(self):
        """Test parsing mix of files with and without handles"""
        inputs = ["A=file1.pdf", "file2.pdf", "B=file3.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {"A": Path("file1.pdf"), "B": Path("file3.pdf")}
        assert files == [Path("file1.pdf"), Path("file2.pdf"), Path("file3.pdf")]

    def test_parse_single_file(self):
        """Test parsing single file"""
        inputs = ["input.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {}
        assert files == [Path("input.pdf")]

    def test_parse_single_file_with_handle(self):
        """Test parsing single file with handle"""
        inputs = ["A=input.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {"A": Path("input.pdf")}
        assert files == [Path("input.pdf")]

    def test_parse_empty_list(self):
        """Test parsing empty input list"""
        inputs = []
        handles, files = parse_input_files(inputs)

        assert handles == {}
        assert files == []

    def test_handle_uppercase_conversion(self):
        """Test that handles are converted to uppercase"""
        inputs = ["a=file1.pdf", "b=file2.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {"A": Path("file1.pdf"), "B": Path("file2.pdf")}

    def test_handle_with_equals_in_filename(self):
        """Test parsing when filename contains equals sign"""
        inputs = ["A=file=with=equals.pdf"]
        handles, files = parse_input_files(inputs)

        # Should split only on first equals
        assert handles == {"A": Path("file=with=equals.pdf")}
        assert files == [Path("file=with=equals.pdf")]

    def test_parse_with_paths(self):
        """Test parsing with directory paths"""
        inputs = ["A=/path/to/file1.pdf", "B=../relative/file2.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {
            "A": Path("/path/to/file1.pdf"),
            "B": Path("../relative/file2.pdf"),
        }
        assert files == [Path("/path/to/file1.pdf"), Path("../relative/file2.pdf")]

    def test_multiple_letter_handles(self):
        """Test handles with multiple letters"""
        inputs = ["AB=file1.pdf", "XYZ=file2.pdf"]
        handles, files = parse_input_files(inputs)

        assert handles == {"AB": Path("file1.pdf"), "XYZ": Path("file2.pdf")}


class TestValidatePdfExists:
    """Test validate_pdf_exists function"""

    def test_valid_pdf_exists(self):
        """Test validation of existing PDF file"""
        # Use test fixture
        pdf_path = Path(__file__).parent / "fixtures" / "1page.pdf"

        # Should not raise any exception
        validate_pdf_exists(pdf_path)

    def test_file_not_found(self):
        """Test validation of non-existent file"""
        pdf_path = Path("/nonexistent/file.pdf")

        with pytest.raises(FileNotFoundError, match="PDF file not found"):
            validate_pdf_exists(pdf_path)

    def test_non_pdf_file(self):
        """Test validation of non-PDF file"""
        # Create a temporary non-PDF file
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="File is not a PDF"):
                validate_pdf_exists(temp_path)
        finally:
            temp_path.unlink()

    def test_pdf_extension_case_insensitive(self):
        """Test that PDF extension check is case-insensitive"""
        # Use test fixture and test it works
        pdf_path = Path(__file__).parent / "fixtures" / "1page.pdf"
        validate_pdf_exists(pdf_path)

        # Test uppercase extension would also work
        with tempfile.NamedTemporaryFile(suffix=".PDF", delete=False) as f:
            temp_path = Path(f.name)
            # Write minimal PDF content
            f.write(b"%PDF-1.4\n")

        try:
            # Should not raise ValueError for .PDF extension
            validate_pdf_exists(temp_path)
        except FileNotFoundError:
            # This is expected since it's not a real PDF
            pass
        finally:
            temp_path.unlink()

    def test_file_without_extension(self):
        """Test validation of file without extension"""
        # Create temporary file without extension
        with tempfile.NamedTemporaryFile(delete=False, suffix="") as f:
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="File is not a PDF"):
                validate_pdf_exists(temp_path)
        finally:
            temp_path.unlink()


class TestIntegration:
    """Integration tests combining multiple utility functions"""

    def test_parse_and_validate_workflow(self):
        """Test typical workflow of parsing and validating inputs"""
        fixtures_dir = Path(__file__).parent / "fixtures"

        inputs = [
            f'A={fixtures_dir / "10page.pdf"}',
            f'B={fixtures_dir / "20page.pdf"}',
        ]

        # Parse inputs
        handles, files = parse_input_files(inputs)

        # Validate all files
        for file in files:
            validate_pdf_exists(file)

        # Should complete without errors
        assert len(handles) == 2
        assert len(files) == 2

    def test_parse_and_validate_with_invalid_file(self):
        """Test workflow with invalid file"""
        inputs = ["A=nonexistent.pdf"]

        handles, files = parse_input_files(inputs)

        # Validation should fail
        with pytest.raises(FileNotFoundError):
            for file in files:
                validate_pdf_exists(file)
