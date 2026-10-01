# Chapter 5: Project Scaffolding and Build Workflows

Drawlib provides the `drawlib init` command to scaffold purpose-built documentation projects in seconds.

## 5.1 Project Template Types

| Template | Use Case | Primary Artifacts |
| :--- | :--- | :--- |
| **`pdf`** | Multi-chapter technical specs, engineering RFCs, and formal reports | `<name>.pdf` (with auto-generated TOC) |
| **`site`** | Multi-page documentation website with sidebar navigation | `<name>_html/` and `<name>/` |
| **`simple`** | Single-page specifications, RFCs, and READMEs | `<name>_html/doc.html` |
| **`image`** | Standalone Python drawing scripts | `<name>/*.png` |

## 5.2 Creating a Google-Style PDF Project

Create a Google-style PDF project in one command:

```bash
uv run drawlib init pdf my_report/ -o report -l en -s google
```

```drawlib 640px center file:fig_project_lifecycle.png caption:"Figure 5.1: Project Lifecycle from Scaffolding to Final Artifact"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=135, height=54)

header_ts = Styles.WhiteBold.patch(text_size=9.2)
ts_sec_body = Styles.Secondary.patch(text_size=7.8, text_halign="left")
ts_body = Styles.Primary.patch(text_size=7.8, text_halign="left")
ts_acc_body = Styles.Accent.patch(text_size=7.8, text_halign="left")

# 1. Scaffold: drawlib init
rectangle((23.5, 24.0), width=35.0, height=38.0, r=2.0, style=Styles.MutedDashed)
rectangle((23.5, 40.0), width=33.0, height=5.5, r=1.5, style=Styles.SecondaryFlat, text="1. drawlib init", textstyle=header_ts)

phosphor.terminal_window(xy=(11.0, 31.0), width=5.0, style=Styles.Secondary)
text((16.0, 31.0), text="-o report\nSynchronized name & path", style=ts_sec_body)

phosphor.palette(xy=(11.0, 21.5), width=5.0, style=Styles.Secondary)
text((16.0, 21.5), text="-s google\nUnified CSS & Python theme", style=ts_sec_body)

phosphor.translate(xy=(11.0, 12.0), width=5.0, style=Styles.Secondary)
text((16.0, 12.0), text="-l en\nEnglish typography stack", style=ts_sec_body)

# Arrow 1
line((42.0, 24.0), (49.0, 24.0), arrowhead="->", style=Styles.PrimaryBold)
text((45.5, 27.5), text="Scaffold", style=Styles.SecondaryBold, size=8.5)

# 2. Source Directory: report_src/ (Source of Truth)
rectangle((67.5, 24.0), width=35.0, height=38.0, r=2.0, style=Styles.PrimaryOutline)
rectangle((67.5, 40.0), width=33.0, height=5.5, r=1.5, style=Styles.PrimaryFlat, text="2. report_src/ (Source)", textstyle=header_ts)

phosphor.file_text(xy=(55.0, 31.0), width=5.0, style=Styles.Primary)
text((60.0, 31.0), text="00_cover.md, 01_*.md\nMarkdown + embedded code", style=ts_body)

phosphor.file_code(xy=(55.0, 21.5), width=5.0, style=Styles.Primary)
text((60.0, 21.5), text="styles.py / style.css\nDesign token definitions", style=ts_body)

phosphor.play_circle(xy=(55.0, 12.0), width=5.0, style=Styles.Primary)
text((60.0, 12.0), text="build.sh\nAutomated build script", style=ts_body)

# Arrow 2
line((86.0, 24.0), (93.0, 24.0), arrowhead="->", style=Styles.PrimaryBold)
text((89.5, 27.5), text="build.sh", style=Styles.PrimaryBold, size=8.5)

# 3. Deliverable: report.pdf
rectangle((111.5, 24.0), width=35.0, height=38.0, r=2.0, style=Styles.AccentOutline)
rectangle((111.5, 40.0), width=33.0, height=5.5, r=1.5, style=Styles.AccentFlat, text="3. report.pdf (Output)", textstyle=header_ts)

phosphor.file_pdf(xy=(99.0, 31.0), width=5.0, style=Styles.Accent)
text((104.0, 31.0), text="A4 Print Optimization\nChromium rendering engine", style=ts_acc_body)

phosphor.list_numbers(xy=(99.0, 21.5), width=5.0, style=Styles.Accent)
text((104.0, 21.5), text="Automatic TOC\nPage numbers in sync", style=ts_acc_body)

phosphor.image(xy=(99.0, 12.0), width=5.0, style=Styles.Accent)
text((104.0, 12.0), text="Vector Graphics\nHigh-res inline diagrams", style=ts_acc_body)
```

### Synchronized Naming via `-o`

Specifying `-o report` establishes a synchronized pipeline:
- **Source Directory**: Creates `my_report/report_src/`.
- **Build Output**: Generates `my_report/report.pdf`.

## 5.3 Directory Structure

The scaffolded `report_src/` folder contains:

```text
my_report/
├── report_src/
│   ├── 00_cover.md           # [Required] Title page and metadata
│   ├── 01_overview.md        # Chapter 1 content
│   ├── 02_design.md          # Chapter 2 content
│   ├── style.css             # PDF stylesheet (Google Theme)
│   ├── styles.py             # Drawing style definitions (GoogleStyles)
│   ├── template.html         # Jinja2 print layout template
│   ├── utils.py              # Project drawing helpers
│   ├── build.sh              # [Executable] One-click build script
│   └── README.md             # Project guide
```

## 5.4 Building the Document

To compile your Markdown documents into a polished PDF, run the generated `build.sh`:

```bash
# Execute build script
./my_report/report_src/build.sh
```

When compilation finishes, `my_report/report.pdf` is ready for distribution.
