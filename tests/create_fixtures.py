"""Create test PDF fixtures for testing"""

from pypdf import PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def create_numbered_pdf(num_pages: int, output: Path):
    """Create a PDF with numbered pages for testing

    Args:
        num_pages: Number of pages to create
        output: Output PDF path
    """
    writer = PdfWriter()

    for i in range(1, num_pages + 1):
        # Create temporary page
        temp_file = f"/tmp/pdftk_test_page_{i}.pdf"
        c = canvas.Canvas(temp_file, pagesize=letter)

        # Draw page number
        c.setFont("Helvetica", 48)
        c.drawString(200, 400, f"Page {i}")

        # Draw smaller text at bottom
        c.setFont("Helvetica", 12)
        c.drawString(50, 50, f"Test PDF - Page {i} of {num_pages}")

        c.save()

        # Add to writer
        from pypdf import PdfReader

        reader = PdfReader(temp_file)
        writer.add_page(reader.pages[0])

        # Clean up temp file
        os.remove(temp_file)

    # Write output
    with open(output, "wb") as f:
        writer.write(f)

    print(f"Created: {output} ({num_pages} pages)")


def main():
    """Create all test fixtures"""
    FIXTURES_DIR.mkdir(exist_ok=True)

    # Create test PDFs with different page counts
    create_numbered_pdf(1, FIXTURES_DIR / "1page.pdf")
    create_numbered_pdf(10, FIXTURES_DIR / "10page.pdf")
    create_numbered_pdf(20, FIXTURES_DIR / "20page.pdf")

    print(f"\nTest fixtures created in {FIXTURES_DIR}")


if __name__ == "__main__":
    main()
