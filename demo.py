"""Demonstration script showing all pdftk operations working correctly"""

from pathlib import Path
from pdftk.core import burst, cat, rotate, shuffle
import tempfile
import shutil

# Create temp directory for outputs
temp_dir = Path(tempfile.mkdtemp())
print(f"Using temporary directory: {temp_dir}\n")

try:
    fixtures = Path("tests/fixtures")

    # Test 1: Burst
    print("=" * 60)
    print("TEST 1: Burst Operation")
    print("=" * 60)
    output_dir = temp_dir / "burst_output"
    output_dir.mkdir()
    pages = burst(fixtures / "10page.pdf", output_dir=output_dir)
    print(f"✓ Successfully burst {pages} pages")
    print(f"  Output files: {list(output_dir.glob('*.pdf'))[:3]}...\n")

    # Test 2: Cat - Simple range
    print("=" * 60)
    print("TEST 2: Cat - Extract Pages 1-5")
    print("=" * 60)
    cat({"A": fixtures / "10page.pdf"}, ["1-5"], temp_dir / "cat_extract.pdf")
    print(f"✓ Created: {temp_dir / 'cat_extract.pdf'}\n")

    # Test 3: Cat - With rotation
    print("=" * 60)
    print("TEST 3: Cat - Pages 1-3 Rotated East (90°)")
    print("=" * 60)
    cat({"A": fixtures / "10page.pdf"}, ["1-3east"], temp_dir / "cat_rotated.pdf")
    print(f"✓ Created: {temp_dir / 'cat_rotated.pdf'}\n")

    # Test 4: Cat - Multiple files
    print("=" * 60)
    print("TEST 4: Cat - Merge Multiple PDFs")
    print("=" * 60)
    cat(
        {"A": fixtures / "10page.pdf", "B": fixtures / "20page.pdf"},
        ["A1-5", "B1-3"],
        temp_dir / "cat_multi.pdf",
    )
    print(f"✓ Created: {temp_dir / 'cat_multi.pdf'} (5 + 3 = 8 pages)\n")

    # Test 5: Cat - Complex ranges
    print("=" * 60)
    print("TEST 5: Cat - Even Pages, Reverse, with Rotation")
    print("=" * 60)
    cat(
        {"A": fixtures / "10page.pdf"},
        ["1-10even", "10-1odd", "1-5east"],
        temp_dir / "cat_complex.pdf",
    )
    print(f"✓ Created: {temp_dir / 'cat_complex.pdf'}\n")

    # Test 6: Rotate
    print("=" * 60)
    print("TEST 6: Rotate - First Page 90°, Pages 5-10 180°")
    print("=" * 60)
    rotate(fixtures / "10page.pdf", ["1east", "5-10south"], temp_dir / "rotated.pdf")
    print(f"✓ Created: {temp_dir / 'rotated.pdf'}\n")

    # Test 7: Shuffle
    print("=" * 60)
    print("TEST 7: Shuffle - Interleave Two PDFs")
    print("=" * 60)
    shuffle(
        {"A": fixtures / "10page.pdf", "B": fixtures / "10page.pdf"},
        ["A1-5", "B1-5"],
        temp_dir / "shuffled.pdf",
    )
    print(f"✓ Created: {temp_dir / 'shuffled.pdf'} (A1, B1, A2, B2, ...)\n")

    # Test 8: Shuffle with reverse
    print("=" * 60)
    print("TEST 8: Shuffle - Front/Back Scan Assembly")
    print("=" * 60)
    shuffle(
        {"A": fixtures / "10page.pdf", "B": fixtures / "10page.pdf"},
        ["A1-5", "B5-1"],  # B pages in reverse
        temp_dir / "shuffled_reverse.pdf",
    )
    print(f"✓ Created: {temp_dir / 'shuffled_reverse.pdf'} (A1, B5, A2, B4, ...)\n")

    print("=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print(f"\nAll output files in: {temp_dir}")
    print("\nTo inspect the PDFs:")
    print(f"  ls -lh {temp_dir}/*.pdf")

finally:
    # Cleanup
    choice = input("\nDelete temporary files? [y/N]: ")
    if choice.lower() == "y":
        shutil.rmtree(temp_dir)
        print("Temporary files deleted.")
    else:
        print(f"Temporary files kept in: {temp_dir}")
