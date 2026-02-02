"""Generate test PDFs with labeled pages for testing multi-file operations"""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_labeled_pdf(filename: str, prefix: str, num_pages: int = 10):
    """Generate a PDF with labeled pages

    Args:
        filename: Output PDF filename
        prefix: Prefix for page labels (e.g., 'a', 'b')
        num_pages: Number of pages to generate
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    for i in range(1, num_pages + 1):
        # Add large centered text with page label
        label = f"{prefix}{i}"
        c.setFont("Helvetica-Bold", 72)
        text_width = c.stringWidth(label, "Helvetica-Bold", 72)
        x = (width - text_width) / 2
        y = height / 2
        c.drawString(x, y, label)

        # Add smaller text at bottom
        c.setFont("Helvetica", 12)
        info = f"File: {filename} | Page: {i}"
        c.drawString(50, 50, info)

        c.showPage()

    c.save()
    print(f"Created {filename} with {num_pages} pages labeled {prefix}1-{prefix}{num_pages}")


if __name__ == "__main__":
    # Generate test PDFs
    generate_labeled_pdf("a.pdf", "a", 10)
    generate_labeled_pdf("b.pdf", "b", 10)
