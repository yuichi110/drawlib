# Chapter 5: Project Scaffolding and Build Workflows

Drawlib provides the `drawlib init` command to scaffold purpose-built documentation projects in seconds.

## 5.1 Project Template Types

| Template | Use Case | Primary Artifacts |
| :--- | :--- | :--- |
| **`doc`** | Multi-chapter technical specs, engineering RFCs, and formal reports | `<target>.pdf`, `<target>_html/`, `<target>_markdown/`, `<target>_images/` |
| **`site`** | Multi-page documentation website with sidebar navigation | `<target>_html/`, `<target>_markdown/`, `<target>_images/` |
| **`slide`** | 16:9 presentation slide deck (web & vector PDF) | `<target>_html/index.html`, `<target>.pdf`, `<target>_images/` |
| **`images`** | Standalone Python drawing scripts | `<target>_images/*.png` (or `<target>/*.png`, `*.webp`) |

## 5.2 Creating a Google-Style Document Project

Create a Google-style document project in one command:

```bash
uv run drawlib init doc report -l en -s google
```

```drawlib align=center file=fig_project_lifecycle.png caption="Figure 5.1: Project Lifecycle from Scaffolding to Final Artifact"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=52)

header_ts = Styles.WhiteBold.patch(text_size=11.0)
ts_body = Styles.Dark.patch(text_size=10.0, halign="left")
ts_arrow = Styles.DarkBold.patch(text_size=10.0)

# 1. Scaffold: drawlib init
rectangle((22.5, 26.0), width=37.0, height=42.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
rectangle((22.5, 43.2), width=35.0, height=6.0, style=Styles.SecondaryFlat.patch(shape_r=1.5), text="1. drawlib init", text_style=header_ts)

phosphor.terminal_window(xy=(8.0, 33.5), width=4.4, style=Styles.Secondary)
text((11.2, 33.5), text="init doc report\nProject scaffold", style=ts_body)

phosphor.palette(xy=(8.0, 22.5), width=4.4, style=Styles.Secondary)
text((11.2, 22.5), text="-s google\nCSS & Python theme", style=ts_body)

phosphor.translate(xy=(8.0, 11.5), width=4.4, style=Styles.Secondary)
text((11.2, 11.5), text="-l en\nEnglish font stack", style=ts_body)

# Arrow 1
line((41.5, 26.0), (47.0, 26.0), arrow_head="->", style=Styles.DarkBold)
text((44.25, 30.0), text="Init", style=ts_arrow)

# 2. Source Directory: report_src/ (Source of Truth)
rectangle((66.0, 26.0), width=37.0, height=42.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((66.0, 43.2), width=35.0, height=6.0, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="2. report_src/ (SoT)", text_style=header_ts)

phosphor.file_text(xy=(51.5, 33.5), width=4.4, style=Styles.Primary)
text((54.7, 33.5), text="00_cover.md, *.md\nProse + drawlib code", style=ts_body)

phosphor.file_code(xy=(51.5, 22.5), width=4.4, style=Styles.Primary)
text((54.7, 22.5), text="styles.py / utils.py\nShared tokens & utils", style=ts_body)

phosphor.folder_open(xy=(51.5, 11.5), width=4.4, style=Styles.Primary)
text((54.7, 11.5), text="_assets/ & build.sh\nAssets & unified build", style=ts_body)

# Arrow 2
line((85.0, 26.0), (90.5, 26.0), arrow_head="->", style=Styles.DarkBold)
text((87.75, 30.0), text="Build", style=ts_arrow)

# 3. Deliverable: report.pdf / report_html/
rectangle((109.5, 26.0), width=37.0, height=42.0, style=Styles.Neutral.patch(shape_r=2.0))
rectangle((109.5, 43.2), width=35.0, height=6.0, style=Styles.DarkFlat.patch(shape_r=1.5), text="3. Build Artifacts", text_style=header_ts)

phosphor.file_pdf(xy=(95.0, 33.5), width=4.4, style=Styles.Dark)
text((98.2, 33.5), text="report.pdf\nA4 print & auto TOC", style=ts_body)

phosphor.globe(xy=(95.0, 22.5), width=4.4, style=Styles.Dark)
text((98.2, 22.5), text="report_html/\nWeb view & link check", style=ts_body)

phosphor.image(xy=(95.0, 11.5), width=4.4, style=Styles.Dark)
text((98.2, 11.5), text="report_images/\nMarkdown & diagrams", style=ts_body)

save()
```

### Automatic Path Resolution via Target Argument

Specifying `drawlib init doc report` establishes a synchronized pipeline:
- **Source Directory**: Creates `report_src/` in the current working directory.
- **Build Output**: Configures `report.pdf`, `report_html/`, `report_markdown/`, and `report_images/` as output targets.

## 5.3 Directory Structure and Incremental Build Cache

The scaffolded `report_src/` folder contains:

```text
report_src/
├── _assets/              # Static assets directory (logos, external images)
├── 00_cover.md           # [Required] Title page and metadata
├── 01_overview.md        # Chapter 1 content
├── 02_design.md          # Chapter 2 content
├── style.css             # PDF / HTML stylesheet (Google Theme)
├── styles.py             # Drawing style definitions (GoogleStyles)
├── template.html         # Jinja2 print and web layout template
├── utils.py              # Shared drawing helpers and constants
├── build.sh              # [Executable] Master build script for all targets
├── serve.sh              # Local preview server startup script
└── README.md             # Project guide
```

During compilation, Drawlib automatically maintains a **SHA-256 incremental build cache** in `.drawlib/cache.db` (SQLite) at the workspace root. By hashing each ````drawlib```` code block alongside `styles.py`, `utils.py`, and any referenced files in `_assets/`, unchanged diagrams are served instantly from cache on subsequent builds.

## 5.4 Building and Verifying Link Integrity

To compile your Markdown sources into PDF, HTML, Markdown, and standalone images, run the generated `build.sh` and verify link integrity with `drawlib serve --check`:

```bash
# Execute master build script (HTML, PDF, Markdown, Images)
./report_src/build.sh

# Automatically verify zero broken internal links or missing images
uv run drawlib serve report_html/ --check
```

When compilation finishes, `report.pdf`, `report_html/`, `report_markdown/`, and `report_images/` are ready for distribution, and `drawlib serve --check` confirms that all links and image references are intact.
