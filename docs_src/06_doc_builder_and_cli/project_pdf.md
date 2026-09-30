# PDF Project Guide (`drawlib init pdf`)

The `pdf` starter template compiles multi-chapter technical specifications, formal whitepapers, architectural design documents, and printed engineering reports into high-fidelity vector PDFs via headless Chromium.

---

## 1. Project Initialization

Scaffold a PDF project using `drawlib init`:

```bash
# Create in a new subdirectory:
drawlib init pdf my_whitepaper/

# Or scaffold directly in current working directory:
drawlib init pdf --here
```

---

## 2. Directory Layout & Anatomy

```text
my_whitepaper/
├── docs_src/                  # [SOURCE OF TRUTH] Edit chapters here
│   ├── 00_cover.md            # Document cover page (Title, Author, Date)
│   ├── 01_overview.md         # Executive summary chapter
│   ├── 02_architecture.md     # Technical architecture chapter
│   ├── template.html          # PDF layout template
│   ├── style.css              # PDF/Print stylesheet (@media print)
│   ├── config.py              # Global drawing settings
│   ├── build.sh               # Executable PDF compilation script
│   └── README.md              # Build instructions
└── docs.pdf                   # [GENERATED] Compiled vector PDF document
```

---

## 3. Headless PDF Compilation Engine

Drawlib leverages Playwright and headless Chromium (`page.pdf()`) to render PDFs. This guarantees:
- **Cross-Platform Determinism**: Eliminates OS font discrepancies and layout differences.
- **Accurate Web Font Rendering**: Custom Google Fonts and CJK typefaces render with exact letter spacing.
- **Vector Fidelity**: Embedded Drawlib diagrams retain crisp vector resolution at 300+ DPI.

### Engine Prerequisites:
Ensure the PDF dependencies and browser binaries are installed:

```bash
uv add "drawlib[pdf]"
uv run playwright install chromium
```

---

## 4. Chapter Structuring & Features

### Cover Page (`00_cover.md`)
The cover page typically defines the publication title, version, author, and date metadata:

```markdown
# Cloud Platform Technical Architecture

### Engineering Whitepaper v2.0
**Author**: System Architecture Team  
**Date**: October 2026
```

### Automatic Table of Contents (`--toc`)
Pass `--toc` (or `--generate-index`) to automatically generate a hierarchical Table of Contents derived from your Markdown `#` and `##` headings, complete with chapter page numbers.

### Automatic Page Breaks (`--page-break`)
Pass `--page-break` to automatically insert standard CSS page breaks (`page-break-before: always;`) before each top-level chapter, ensuring each `.md` file begins on a clean new sheet.

---

## 5. Compiling the PDF

### Automated Build (`./build.sh`)
```bash
./docs_src/build.sh
```

### Direct CLI Command
```bash
drawlib build pdf docs_src/ -o docs.pdf --toc --page-break -s docs_src/styles.py
```
