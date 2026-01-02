# Announcement Drafts for pdftk-python v0.1.0

## Reddit - r/Python

**Title:** [Release] pdftk-python v0.1.0 - A Python implementation of PDF Toolkit

**Body:**
I'm excited to release pdftk-python v0.1.0, a Python implementation of the classic pdftk (PDF Toolkit) for manipulating PDF documents.

**What it does:**
- Split PDFs into individual pages (burst)
- Merge/concatenate PDFs with advanced page selection (cat)
- Rotate specific pages (rotate)
- Collate pages from multiple PDFs (shuffle)

**Why I built it:**
The original pdftk is a powerful tool, but it requires Java and isn't always easy to install. I wanted a pure Python solution that's easy to `pip install` and use both from CLI and as a library.

**Features:**
- 🎯 Full pdftk page range syntax (1-5, end, r1, even/odd, rotation, handles)
- 🐍 Python 3.9+ compatible
- ✅ 80 tests, fully typed (mypy), formatted (black)
- 📦 Zero C dependencies (pure Python with pypdf)
- 🚀 Fast and lightweight

**Installation:**
```bash
pip install pdftk-python
```

**Quick Examples:**
```bash
# Split PDF into pages
pdftk burst document.pdf

# Extract pages 1-5
pdftk cat input.pdf -o output.pdf -r 1-5

# Rotate pages
pdftk rotate input.pdf -o output.pdf -r 1east 5-10south

# Merge with page selection
pdftk cat A=doc1.pdf B=doc2.pdf -o merged.pdf -r A1-10 B5-15
```

**Status:** Beta - All core features working and tested

**Links:**
- GitHub: https://github.com/frankieliu/pdftk
- PyPI: https://pypi.org/project/pdftk-python/

Would love feedback! Next planned features: watermarking, metadata editing, and form filling.

---

## Hacker News

**Title:** Pdftk-python – A Python implementation of PDF Toolkit

**URL:** https://github.com/frankieliu/pdftk

**Comment (if discussion starts):**

I'm the author - happy to answer questions!

The main goal was to make PDF manipulation easy and Pythonic. The original pdftk is great but requires Java. This version is pure Python, easy to install, and works as both a CLI tool and a library.

The most complex part was implementing the page range parser - pdftk has a sophisticated syntax for selecting pages (ranges, even/odd, reverse numbering, rotation). I built a comprehensive parser with 39 tests covering all the edge cases.

Future plans include watermarking, form filling, and metadata operations.

---

## Twitter/X

**Thread:**

🎉 Just released pdftk-python v0.1.0 - A pure Python implementation of PDF Toolkit!

Split, merge, rotate, and shuffle PDFs from the command line or Python.

pip install pdftk-python

🧵 1/4

---

Key features:
✅ Split PDFs (burst)
✅ Merge with page ranges (cat)
✅ Rotate pages (rotate)
✅ Collate pages (shuffle)
✅ Full pdftk page syntax
✅ 80 tests, fully typed

2/4

---

Why build this? The original pdftk requires Java. I wanted something that's:
- Pure Python
- Easy pip install
- Works as CLI & library
- Zero C dependencies

Perfect for scripts, automation, and CLI workflows! 🚀

3/4

---

Examples:
```bash
# Split PDF
pdftk burst doc.pdf

# Extract pages
pdftk cat in.pdf -o out.pdf -r 1-5

# Rotate
pdftk rotate in.pdf -o out.pdf -r 1east
```

GitHub: github.com/frankieliu/pdftk
PyPI: pypi.org/project/pdftk-python

Feedback welcome! 🙏

4/4

---

## Mastodon

**Post:**

🎉 Released pdftk-python v0.1.0! 🐍

A pure Python implementation of PDF Toolkit for manipulating PDFs from the command line.

Features:
📄 Split PDFs into pages
🔀 Merge with advanced page selection
🔄 Rotate specific pages
📚 Collate pages from multiple PDFs

pip install pdftk-python

✅ 80 tests
✅ Fully typed
✅ Zero C dependencies

Perfect for #Python automation!

https://github.com/frankieliu/pdftk

#Release #OpenSource #PDFTools

---

## Product Hunt (Future)

**Tagline:** A Python implementation of PDF Toolkit - split, merge, rotate PDFs

**Description:**
pdftk-python brings the power of the classic pdftk to the Python ecosystem. Manipulate PDF documents from the command line or Python scripts without Java dependencies.

**Features:**
• Split PDFs into individual pages
• Merge multiple PDFs with advanced page selection
• Rotate specific pages or page ranges
• Collate pages from multiple inputs
• Full pdftk page range syntax support
• Works as both CLI tool and Python library

**Perfect for:**
- Document automation workflows
- PDF processing pipelines
- Batch operations on PDFs
- CLI enthusiasts

**Tech Stack:** Python 3.9+, pypdf, argparse

**Made by:** Solo developer, open source (MIT License)

---

## Dev.to

**Title:** Introducing pdftk-python: A Pure Python PDF Toolkit

**Tags:** python, opensource, cli, pdf

**Article:**

# Introducing pdftk-python: A Pure Python PDF Toolkit

I'm excited to announce the release of pdftk-python v0.1.0 - a pure Python implementation of the classic PDF Toolkit!

## The Problem

PDF manipulation is a common task in automation workflows. The original pdftk is powerful but requires Java, which can be a barrier for Python-centric projects. While libraries like PyPDF2/pypdf exist, they don't provide the convenient CLI interface that pdftk offers.

## The Solution

pdftk-python brings pdftk's functionality to Python with:

- **Pure Python**: No Java, no C extensions
- **Easy Install**: `pip install pdftk-python`
- **Dual Interface**: CLI tool + Python API
- **Full Compatibility**: Supports pdftk's page range syntax

## What Can It Do?

### Burst - Split into Individual Pages
```bash
pdftk burst document.pdf
```

### Cat - Merge with Page Selection
```bash
pdftk cat A=doc1.pdf B=doc2.pdf -o merged.pdf -r A1-10 B5-15
```

### Rotate - Rotate Specific Pages
```bash
pdftk rotate input.pdf -o output.pdf -r 1east 5-10south
```

### Shuffle - Collate Pages
```bash
pdftk shuffle A=front.pdf B=back.pdf -o book.pdf -r A Bend-1
```

## Technical Highlights

### Page Range Parser
The most challenging part was implementing pdftk's sophisticated page range syntax:
- Ranges (1-5, 10-20)
- Reverse (10-1)
- Keywords (end, r1, rend)
- Qualifiers (even, odd)
- Rotation (north, east, south, west)

I built a comprehensive parser with 39 tests covering all edge cases.

### Code Quality
- ✅ 80 tests (100% core functionality covered)
- ✅ Fully type-hinted with mypy
- ✅ Formatted with black
- ✅ CI/CD with GitHub Actions

## Installation

```bash
pip install pdftk-python
```

## What's Next?

Phase 2 features planned:
- Watermarking and stamps
- Metadata editing
- Form filling
- Encryption/security

## Try It Out!

- **GitHub**: https://github.com/frankieliu/pdftk
- **PyPI**: https://pypi.org/project/pdftk-python/

I'd love your feedback! Feel free to open issues or contribute on GitHub.

---

*Built with Python 3.9+, pypdf, and a lot of ☕*

---

## LinkedIn

**Post:**

🚀 Excited to announce the release of pdftk-python v0.1.0!

After 4 weeks of development, I've built a pure Python implementation of the classic PDF Toolkit. This brings powerful PDF manipulation capabilities to Python developers without Java dependencies.

Key achievements:
✅ 4 core operations (burst, cat, rotate, shuffle)
✅ 80 comprehensive tests
✅ Full type safety (mypy)
✅ CI/CD pipeline
✅ Production-ready code quality

The most challenging part was implementing pdftk's sophisticated page range parser - a mini language for selecting, rotating, and manipulating PDF pages.

Perfect for:
📊 Document automation
🔄 PDF processing pipelines
🤖 Batch operations
⚙️ CLI workflows

Check it out: https://github.com/frankieliu/pdftk

#Python #OpenSource #SoftwareDevelopment #PDFAutomation #CLI

---

*Feel free to customize these announcements based on your personal style and the specific platform guidelines!*
