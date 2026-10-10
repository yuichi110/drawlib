# Drawlib Linear Document & PDF Project Guidelines (`project-doc`)

A **`doc` project** (`drawlib init doc`) compiles a sequential series of Markdown chapter files (`doc_src/*.md`) containing embedded ````drawlib```` blocks into a **single unified HTML document (`doc_html/index.html`)**, a **print-ready A4 vector PDF (`doc.pdf`)**, **GitHub-Flavored Markdown (`doc_markdown/`)**, and **extracted diagram images (`doc_images/`)**.

*(For general project scaffolding, see `uv run drawlib rules show project-overview`. For multi-page websites with a sidebar, see `uv run drawlib rules show project-site`. For the 3-stage review loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. When to Choose a `doc` Project

Choose `drawlib init doc` when the user wants a **linear, end-to-end technical document or printable PDF report**:
- Architecture whitepapers, technical reports, and case studies (e.g., `drawlib-dogfooding`).
- Engineering RFCs, design specifications, and security threat models.
- Step-by-step quickstart manuals (`quickstart`) intended to be read linearly or exported as a single PDF book.

```bash
# Scaffold a linear document project (default target 'doc', or custom name e.g. 'spec'):
uv run drawlib init doc [target] [-l <lang>] [-s <default|google|monochrome>]

# Examples:
uv run drawlib init doc --lang ja -s google
uv run drawlib init doc rbac_spec -s default
```

---

## 2. Directory Structure & Multi-Target Compilation (`doc_src/`)

```text
.
├── doc_src/                   # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── 00_cover.md            # Cover chapter (H1 Document Title, subtitle, hero figure, metadata)
│   ├── 01_overview.md         # Chapter 1: Executive Overview
│   ├── 02_architecture.md     # Chapter 2: System Architecture
│   ├── 03_implementation.md   # Chapter 3: Implementation & Benchmarks
│   ├── _assets/               # Static images, logos, or custom .ttf fonts
│   ├── styles.py              # Document-wide Drawlib Styles & Colors
│   ├── utils.py               # Reusable Python drawing helpers & macros
│   ├── style.css              # Screen + @media print / @page A4 CSS stylesheet
│   ├── template.html          # Jinja2 linear document HTML template
│   ├── build.sh               # Master build script (HTML + PDF + Markdown + Images)
│   ├── build_html.sh          # Compiles merged HTML preview (doc_html/index.html)
│   ├── build_pdf.sh           # Compiles headless Chromium vector PDF (doc.pdf)
│   ├── build_markdown.sh      # Compiles GitHub-ready Markdown chapters (doc_markdown/)
│   ├── build_image.sh         # Extracts standalone diagram PNGs (doc_images/)
│   └── serve.sh               # Local preview server for doc_html/
├── doc_html/                  # [GENERATED] Merged linear HTML document
├── doc.pdf                    # [GENERATED] High-resolution printable vector PDF
├── doc_markdown/              # [GENERATED] Rendered Markdown with image links
└── doc_images/                # [GENERATED] Extracted chapter diagram images
```

> **CRITICAL (`No navbar.md` in `doc` Projects & Excluding Planning Files)**: Never create a `navbar.md` file inside `doc_src/`. Drawlib's HTML builder uses the presence of `navbar.md` to distinguish between a multi-page website (`site`) and a merged single-page linear document (`doc`). Any non-chapter files or subdirectories starting with `_` (e.g., `_outline.md`, `_drafts/`) as well as `README.md` are automatically excluded from document compilation.

```drawlib center fold-code file:project_doc_pipeline.png caption:"Linear Document (doc_src/) Chapter Merging, ToC Injection & PDF Compilation"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=58, dpi=150)

rectangle((75, 29), width=144, height=52, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (75, 50.5),
    "Linear Document & Vector PDF Pipeline (doc_src/*.md -> doc.pdf)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# Stage 1: Ordered Chapters
rectangle((26, 25), width=38, height=34, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.files((12, 36.5), width=5.0, style=Styles.PrimaryBold)
text((28, 36.5), "1. Chapter Files", style=Styles.PrimaryBold.patch(text_size=11.5))
text(
    (26, 21),
    "• 00_cover.md (Cover)\n• 01_overview.md\n• 02_design.md\n• 2+ diagrams / chapter",
    style=Styles.Dark.patch(text_size=10.0),
)

line((45.5, 25), (54.5, 25), arrow_head="->", style=Styles.DarkBold)

# Stage 2: Merge + Auto ToC + Page Breaks
rectangle((75, 25), width=40, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.list_numbers((60.5, 36.5), width=5.0, style=Styles.SecondaryBold)
text((77, 36.5), "2. Merge & ToC", style=Styles.SecondaryBold.patch(text_size=11.5))
text(
    (75, 21),
    "• Sorted path merge\n• --toc after 00_cover\n• --page-break chapters\n• 720pt font scaling",
    style=Styles.Dark.patch(text_size=10.0),
)

line((95.5, 25), (104.5, 25), arrow_head="->", style=Styles.DarkBold)

# Stage 3: Multi-Target Outputs
rectangle((124, 25), width=38, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.file_pdf((110, 36.5), width=5.0, style=Styles.WhiteBold)
text((126, 36.5), "3. Deliverables", style=Styles.WhiteBold.patch(text_size=11.5))
text(
    (124, 21),
    "• doc.pdf (Vector A4)\n• doc_html/index.html\n• doc_markdown/*.md\n• doc_images/*.png",
    style=Styles.White.patch(text_size=10.0),
)

save()
```

---

## 3. Authoring Best Practices for Linear Documents & Whitepapers

### 3.1. Deterministic Chapter Numbering (`00_cover.md`, `01_...`, `02_...`)
When `drawlib build html` or `drawlib build pdf` compiles `doc_src/`, it discovers all `.md` files (excluding `README.md`) and merges them in **sorted lexicographical order**:
1. **`00_cover.md` (Cover Page)**:
   - Place the overall document `# Title`, subtitle, executive abstract, a rich cover Hero diagram (`hide-code`), and author/date metadata in `00_cover.md`.
   - When `--toc` (`--generate-index`) is passed to `drawlib build pdf` (or `build_pdf.sh`), Drawlib automatically injects the generated **Table of Contents** immediately after the first chapter (`00_cover.md`) and before `01_*.md`.
2. **Numbered Chapters (`01_overview.md`, `02_architecture.md`, ...)**:
   - Start each chapter file with a top-level `# 1. Chapter Title` heading.
   - When `--page-break` (default `True`) is enabled, Drawlib inserts a CSS page break (`page-break-before: always`) before each chapter file so every chapter starts cleanly at the top of a new A4 PDF page.

### 3.2. Code Visibility Strategy (`hide-code` vs. `fold-code` vs. `show-code`)
Choose the ```` ```drawlib ```` visibility attribute based on the document's purpose and target medium:
- **Whitepapers, RFCs & Architecture Specs (`hide-code` Recommended)**:
  In narrative whitepapers (`drawlib-dogfooding`) or design specifications where readers care about the architecture rather than the Python drawing code, use `hide-code` (the default) so both the web preview and printed PDF read like a polished book.
- **Tutorials & Quickstart Guides (`fold-code` + `show-code`)**:
  In developer guides (`quickstart`), use **`fold-code`** on the chapter's opening Hero diagram (so the illustration appears immediately above the fold) and `show-code` on instructional code examples where the reader is learning Drawlib syntax.

### 3.3. Page Composition, Visual Density & A4 Print Discipline
1. **Chapter Hero Diagram at `Lines 5–15`**:
   Begin every chapter (`01_*.md`, `02_*.md`, ...) with `# Chapter Title`, a 1–2 sentence lead paragraph, and an immediate **Chapter Hero diagram at Lines 5–15** combining `phosphor`/`gcp` icons with high-level components (`SmartArts`, `Diagrams`, `Graphs`, `Charts`).
2. **`2+` Diagrams per Chapter**:
   Break up long prose sections with at least `2` diagrams per chapter (`file:<name>.png` and `caption:"..."` mandatory on every block).
3. **Full Column Width & `720pt` Typography Scaling**:
   - **Never pass narrow pixel widths** (`500px`, `600px`) on code fences. Omit pixel width tokens so figures fill `100%` of the document column in both HTML and A4 PDF.
   - Keep **`text_size >= 10.0`** (standard `10.5`–`12.0`, titles `12.0`–`14.0`, floor `9.5`) so rendered text ($\text{text\_size} \times \text{Width} / 720$) matches the document body font.
4. **Landscape Aspect Ratios for Clean PDF Page Breaks**:
   - Avoid tall portrait canvases (`height > width`), which often get pushed to the next A4 page and leave large blank gaps at the bottom of the preceding page.
   - Favor compact widescreen or landscape canvases (`setup(width=140, height=60)`, `150×65`, or `120×55`) that fit comfortably alongside headings and prose on an A4 page.
5. **Strictly Relative Links & Asset References (No Absolute Paths or `file://` URLs)**:
   - All cross-chapter references (`[Chapter 2](02_details.md)`) and image assets (`![Fig](_assets/arch.png)`) must use relative paths.
   - Never write local filesystem absolute paths (`/usr/...`, `/home/...`, `/Users/...`, `C:\...`) or `file:///` URLs. Prohibited paths are rejected at build time.

---

## 4. Autonomous 3-Stage Verification Workflow for `doc` Projects

Always verify linear documents across all three stages before finishing:

1. **Stage 1 — Static & Anchor Check**:
   Verify that every chapter has `>= 2` diagrams, a Chapter Hero at `Lines 5–15`, explicit `file:<name>.png` and `caption:"..."`, zero narrow `px` width caps, `text_size >= 10.0`, zero `file://` or absolute path links, and accurate `Center` (`shapes`/`text`/`icons`) vs. `Bottom-Left` (`SmartArts`/`Charts`/`Diagrams`/`Graphs`) coordinate anchors.
2. **Stage 2 — Micro-Geometry Grid Review (`drawlib show ... -g` + `view_file`)**:
   Test each new or modified diagram quickly with the coordinate grid without rebuilding the entire PDF:
   ```bash
   uv run drawlib show doc_src/02_architecture.md system_arch.png \
       -s doc_src/styles.py -u doc_src/utils.py \
       -g -o .drawlib/scratch/preview.png
   ```
   Inspect `.drawlib/scratch/preview.png` via `view_file` to fix any label collisions, cramped margins (`< 4–6` units), or color imbalance (`50%+` neutral cards).
3. **Stage 3 — Full Build, Link Check & HTML/PDF Inspection**:
   ```bash
   ./doc_src/build.sh
   uv run drawlib serve doc_html/ --check
   ```
   Inspect `doc.pdf` (or a `1280×920` headless Chromium screenshot of `doc_html/index.html`) via `view_file` to confirm that:
   - The cover page (`00_cover.md`) and Table of Contents (`--toc`) render cleanly without overflowing onto extra blank pages.
   - Diagram labels are crisp and proportional to the surrounding body prose.
   - Clean up `.drawlib/scratch/` when done.
