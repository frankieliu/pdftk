# PDFTK(1)

## NAME

**pdftk** - PDF Toolkit - manipulate PDF documents

## SYNOPSIS

```
pdftk <input PDF files | - | PROMPT>
      [input_pw <input PDF owner passwords | PROMPT>]
      [<operation> <operation arguments>]
      [output <output filename | - | PROMPT>]
      [encrypt_40bit | encrypt_128bit]
      [allow <permissions>]
      [owner_pw <owner password | PROMPT>]
      [user_pw <user password | PROMPT>]
      [flatten] [need_appearances]
      [compress | uncompress]
      [keep_first_id | keep_final_id]
      [drop_xfa]
      [verbose]
      [dont_ask | do_ask]
```

Where `<operation>` can be:
```
cat | shuffle | burst | rotate |
generate_fdf | fill_form |
background | multibackground |
stamp | multistamp |
dump_data | dump_data_utf8 |
dump_data_fields | dump_data_fields_utf8 |
dump_data_annots |
update_info | update_info_utf8 |
attach_files | unpack_files
```

## DESCRIPTION

**pdftk** is a command-line tool for manipulating PDF documents. It can merge, split, rotate, encrypt, decrypt, fill forms, apply watermarks, and much more.

If no operation is specified, pdftk runs in **filter mode**, taking a single PDF input and creating a new PDF after applying output options like encryption and compression.

## INPUT FILES

### Basic Input

```
pdftk input.pdf [operation] output output.pdf
```

Use `-` to pass a PDF via stdin:
```
cat input.pdf | pdftk - cat output output.pdf
```

### Input with Handles

Associate input files with handles (one or more uppercase letters):
```
pdftk A=input1.pdf B=input2.pdf cat A1-3 B output combined.pdf
```

Handles are useful for:
- Specifying page ranges from different PDFs
- Associating passwords with specific files
- Referencing files in operations

## PASSWORDS

### Syntax

```
input_pw <handle>=<password>
```

### Password Rules

- Most features require the **owner password** for encrypted PDFs
- If no owner password exists, provide the **user password**
- If no password is needed, omit this option
- Passwords without handles are matched to input files by order

### Example

```
pdftk A=secure1.pdf B=secure2.pdf input_pw A=pass1 B=pass2 cat output out.pdf
```

In `do_ask` mode, pdftk prompts for passwords if incorrect or missing.

## OPERATIONS

### cat [<page ranges>]

Concatenate pages from input PDFs.

**Page Range Syntax:**
```
[<handle>][<start>[-<end>[<qualifier>]]][<rotation>]
```

**Qualifiers:**
- `even` - Even-numbered pages only
- `odd` - Odd-numbered pages only

**Rotations:**
- `north` - 0° (no rotation)
- `east` - 90° clockwise
- `south` - 180°
- `west` - 270° clockwise
- `left` - -90° relative
- `right` - +90° relative
- `down` - +180° relative

**Special Keywords:**
- `end` - Last page of document
- `r<N>` - Reverse page numbering (r1 = last page, rend = first page)

**Examples:**
```bash
# Merge all PDFs in order
pdftk *.pdf cat output combined.pdf

# Extract specific pages
pdftk input.pdf cat 1-3 5 7-9 output subset.pdf

# Rotate entire document 90° clockwise
pdftk input.pdf cat 1-endeast output rotated.pdf

# Combine with handles
pdftk A=in1.pdf B=in2.pdf cat A1-10 B5-15 A20 output out.pdf

# Even pages only, rotated
pdftk input.pdf cat 1-endeven west output even_rotated.pdf

# Reverse order
pdftk input.pdf cat end-1 output reversed.pdf

# Interleave two PDFs
pdftk A=doc1.pdf B=doc2.pdf cat A B output interleaved.pdf
```

### shuffle [<page ranges>]

Collate pages by taking one page at a time from each range. Useful for collating scanned documents.

**Examples:**
```bash
# Shuffle two PDFs alternating pages
pdftk A=odd.pdf B=even.pdf shuffle A B output collated.pdf

# Perfect binding - combine front and back scans
pdftk A=front.pdf B=back.pdf shuffle A Bend-1 output book.pdf
```

### burst

Split a single PDF into individual page files. Creates `doc_data.txt` with metadata.

**Default naming:** `pg_0001.pdf`, `pg_0002.pdf`, etc.

**Examples:**
```bash
# Basic burst
pdftk input.pdf burst

# Custom naming with printf format
pdftk input.pdf burst output page_%02d.pdf

# Burst with encryption
pdftk input.pdf burst owner_pw secretpass
```

### rotate [<page ranges>]

Rotate specific pages without changing page order.

**Examples:**
```bash
# Rotate first page 90° clockwise
pdftk input.pdf rotate 1east output rotated.pdf

# Rotate pages 3-5 180°
pdftk input.pdf rotate 3-5south output rotated.pdf

# Rotate even pages left, odd pages right
pdftk input.pdf rotate 1-endeven left 1-endodd right output rotated.pdf
```

### generate_fdf

Extract form field data from a PDF to an FDF file.

**Example:**
```bash
pdftk form.pdf generate_fdf output data.fdf
```

### fill_form <FDF/XFDF file | - | PROMPT>

Fill PDF form fields with data from FDF/XFDF file or stdin.

**Examples:**
```bash
# Fill form from FDF file
pdftk form.pdf fill_form data.fdf output filled.pdf

# Fill and flatten
pdftk form.pdf fill_form data.fdf output filled.pdf flatten

# Fill from stdin
cat data.fdf | pdftk form.pdf fill_form - output filled.pdf
```

**Notes:**
- Supports Rich Text formatted data
- Use `flatten` to merge form data with pages
- Use `need_appearances` for non-ASCII text

### background <background PDF | - | PROMPT>

Apply PDF as background (watermark behind content). Uses only first page of background PDF.

**Example:**
```bash
pdftk document.pdf background watermark.pdf output watermarked.pdf
```

**Note:** Input PDF must have transparent background for watermark to show through.

### multibackground <background PDF | - | PROMPT>

Like `background`, but applies each page of background PDF to corresponding input page. Final background page repeats if needed.

**Example:**
```bash
pdftk slides.pdf multibackground headers.pdf output branded.pdf
```

### stamp <stamp PDF | - | PROMPT>

Overlay stamp PDF on top of input pages. Works best with transparent backgrounds.

**Example:**
```bash
pdftk document.pdf stamp approved.pdf output stamped.pdf
```

### multistamp <stamp PDF | - | PROMPT>

Like `stamp`, but applies each stamp page to corresponding input page.

**Example:**
```bash
pdftk report.pdf multistamp pagenumbers.pdf output numbered.pdf
```

### dump_data

Extract metadata, bookmarks, page metrics to stdout or file. Non-ASCII encoded as XML entities.

**Example:**
```bash
pdftk input.pdf dump_data output metadata.txt
```

### dump_data_utf8

Same as `dump_data` but with UTF-8 encoding.

### dump_data_fields

Report form field statistics.

**Example:**
```bash
pdftk form.pdf dump_data_fields output fields.txt
```

### dump_data_fields_utf8

Same as `dump_data_fields` but with UTF-8 encoding.

### dump_data_annots

Report annotation information (currently links only).

### update_info <info file | - | PROMPT>

Update PDF metadata and bookmarks from data file (same format as `dump_data` output).

**Example:**
```bash
pdftk input.pdf update_info metadata.txt output updated.pdf
```

### update_info_utf8 <info file | - | PROMPT>

Same as `update_info` but with UTF-8 encoding.

### attach_files <files> [to_page <page number | PROMPT>]

Attach files to PDF at document level or to specific page.

**Examples:**
```bash
# Attach to document
pdftk report.pdf attach_files data.xlsx notes.txt output report_with_files.pdf

# Attach to specific page
pdftk slides.pdf attach_files chart.csv to_page 12 output slides_with_data.pdf
```

### unpack_files

Extract all attachments from PDF to current directory or specified output directory.

**Examples:**
```bash
# Extract to current directory
pdftk document.pdf unpack_files

# Extract to specific directory
pdftk report.pdf unpack_files output ~/attachments/
```

## OUTPUT OPTIONS

### output <filename | - | PROMPT>

Specify output filename. Cannot be same as input filename. Use `-` for stdout.

**Context-specific behavior:**
- **dump_data:** Sets output data filename
- **unpack_files:** Sets output directory
- **burst:** Controls page filename format

### Encryption

**encrypt_40bit | encrypt_128bit**

Set encryption strength. Default is 128-bit when password is specified.

**Example:**
```bash
pdftk input.pdf output encrypted.pdf user_pw userpass owner_pw ownerpass encrypt_128bit
```

### allow <permissions>

Set PDF permissions (requires encryption or password). Multiple permissions can be specified.

**Available Permissions:**
- `Printing` - Top quality printing
- `DegradedPrinting` - Lower quality printing
- `ModifyContents` - Also allows Assembly
- `Assembly` - Assemble document
- `CopyContents` - Also allows ScreenReaders
- `ScreenReaders` - Screen reader access
- `ModifyAnnotations` - Also allows FillIn
- `FillIn` - Fill in form fields
- `AllFeatures` - All of the above

**Example:**
```bash
pdftk in.pdf output secured.pdf owner_pw secret allow Printing CopyContents
```

### owner_pw <password | PROMPT>

Set owner (master) password for output PDF.

### user_pw <password | PROMPT>

Set user (open) password for output PDF.

**Example:**
```bash
pdftk input.pdf output protected.pdf user_pw openpass owner_pw masterpass
```

**Note:** If encryption is specified but no passwords are given, the PDF can be opened and altered by anyone.

### flatten

Merge form fields and their data with PDF pages. Only works with single input PDF. Often used with `fill_form`.

**Example:**
```bash
pdftk form.pdf fill_form data.fdf output filled.pdf flatten
```

### need_appearances

Set flag for Reader/Acrobat to generate field appearances from values. Use for non-ASCII text in forms. Cannot combine with `flatten`.

### compress | uncompress

**uncompress** - Remove page stream compression for text editing
**compress** - Restore page stream compression

**Example:**
```bash
# Uncompress for editing
pdftk input.pdf output uncompressed.pdf uncompress

# Recompress after editing
pdftk uncompressed.pdf output final.pdf compress
```

### keep_first_id | keep_final_id

Copy document ID from first or final input PDF to output. Otherwise creates new ID.

### drop_xfa

Remove XFA data from Acrobat 7/Adobe Designer forms. Needed when filled forms fail to display in Acrobat 7.

**Note:** XFA data is automatically omitted when assembling multiple PDFs.

### verbose

Enable verbose output. By default, pdftk runs quietly.

### dont_ask | do_ask

Override default prompting behavior for problems like bad passwords.

**Note:** In `dont_ask` mode, pdftk will overwrite output files without notice.

## GLOBAL OPTIONS

### --help, -h

Show help summary.

## EXAMPLES

### Basic Operations

```bash
# Merge PDFs
pdftk file1.pdf file2.pdf file3.pdf cat output merged.pdf

# Extract pages 1-5 and 10-15
pdftk input.pdf cat 1-5 10-15 output extracted.pdf

# Reverse page order
pdftk input.pdf cat end-1 output reversed.pdf

# Remove page 13
pdftk input.pdf cat 1-12 14-end output fixed.pdf

# Split PDF in half
pdftk input.pdf cat 1-20 output first_half.pdf
pdftk input.pdf cat 21-end output second_half.pdf
```

### Rotation

```bash
# Rotate all pages 90° clockwise
pdftk landscape.pdf cat 1-endeast output portrait.pdf

# Rotate just the first page
pdftk input.pdf cat 1east 2-end output rotated.pdf

# Flip even and odd pages differently
pdftk input.pdf cat 1-endoddeast 1-endevenwest output mixed.pdf
```

### Forms

```bash
# Fill form
pdftk form.pdf fill_form data.fdf output filled.pdf

# Fill and flatten
pdftk form.pdf fill_form data.fdf output filled.pdf flatten

# Generate FDF from filled form
pdftk filled_form.pdf generate_fdf output data.fdf
```

### Watermarks & Stamps

```bash
# Background watermark
pdftk document.pdf background watermark.pdf output watermarked.pdf

# Overlay stamp
pdftk document.pdf stamp approved.pdf output stamped.pdf

# Multi-page backgrounds
pdftk slides.pdf multibackground headers.pdf output branded.pdf
```

### Encryption & Security

```bash
# Encrypt with passwords
pdftk input.pdf output secure.pdf user_pw userpass owner_pw ownerpass

# Encrypt with permissions
pdftk input.pdf output restricted.pdf owner_pw secret allow Printing

# Remove encryption (requires owner password)
pdftk secure.pdf input_pw ownerpass output unlocked.pdf
```

### Metadata

```bash
# Extract metadata
pdftk input.pdf dump_data output info.txt

# Update metadata
pdftk input.pdf update_info info.txt output updated.pdf

# Extract form fields
pdftk form.pdf dump_data_fields output fields.txt
```

### Attachments

```bash
# Attach files
pdftk report.pdf attach_files data.csv chart.png output with_files.pdf

# Extract attachments
pdftk document.pdf unpack_files output ~/extracted/
```

### Advanced

```bash
# Collate odd and even scanned pages
pdftk A=odd.pdf B=even.pdf shuffle A B output collated.pdf

# Burst into individual pages
pdftk document.pdf burst output page_%03d.pdf

# Combine operations
pdftk A=form.pdf fill_form data.fdf output filled.pdf \
      stamp approved.pdf flatten compress owner_pw secret
```

## SEE ALSO

**pdf2ps**(1), **ps2pdf**(1), **gs**(1)

## NOTES

- Page numbers are 1-based (first page is 1, not 0)
- Use handles to reference multiple input files
- Operations are case-sensitive
- Most operations require owner password for encrypted PDFs
- Filter mode (no operation) processes a single PDF with output options

## AUTHOR

Sid Steward (https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/)
