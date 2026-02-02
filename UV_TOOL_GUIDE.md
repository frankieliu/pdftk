# UV Tool Management Guide

## Current Installation Status

Your `pdftk` tool is installed in **editable mode** from:
```
/Users/frankliu/Library/CloudStorage/Box-Box/Work/pdftk
```

This means changes to the source code are automatically available without reinstalling.

## UV Tool Commands

### View Installed Tools
```bash
uv tool list
```

### Install a Tool

**From PyPI:**
```bash
uv tool install pdftk-python
```

**From local source (editable mode):**
```bash
uv tool install --editable /path/to/pdftk
```

**From local source (non-editable):**
```bash
uv tool install /path/to/pdftk
```

### Update a Tool

**Update from PyPI:**
```bash
uv tool upgrade pdftk-python
```

**Reinstall from local source (if you made changes):**
```bash
# Force reinstall in editable mode
uv tool install --force --editable ~/Library/CloudStorage/Box-Box/Work/pdftk

# Or reinstall from current directory
cd ~/Library/CloudStorage/Box-Box/Work/pdftk
uv tool install --force --editable .
```

### Uninstall a Tool
```bash
uv tool uninstall pdftk-python
```

### Check Tool Info
```bash
# View where tool is installed
which pdftk

# View tool receipt (installation details)
cat ~/.local/share/uv/tools/pdftk-python/uv-receipt.toml

# List all uv tools
ls ~/.local/share/uv/tools/
```

## Your Current Setup

Since your installation is **editable**, you don't need to reinstall after making code changes:

1. ✅ Edit source files in `~/Library/CloudStorage/Box-Box/Work/pdftk/src/`
2. ✅ Changes are immediately available when running `pdftk`
3. ❌ No reinstall needed

**Exception**: If you change `pyproject.toml` (dependencies, entry points, etc.), you may need to reinstall:
```bash
uv tool install --force --editable ~/Library/CloudStorage/Box-Box/Work/pdftk
```

## Testing Your Installation

```bash
# Verify pdftk is accessible
which pdftk

# Check version
pdftk --version

# Test help with new examples
pdftk cat --help

# Test actual functionality
cd /tmp
pdftk cat ~/path/to/file.pdf -o output.pdf -r 1-5
```

## How It Works

```
Source Code (editable)
~/Library/CloudStorage/Box-Box/Work/pdftk/
    ↓ (symlinked via editable install)
Tool Environment
~/.local/share/uv/tools/pdftk-python/
    ↓ (creates executable)
Executable Symlink
~/.local/bin/pdftk
    ↓ (in your PATH)
Available globally as `pdftk` command
```

## Publishing vs Local Development

**Local Development (current setup):**
- Editable install: Changes immediately available
- Use: `uv tool install --editable .`

**After Publishing to PyPI:**
- Users install from PyPI: `uv tool install pdftk-python`
- Users get updates with: `uv tool upgrade pdftk-python`

## Quick Reference

| Task | Command |
|------|---------|
| Install editable (dev) | `uv tool install --editable .` |
| Install from PyPI | `uv tool install pdftk-python` |
| Update from PyPI | `uv tool upgrade pdftk-python` |
| Reinstall editable | `uv tool install --force --editable .` |
| Uninstall | `uv tool uninstall pdftk-python` |
| List tools | `uv tool list` |
| Check location | `which pdftk` |
