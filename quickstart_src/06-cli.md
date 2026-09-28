# 6. Unified CLI & Document Builder

Drawlib includes a built-in **Document Builder** and **CLI** (`drawlib`) that compiles standalone Python scripts or Markdown documentation containing embedded `drawlib` code blocks into multiple publication targets.

## Core CLI Subcommands

| Command | Description |
| :--- | :--- |
| `drawlib build image <src>` | Execute `.py` files or directories to batch-generate illustration images. |
| `drawlib build markdown <src> -o <out>` | Compile Markdown with `drawlib` blocks into standard GitHub-ready Markdown + images. |
| `drawlib build html <src> -o <out>` | Compile Markdown/HTML into a responsive static HTML website (`--css google`). |
| `drawlib build pdf <src> -o <out.pdf>` | Merge Markdown/HTML files in filename order into a single PDF (`--generate-index`). |
| `drawlib show <file> [block]` | Preview an illustration or Markdown block interactively or headlessly. |
| `drawlib export <file> [block] -o <img.png>` | Export a specific `drawlib` block from Markdown to an image file. |
| `drawlib serve <html_dir>` | Start a local HTTP server with link and asset verification. |

## Example Build Commands

```bash
# Build GitHub Markdown and HTML website
uv run drawlib build markdown docs_src/ -o docs/
uv run drawlib build html docs_src/ -o docs_html/

# Build merged Quickstart PDF with auto-generated index between 1st and 2nd files
uv run drawlib build pdf quickstart_src/ -o quickstart.pdf --generate-index
```

```drawlib 600px center caption:"Figure 6.1: Single-Source Documentation Compilation Pipeline"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import styles
from drawlib.text import text

setup(width=110, height=46)

# Source
rectangle(
    xy=(20, 23),
    width=28,
    height=24,
    r=2,
    style=styles.primary_outline,
)
text(xy=(20, 26), text="Markdown + drawlib", style=styles.primary_bold, size=10)
text(xy=(20, 19), text="(docs_src/)", style=styles.primary, size=9)

# Compiler
rectangle(
    xy=(56, 23),
    width=24,
    height=20,
    r=2,
    style=styles.secondary_outline,
)
text(xy=(56, 23), text="drawlib build", style=styles.secondary_bold, size=10)

line((34, 23), (44, 23), arrowhead="->", style=styles.primary_bold)

# Outputs
outputs = [
    (36, "docs/ (Markdown)", styles.accent),
    (23, "docs_html/ (Web)", styles.success),
    (10, "quickstart.pdf (PDF)", styles.primary),
]
for y_pos, label, st in outputs:
    line((68, 23), (78, y_pos), arrowhead="->", style=styles.secondary_bold)
    rectangle(
        xy=(93, y_pos),
        width=28,
        height=9,
        r=1.5,
        style=st,
        text=label,
        textstyle=styles.white_bold,
    )
```
