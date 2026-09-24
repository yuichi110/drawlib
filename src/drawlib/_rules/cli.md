# Drawlib CLI Guidelines

Drawlib provides a CLI for compiling documents, exporting individual diagrams, and managing caches.

## 1. Document Compiler (`drawlib build`)
Compile Markdown documentation, HTML sites, or headless PDFs:
```bash
# Compile Markdown document(s) with embedded ```drawlib code blocks:
drawlib build markdown docs_src/ -o docs/

# Compile documentation to responsive static HTML site:
drawlib build html docs_src/ -o docs_html/ --css google

# Compile single Markdown document to vector PDF via headless browser:
drawlib build pdf doc.md -o output.pdf --css google

# Execute Python drawing scripts in batch to generate image assets:
drawlib build images script_dir/ -o image_dir/
```
Key Options:
- `-o`, `--output <path>`: Destination output file or directory path.
- `-c`, `--config <path>`: Path to custom configuration script (e.g. `config.py`).
- `--css <name|path>`: Built-in CSS theme or custom CSS path. HTML: `default`, `default-dark`, `default-auto`, `google`, `google-dark`, `google-auto`, `github`, `minimal`, `monochrome`. PDF: `default`, `default-dark`, `google`, `google-dark`, `github`, `minimal`, `monochrome`.
- `--no-cache`: Force clean execution by ignoring SQLite image cache.

## 2. Embedded Markdown Code Blocks (```drawlib)
In Markdown documents, embed illustrations using the ````drawlib```` language fence.
Header options can be specified as space-separated tokens or `key:value` pairs:

````markdown
```drawlib 600px center show-code caption:"System Architecture"
from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=50)
circle((50, 25), radius=15)
save()
```
````

### Block Header Options:
- **Code Visibility**:
  - *(Default / omitted)*: Code is hidden; only the rendered image is displayed.
  - `show-code` (`code:show`, `code=show`): Displays Python code block followed by the rendered image.
  - `fold-code` (`code:fold`, `code=fold`): Displays rendered image followed by a collapsed `<details>` dropdown with Python code (omitted in PDF export).
- **Width**: `500px`, `100%`, `w:500px`, or integer `500` (e.g. `500px`).
- **Height**: `300px`, `h:300px`.
- **Alignment**: `center`, `left`, `right`, `a:center` (default: `center`).
- **Caption**: `caption:"Figure Title"` (displayed below image in `<figcaption>`).
- **Filename**: `file:custom_name.png` (explicit output image filename).
- **Format**: `format:png`, `format:webp` (default: `png`).
- **CSS Class**: `class:"shadow rounded"` (custom CSS classes on container).

## 3. Diagram Export & Inspection (`drawlib export`, `drawlib show`)
Render and verify individual illustrations without GUI popups:
```bash
# List all drawlib code blocks inside a Markdown file:
drawlib export doc.md

# Export specific block (1-based index) to image:
drawlib export doc.md 1 -o scratch/test.png

# Export standalone Python script with coordinate grid overlay:
drawlib export my_drawing.py -g -o scratch/debug_grid.png

# Open desktop GUI preview window:
drawlib show my_drawing.py --grid
```

## 4. Cache & Theme Utilities
```bash
# Check status of the SQLite image build cache:
drawlib cache status

# Clean the image build cache:
drawlib cache clean

# List built-in documentation CSS themes:
drawlib css list

# Export built-in Jinja2 sidebar template for customization:
drawlib template export custom.j2
```

## 5. Project Initialization (`drawlib init`)
Scaffold starter documentation projects with sample illustrations and working `docs_build.sh` scripts:
```bash
# List available starter project types:
drawlib init --list

# Initialize single document project in a new folder:
drawlib init simple my_project/

# Initialize multi-page responsive site directly in current project/repository:
drawlib init site --here

# Initialize multi-chapter PDF report with Table of Contents:
drawlib init pdf my_report/
```
