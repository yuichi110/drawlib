# Linear Document Project Guide (`drawlib init doc`)

The `doc` starter template is designed for authoring linear technical documents — such as specifications, Request for Comments (RFCs), system architecture proposals, whitepapers, thesis papers, and formal engineering reports.

By unifying single-page specs and multi-chapter reports into a single archetype, Drawlib allows you to compile **HTML, PDF, Markdown, and standalone images** from the same Markdown source files.

---

## 1. Project Initialization

Scaffold a linear document project using `drawlib init`:

```bash
# Create in a new subdirectory:
drawlib init doc my_doc/

# With custom theme, language, and output base name:
drawlib init doc my_report/ -o rbac -s google -l en

# Or scaffold directly in current working directory:
drawlib init doc --here
```

---

## 2. Directory Layout & Anatomy

```text
my_doc/
├── doc_src/                   # [SOURCE OF TRUTH] Author Markdown content here
│   ├── 00_cover.md            # Cover page (title, author, metadata)
│   ├── 01_overview.md         # Executive overview chapter
│   ├── 02_design.md           # Technical design chapter
│   ├── template.html          # Clean Jinja2 layout template
│   ├── style.css              # Document stylesheet (3-layer CSS)
│   ├── styles.py              # Shared project styling themes
│   ├── utils.py               # Helper drawing functions
│   ├── build.sh               # Master build script (runs all target builds)
│   ├── build_html.sh          # Fast preview HTML build (doc_html/)
│   ├── build_pdf.sh           # Headless Chromium vector PDF build (doc.pdf)
│   ├── build_markdown.sh      # Rendered Markdown for GitHub browsing (doc_markdown/)
│   ├── build_image.sh         # Extract embedded drawlib blocks to doc_images/
│   ├── serve.sh               # Local preview server script
│   └── README.md              # Project instructions
├── doc_html/                  # [GENERATED] Single-page HTML document(s)
├── doc.pdf                    # [GENERATED] High-quality vector PDF
├── doc_markdown/              # [GENERATED] Markdown with rendered images for GitHub
└── doc_images/                # [GENERATED] Extracted standalone diagram images
```

---

## 3. Four Target Outputs from One Source

A `doc` project compiles into 4 distinct target artifacts:

| Output Target | Target Audience | Primary Use Case | Build Script |
| :--- | :--- | :--- | :--- |
| **`doc_html/`** | Web Browsers | Fast local preview, web publishing, internal documentation wikis | `build_html.sh` |
| **`doc.pdf`** | Print & Distribution | Formal whitepapers, client deliverables, printable reports with Table of Contents | `build_pdf.sh` |
| **`doc_markdown/`** | GitHub & Version Control | Direct viewing in GitHub/GitLab repositories with rendered image links | `build_markdown.sh` |
| **`doc_images/`** | Presentations & Messaging | Drag-and-drop into Google Slides, Keynote, PowerPoint, Slack, or PRs | `build_image.sh` |

---

## 4. Modular Build Scripts Architecture

Each project contains specialized scripts alongside a master orchestrator:

1. **`build_html.sh`**:
   Compiles Markdown chapters into a beautifully styled HTML document (`doc_html/`). Extremely fast for local verification.
2. **`build_pdf.sh`**:
   Renders the document into an A4 vector PDF via headless Chromium (`page.pdf()`). Supports automatic Table of Contents (`--toc`) and clean chapter page breaks (`--page-break`).
3. **`build_markdown.sh`**:
   Converts inline ````drawlib```` blocks into standard Markdown image tags pointing to rendered diagrams in `doc_markdown/<chapter>_images/`.
4. **`build_image.sh`**:
   Scans all Markdown files, extracts embedded ````drawlib```` blocks, and renders them cleanly into `doc_images/<chapter>_images/` without risk of name collisions.
5. **`build.sh` (Master Script)**:
   Runs all of the above target builds in sequence to produce a complete set of release artifacts.

---

## 5. Direct CLI Commands

You can also run the build commands directly from the terminal:

```bash
# 1. Compile to HTML:
drawlib build html doc_src/ -o doc_html/

# 2. Compile to PDF with Cover and Table of Contents:
drawlib build pdf doc_src/ -o doc.pdf --toc --page-break

# 3. Compile to GitHub-ready Markdown:
drawlib build markdown doc_src/ -o doc_markdown/

# 4. Extract diagram images from Markdown:
drawlib build image doc_src/ -o doc_images/
```
