# Documentation Project & Build Overview

Drawlib is not only a drawing library—it is a **complete documentation compiler** that bridges executable Python illustrations and version-controlled technical documentation.

---

## The Documentation-as-Code Workflow

Instead of writing documentation in static wikis and manually copying and pasting PNG screenshots, Drawlib establishes a clean, repeatable build pipeline:

```drawlib 650px center file:doc_build_pipeline.png caption:"Drawlib Documentation Build Pipeline"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=120, height=45)

# Source folder
rectangle((24, 22.5), width=32, height=24, style=Styles.PrimaryFlat, text="Source of Truth\n\ndocs_src/\n(Markdown + Code)", text_style=Styles.WhiteBold)

# Build engine
rectangle((60, 22.5), width=24, height=16, style=Styles.AccentFlat, text="drawlib\nbuild", text_style=Styles.WhiteBold)

# Outputs
rectangle((98, 31), width=28, height=12, style=Styles.SuccessFlat, text="docs_html/ (Site)", text_style=Styles.WhiteBold)
rectangle((98, 14), width=28, height=12, style=Styles.SecondaryFlat, text="docs/ (GitHub MD)", text_style=Styles.WhiteBold)

# Lines
line((40, 22.5), (48, 22.5), arrowhead="->", style=Styles.PrimaryBold)
line((72, 25), (84, 31), arrowhead="->", style=Styles.PrimaryBold)
line((72, 20), (84, 14), arrowhead="->", style=Styles.PrimaryBold)
```

### The Golden Rule: `<name>_src/` is the Single Source of Truth
- Always edit Markdown files and Python code inside the source directory (e.g. `docs_src/`).
- Never edit the output directories (`docs/`, `docs_html/`, `docs.pdf`) directly; they are build artifacts completely overwritten during compilation.

---

## 1. Project Scaffolding (`drawlib init`)

Scaffold a complete project template with a single command:

```bash
# Initialize a multi-page documentation website
$ uv run drawlib init site

# Or scaffold into a custom output name (e.g., mybook_src/ -> mybook/):
$ uv run drawlib init site -o mybook
```

Drawlib supports four starter project types:
- **`site`**: Multi-page documentation website with sidebar navigation (`navbar.md`) and instant search.
- **`simple`**: Single technical specification or RFC document compiled to standalone HTML and GitHub Markdown.
- **`pdf`**: Multi-chapter formal technical publication compiled to vector PDF via headless Chromium.
- **`image`**: Standalone Python illustration scripts (`images_src/*.py`) batch-compiled to image files (`images/*.png`).

---

## 2. One-Command Compilation

Once initialized, compile your documentation using the generated `build.sh` script or the `drawlib build` CLI:

```bash
# Run the project build script
$ ./build.sh

# Or compile using the CLI directly:
$ uv run drawlib build html docs_src/ -o mybook_html/
$ uv run drawlib build markdown docs_src/ -o mybook/
```

During the build process:
1. Drawlib detects all ````drawlib```` code blocks across your Markdown documents.
2. The code blocks are executed in isolated memory spaces to render vector diagrams.
3. Images are cached intelligently (only modified code blocks re-render).
4. The final HTML website or rendered Markdown documents are generated with perfect image links.

---

## 3. Local Live Preview (`drawlib serve`)

Preview your compiled HTML site locally with automatic live inspection:

```bash
$ uv run drawlib serve docs_html/
```

Open `http://localhost:8000` in your browser to inspect the full documentation site, search index, and responsive styling.

---

> [!NOTE]
> For in-depth guides on code block attributes (`show-code`, `fold-code`, `caption:`), custom HTML templates, CSS theming, and Chromium PDF exports, see **[Chapter 6: Document Builder & CLI](../06_doc_builder_and_cli/overview.md)**.
