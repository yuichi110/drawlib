# Drawlib Linear Document, PDF & MS Word Project Guidelines (`project-doc`)

A **`doc` project** (`drawlib init doc`) compiles a sequential series of Markdown chapter files (`doc_src/*.md`) containing embedded ````drawlib```` blocks into a **single unified HTML document (`doc_html/index.html`)**, a **print-ready A4 vector PDF (`doc.pdf`)**, **GitHub-Flavored Markdown (`doc_markdown/`)**, and **extracted diagram images (`doc_images/`)**, with optional on-demand export to a **native editable Microsoft Word document (`doc.docx`)** via `drawlib build docx`.

*(For general project scaffolding, see `uv run drawlib rules show project-overview`. For multi-page websites with a sidebar, see `uv run drawlib rules show project-site`. For the 3-stage review loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. When to Choose a `doc` Project

Choose `drawlib init doc` when the user wants a **linear, end-to-end technical document, printable PDF report, or editable MS Word (`.docx`) deliverable**:
- Architecture whitepapers, technical reports, and case studies (e.g., `drawlib-dogfooding`).
- Engineering RFCs, design specifications, and security threat models (including `.docx` exports for stakeholder redlining).
- Step-by-step quickstart manuals (`quickstart`) intended to be read linearly or exported as a single PDF or Word book.

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

### 2.1. Zero-Config PDF Compilation & On-Demand MS Word (`.docx`) Export
- **Standard Out-of-the-Box Dependencies**: `playwright` and `python-docx` are standard dependencies of `drawlib` (no optional extras required). Headless Chromium (`chromium-headless-shell`) downloads automatically on your first `drawlib build pdf` run (or pre-download offline via `uv run drawlib cache download --browser` / `--all`; in minimal Linux containers such as `python:3.12-slim` lacking OS shared libraries, run `playwright install-deps chromium`).
- **On-Demand MS Word Export (`drawlib build docx` / `drawlib.tools.build_docx`)**:
  While scaffolded `build.sh` continues to build HTML, PDF, Markdown, and Images, you can compile `doc_src/` (or any single `.md` file) into a native editable `.docx` document with headings, prose, lists, tables, blockquotes, syntax-highlighted code blocks, and high-DPI static PNG diagrams (`dpi=200` default):
  ```bash
  # CLI export (directory or single .md):
  uv run drawlib build docx doc_src/ -o doc.docx --page-break --generate-index \
      --dpi 200 -s doc_src/styles.py -u doc_src/utils.py
  ```
  ```python
  # Python API (drawlib.tools.build_docx):
  from drawlib.tools import build_docx

  build_docx(
      input_path="doc_src/",
      output_file="doc.docx",
      title=None,
      page_break=True,
      generate_index=True,
      dpi=200,
      styles_path="doc_src/styles.py",
      utils_path="doc_src/utils.py",
      no_cache=False,
      timestamp=False,
  )
  ```

```drawlib align=center code=fold file=project_doc_pipeline.png caption="Linear Document (doc_src/) Chapter Merging, ToC Injection & PDF / Word Compilation"
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
    "Linear Document Pipeline (doc_src/*.md -> doc.pdf / doc.docx)",
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
    "• Sorted path merge\n• --generate-index ToC\n• --page-break chapters\n• 720pt font scaling",
    style=Styles.Dark.patch(text_size=10.0),
)

line((95.5, 25), (104.5, 25), arrow_head="->", style=Styles.DarkBold)

# Stage 3: Multi-Target Outputs
rectangle((124, 25), width=38, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.file_pdf((110, 36.5), width=5.0, style=Styles.WhiteBold)
text((126, 36.5), "3. Deliverables", style=Styles.WhiteBold.patch(text_size=11.5))
text(
    (124, 21),
    "• doc.pdf (Vector A4)\n• doc.docx (MS Word)\n• doc_html/index.html\n• doc_markdown/*.md",
    style=Styles.White.patch(text_size=10.0),
)

save()
```

---

## 3. Authoring Best Practices for Linear Documents & Whitepapers

### 3.1. Deterministic Chapter Numbering (`00_cover.md`, `01_...`, `02_...`)
When `drawlib build html`, `drawlib build pdf`, or `drawlib build docx` compiles `doc_src/`, it discovers all `.md` files (excluding `README.md`) and merges them in **sorted lexicographical order**:
1. **`00_cover.md` (Cover Page)**:
   - Place the overall document `# Title`, subtitle, executive abstract, a rich cover Hero diagram (`code=hide`), and author/date metadata in `00_cover.md`.
   - When `--generate-index` is passed to `drawlib build pdf` or `drawlib build docx` (or `build_pdf.sh`), Drawlib automatically injects the generated **Table of Contents** immediately after the first chapter (`00_cover.md`) and before `01_*.md`.
2. **Numbered Chapters (`01_overview.md`, `02_architecture.md`, ...)**:
   - Start each chapter file with a top-level `# 1. Chapter Title` heading.
   - When `--page-break` (default `True`) is enabled, Drawlib inserts a page break before each chapter file so every chapter starts cleanly at the top of a new page in both A4 PDF and MS Word (`.docx`).

### 3.2. Code Visibility Strategy (`code=hide` vs. `code=fold` vs. `code=show`)
Choose the ```` ```drawlib ```` visibility attribute based on the document's purpose and target medium:
- **Whitepapers, RFCs & Architecture Specs (`code=hide` Recommended)**:
  In narrative whitepapers (`drawlib-dogfooding`) or design specifications where readers care about the architecture rather than the Python drawing code, use `code=hide` (the default) so both the web preview and printed PDF read like a polished book.
- **Tutorials & Quickstart Guides (`code=fold` + `code=show`)**:
  In developer guides (`quickstart`), use **`code=fold`** on the chapter's opening Hero diagram (so the illustration appears immediately above the fold) and `code=show` on instructional code examples where the reader is learning Drawlib syntax.

### 3.3. Page Composition, Visual Density & A4 Print Discipline
1. **Chapter Hero Diagram at `Lines 5–15`**:
   Begin every chapter (`01_*.md`, `02_*.md`, ...) with `# Chapter Title`, a 1–2 sentence lead paragraph, and an immediate **Chapter Hero diagram at Lines 5–15** combining `phosphor`/`gcp` icons with high-level components (`SmartArts`, `Diagrams`, `Graphs`, `Charts`).
2. **`2+` Diagrams per Chapter**:
   Break up long prose sections with at least `2` diagrams per chapter (`file=<name>.png` and `caption="..."` mandatory on every block).
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
   Verify that every chapter has `>= 2` diagrams, a Chapter Hero at `Lines 5–15`, explicit `file=<name>.png` and `caption="..."`, zero narrow `px` width caps, `text_size >= 10.0`, zero `file://` or absolute path links, and accurate `Center` (`shapes`/`text`/`icons`/`images`/`MindMapNode`/`Cycle`), `Bottom-Left` (`ChevronProcess`/`GridLayout`/`Pyramid`/`BoxList`/`CardList`/`KpiCards`/`Roadmap`/`Panel`/`GeoMap`/`MonthCalendar`/`Charts`/`Diagrams`), and `Top-Left` (`Table`/`TreeNode`/`BulletPoints`/`SourceCode`) coordinate anchors.
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
   - The cover page (`00_cover.md`) and Table of Contents (`--generate-index`) render cleanly without overflowing onto extra blank pages.
   - Diagram labels are crisp and proportional to the surrounding body prose.
   - Clean up `.drawlib/scratch/` when done.
4. **Parallel Multi-Agent Chapter Delegation (For Multi-Chapter Documents)**:
   Because each chapter in `doc_src/` is a standalone numbered file (`01_overview.md`, `02_architecture.md`, `03_security.md`, etc.), **distribute chapter authoring across parallel subagents** whenever creating or updating multiple chapters:
   - **Phase 1 (Parent)**: Scaffold `doc_src/`, configure `styles.py`, `utils.py`, and `00_cover.md`, and define the numbered chapter filenames.
   - **Phase 2 (Parallel Subagents)**: Assign each subagent its own `doc_src/0N_<chapter>.md` file(s). Each subagent writes the chapter (`2+` diagrams, Chapter Hero at `Lines 5–15`) and executes Stage 1 & Stage 2 using a **unique scratch filename** (`-o .drawlib/scratch/0N_<diagram>_grid.png`).
   - **Phase 3 (Parent)**: Run `./doc_src/build.sh` once after all subagents finish, verify links (`drawlib serve doc_html/ --check`), and perform Stage 3 inspection of `doc.pdf` and `doc_html/index.html`.

