"""Test multi-PDF operations with verification"""

from pypdf import PdfReader


def verify_test_results():
    """Verify all test PDF outputs are correct"""

    tests = [
        {
            "file": "test1.pdf",
            "ranges": "A1-3 B5 B7",
            "expected_pages": 5,
            "description": "Extract pages 1-3 from a.pdf and pages 5, 7 from b.pdf",
        },
        {
            "file": "test2.pdf",
            "ranges": "A1-3 A10 B5 B7 B8-10",
            "expected_pages": 9,
            "description": "Multiple ranges from each file",
        },
        {
            "file": "test3.pdf",
            "ranges": "A1-3east B5 B7",
            "expected_pages": 5,
            "description": "With rotation (A1-3 rotated 90° clockwise)",
        },
        {
            "file": "test4.pdf",
            "ranges": "A1-10even B5-10odd",
            "expected_pages": 8,
            "description": "Even pages from A, odd pages from B",
        },
    ]

    print("Multi-PDF Operation Test Results")
    print("=" * 70)

    all_passed = True
    for test in tests:
        try:
            reader = PdfReader(test["file"])
            actual = len(reader.pages)
            expected = test["expected_pages"]
            passed = actual == expected
            all_passed = all_passed and passed

            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"\n{status}: {test['file']}")
            print(f"  Description: {test['description']}")
            print(f"  Ranges: {test['ranges']}")
            print(f"  Pages: {actual} (expected {expected})")

        except Exception as e:
            print(f"\n✗ ERROR: {test['file']}")
            print(f"  Error: {e}")
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")

    return all_passed


if __name__ == "__main__":
    verify_test_results()
