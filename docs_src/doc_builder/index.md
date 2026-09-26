# Document Builder Overview

Drawlib follows an **"Illustration as Code"** and **"Documentation as Code"** philosophy. 
Instead of relying on external documentation engines (such as Sphinx, MkDocs, or Docusaurus) and managing external diagram image assets manually, Drawlib features a built-in documentation compiler: `drawlib.doc_builder`.

---

## 1. Core Principles

- **Single Source of Truth**: Author your documentation exclusively in standard Markdown (`.md`) containing embedded `drawlib` code blocks.
- **Zero External Diagram Generators**: Drawing scripts are executed natively during compilation, outputting vector-grade PNG, WebP, or SVG graphics.
- **Tri-Target Compilation**: A single documentation source compiles into three publication targets:
  1. **Rendered Markdown (`docs/`)**: Optimized for GitHub repository browsing. Code blocks become syntax-highlighted Python snippets followed by relative image links.
  2. **Static HTML Website (`docs_html/`)**: A responsive documentation website featuring auto-generated sidebar navigation, breadcrumbs, search-ready structure, clean typography, and light/dark theme styling.
  3. **Headless Vector PDF (`<name>.pdf`)**: High-fidelity publication-ready PDF documents generated via system Chromium browsers without requiring bulky browser automation frameworks.

---

## 2. Compilation Targets

| Target Format | Output Location | Primary Use Case | Output Characteristics |
| :--- | :--- | :--- | :--- |
| **HTML** | `docs_html/` | Public web hosting (GitHub Pages, Netlify, S3) | Interactive responsive website, sidebar navigation, light/dark themes, collapsible code sections. |
| **Markdown** | `docs/` | GitHub / GitLab repo browsing | Native Markdown with syntax-highlighted Python blocks and local image references. |
| **PDF** | `doc.pdf` / `<name>.pdf` | Offline distribution, print, release manuals | Vector-quality multi-page PDF generated via headless Chromium. |

```drawlib 700px center caption:"Drawlib Single-Source Documentation Architecture"
from drawlib.canvas import save, setup
from drawlib.colors import Colors, Colors140
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style
from drawlib.config import styles

setup(width=140, height=80)

# Colors
blue_primary = Colors140.RoyalBlue
green_primary = Colors140.ForestGreen
purple_primary = Colors140.DarkSlateBlue
orange_primary = Colors140.DarkOrange

# 1. Source (Left)
rectangle(
    (22, 40),
    width=32,
    height=56,
    r=3,
    style=styles.primary.patch(shape_fill_color=Colors140.AliceBlue, shape_line_color=blue_primary, shape_line_width=2),
)
text((22, 61), "Source of Truth", style=styles.primary.patch(text_size=15, text_font=FontRoboto.ROBOTO_BOLD, text_color=blue_primary))
text((22, 53), "docs_src/*.md", style=styles.primary.patch(text_size=13, text_font=FontRoboto.ROBOTO_BOLD))
rectangle(
    (22, 31),
    width=26,
    height=24,
    r=2,
    style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=Colors140.LightSteelBlue, shape_line_width=1.5),
)
text((22, 38), "Markdown Text", style=styles.primary.patch(text_size=11, text_color=Colors140.DimGray))
text((22, 27), "```drawlib\n# Python Code\n```", style=styles.primary.patch(text_size=10, text_color=Colors140.MidnightBlue))

# 2. Engine (Center)
rectangle(
    (70, 40),
    width=34,
    height=44,
    r=4,
    style=styles.primary.patch(shape_fill_color=Colors140.Lavender, shape_line_color=purple_primary, shape_line_width=2.5),
)
text((70, 53), "drawlib compiler", style=styles.primary.patch(text_size=15, text_font=FontRoboto.ROBOTO_BOLD, text_color=purple_primary))
text((70, 43), "drawlib.doc_builder", style=styles.primary.patch(text_size=12, text_font=FontRoboto.ROBOTO_BOLD))
text((70, 31), "• AST Markdown Parser\n• In-Memory Code Runner\n• Canvas Reset & Isolation", style=styles.primary.patch(text_size=10, text_color=Colors140.DarkSlateGray))

# Connect Source -> Engine
line((38, 40), (53, 40), arrowhead="->", style=styles.primary.patch(line_width=2.5, line_color=blue_primary))

# 3. Targets (Right)
rectangle(
    (118, 62),
    width=34,
    height=16,
    r=3,
    style=styles.primary.patch(shape_fill_color=Colors140.HoneyDew, shape_line_color=green_primary, shape_line_width=2),
)
text((118, 65), "Rendered Markdown", style=styles.primary.patch(text_size=12, text_font=FontRoboto.ROBOTO_BOLD, text_color=green_primary))
text((118, 57), "docs/ (for GitHub Browsing)", style=styles.primary.patch(text_size=10, text_color=Colors140.DarkSlateGray))

rectangle(
    (118, 40),
    width=34,
    height=16,
    r=3,
    style=styles.primary.patch(shape_fill_color=Colors140.AliceBlue, shape_line_color=blue_primary, shape_line_width=2),
)
text((118, 43), "Responsive HTML Site", style=styles.primary.patch(text_size=12, text_font=FontRoboto.ROBOTO_BOLD, text_color=blue_primary))
text((118, 35), "docs_html/ (Static Website)", style=styles.primary.patch(text_size=10, text_color=Colors140.DarkSlateGray))

rectangle(
    (118, 18),
    width=34,
    height=16,
    r=3,
    style=styles.primary.patch(shape_fill_color=Colors140.Linen, shape_line_color=orange_primary, shape_line_width=2),
)
text((118, 21), "Headless Vector PDF", style=styles.primary.patch(text_size=12, text_font=FontRoboto.ROBOTO_BOLD, text_color=orange_primary))
text((118, 13), "doc.pdf (Chromium Print)", style=styles.primary.patch(text_size=10, text_color=Colors140.DarkSlateGray))

# Connect Engine -> Targets
line((87, 48), (101, 62), arrowhead="->", style=styles.primary.patch(line_width=2, line_color=green_primary))
line((87, 40), (101, 40), arrowhead="->", style=styles.primary.patch(line_width=2, line_color=blue_primary))
line((87, 32), (101, 18), arrowhead="->", style=styles.primary.patch(line_width=2, line_color=orange_primary))

save()
```

---

## 3. Directory Layout & Workflow

A typical Drawlib documentation project is structured as follows:

```text
my_project/
├── docs_src/                  # [SOURCE OF TRUTH] Edit your markdown files here
│   ├── index.md               # Main landing page (H1 title becomes site title)
│   ├── navbar.md              # Optional navigation hierarchy definition
│   ├── config.py              # Global Python configuration script
│   ├── style.css              # Custom stylesheet (customizable directly)
│   ├── template.html          # Jinja2 HTML layout (customizable directly)
│   ├── build.sh               # Project build script
│   ├── guides/                # Topic subdirectories containing .md files
│   └── images/                # Static assets (logos, screenshots)
│
├── docs/                      # [GENERATED] Compiled Markdown for GitHub
│   ├── index.md
│   └── *_images/              # Generated illustrations
│
└── docs_html/                 # [GENERATED] Compiled static HTML website
    ├── index.html
    ├── style.css              # Extracted CSS stylesheet
    └── *_images/              # Generated illustrations and copied static assets
```

> [!IMPORTANT]
> **The Golden Rule**: Never edit files in `docs/` or `docs_html/` directly. Always author documentation in `docs_src/` and build using the `drawlib build` CLI command.

---

## 4. Next Steps

- **[Code Block Syntax](./code_blocks.md)**: Learn how to embed and configure `drawlib` code blocks in Markdown.
- **[Building Documents](./building_docs.md)**: Compile your documents using the CLI and Python API.
- **[Templates & Styling](./templates_and_css.md)**: Customize Jinja2 templates and CSS styling.
- **[Project Scaffolding](./project_scaffolding.md)**: Bootstrap starter projects with `drawlib init`.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
