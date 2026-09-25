# Drawlib Agent Drawing Guidelines

Drawlib is a modern Python diagramming and visualization library designed around the philosophy of **"Illustration as Code"**.  
It allows developers, system architects, and AI coding agents to create clean, publication-ready architectural schemas, workflows, data visualizations, and technical documentation using declarative, reproducible Python code.

This document serves as the high-level architectural foundation. When you need exhaustive function-by-function reference, refer to the on-demand topic rule commands detailed in [Section 5](#5-topic-reference-catalog--rules-commands).

---

## 1. Core Concept: Illustration as Code

Traditional technical diagramming relies on drag-and-drop GUI applications (e.g., Microsoft Visio, Lucidchart, Figma, Draw.io). While accessible for quick whiteboard sketches, GUI tools introduce severe bottlenecks into professional software engineering workflows:
- **No Meaningful Version Control**: Binary files or monolithic XML/JSON blobs make git diffs unreadable and merge conflicts impossible to resolve collaboratively.
- **Visual Drift & Inconsistency**: Colors, border widths, spacing, and font sizes drift unpredictably across team members, diluting corporate branding and visual clarity.
- **Maintenance Overhead**: Keeping diagrams synchronized with rapid codebase evolution requires opening external tools, re-drawing elements manually, exporting raster assets, and moving files by hand.

### 1.1. The Illustration-as-Code Paradigm
Drawlib treats illustrations as software artifacts governed by the same rigorous engineering standards as source code:
1. **Plain Python Syntax**: Diagrams are authored in standard Python scripts (`.py`) or embedded directly inside Markdown documentation blocks (` ```drawlib `).
2. **Deterministic & Reproducible**: Geometry, spacing, palette shades, and typography are mathematically defined in code. Running the build script guarantees bit-for-bit identical visual output across all environments.
3. **Diff-Friendly Pull Requests**: Structural changes (such as inserting an API gateway, adding a microservice, or adjusting an OAuth handshake) appear as clear, human-readable code diffs.
4. **Programmatic Geometry & Math**: Standard Python constructs—loops, list comprehensions, math functions (`cos`, `sin`), and data structures—eliminate tedious manual positioning for repetitive grids, circular cycles, and trees.
5. **Centralized Style Governance**: Color palettes (`ColorsDefault`, `ColorsMonochrome`, `ColorsEssentials`) ensure that shapes, connectors, text, and icons adhere to a cohesive visual hierarchy across hundreds of figures.

### 1.2. Programmatic Layout Patterns
Unlike GUI tools where every coordinate is dragged by hand, Drawlib code leverages arithmetic and loops to compute perfect alignments:

```drawlib show-code
# Pattern A: Horizontal linear distribution with computed gaps
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import rectangle

config(width=140, height=40)
services = ["Auth API", "Core API", "Billing API", "Notify API"]
box_w, box_h = 20, 14
start_x, y, gap = 15, 20, 10

for i, name in enumerate(services):
    x = start_x + i * (box_w + gap) + (box_w / 2)
    rectangle((x, y), width=box_w, height=box_h, style=styles.blue_flat, text=name, textstyle=styles.white_bold)
    if i > 0:
        prev_right = start_x + (i - 1) * (box_w + gap) + box_w
        curr_left = start_x + i * (box_w + gap)
        line((prev_right, y), (curr_left, y), arrowhead="->", style=styles.bold)

save()
```

```drawlib show-code
# Pattern B: Radial / Circular distribution using trigonometry
import math
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import circle

config(width=100, height=100)
center_x, center_y, radius = 50, 50, 30
nodes = ["Ingest", "Transform", "Validate", "Store", "Index", "Serve"]
n = len(nodes)

# Central hub
circle((center_x, center_y), radius=12, style=styles.purple_flat, text="Data Hub", textstyle=styles.white_bold)

# Satellite nodes
for i, label in enumerate(nodes):
    angle = (2 * math.pi / n) * i
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    circle((x, y), radius=8, style=styles.green_flat, text=label, textstyle=styles.white_bold)

    # Connect hub edge to satellite edge without cutting through nodes
    lx1 = center_x + 13 * math.cos(angle)
    ly1 = center_y + 13 * math.sin(angle)
    lx2 = center_x + 21 * math.cos(angle)
    ly2 = center_y + 21 * math.sin(angle)
    line((lx1, ly1), (lx2, ly2), arrowhead="->", style=styles.bold)

save()
```

### 1.3. Software Engineering Best Practices for Drawing Code
To write maintainable illustrations that scale to large projects:
1. **Parameterize Geometry**: Define layout constants (`box_w`, `box_h`, `margin`, `gap`) at the top of functions instead of hardcoding magic numbers across dozens of coordinates.
2. **Componentize Recurring Sub-diagrams**: Wrap repeated visual clusters (e.g. a microservice pod consisting of a box, database icon, and health indicator) into Python functions.
3. **Decouple Data from Layout**: Model diagram contents as lists or dictionaries of dataclasses, then iterate over data to render graphical nodes. If a new service is added, only the data list changes.
4. **Use High-Level Abstractions First**: If a concept matches a SmartArts structure (`Table`, `TreeNode`, `MindMap`, `ChevronProcess`) or a domain diagram (`FlowDiagram`, `SequenceDiagram`, `ArchitectureDiagram`), use it instead of manually drawing basic primitives.

---

## 2. Core Concept: The Canvas System

The canvas represents the virtual Cartesian drawing plane upon which all graphical elements are rendered.

### 2.1. Coordinate System & Virtual Units
- **Origin `(0, 0)`**: Positioned strictly at the **bottom-left corner** of the canvas.
- **X-axis**: Extends horizontally to the **right** (`0 -> width`).
- **Y-axis**: Extends vertically **upward** (`0 -> height`).
- **Virtual Coordinate Units**: Canvas dimensions are expressed in resolution-independent virtual units (commonly `100x100`, `120x60`, or `160x90`). Virtual units decouple spatial composition from pixel rasterization density.

```text
(0, height) ┌─────────────────────────────────────────┐ (width, height)
            │                                         │
            │   Drawlib Cartesian Canvas Plane        │
            │   Y-axis increases UPWARD               │
            │                                         │
            │   (x, y) = shape anchor center          │
            │                                         │
    (0, 0)  └─────────────────────────────────────────┘ (width, 0)
            X-axis increases RIGHTWARD
```

### 2.2. Coordinate Alignment (`halign` & `valign`)
By default, all shapes, containers, and text blocks interpret coordinate `(x, y)` as the geometric **center** (`halign="center"`, `valign="center"`).  
Drawlib supports explicit anchor alignment to streamline layout construction without manual arithmetic offsets:
- **`halign` (Horizontal Alignment)**:
  - `"center"`: Anchor `x` is the horizontal midpoint of the element (default).
  - `"left"`: Anchor `x` is the left edge; element extends to the right (`x -> x + width`).
  - `"right"`: Anchor `x` is the right edge; element extends to the left (`x - width -> x`).
- **`valign` (Vertical Alignment)**:
  - `"center"`: Anchor `y` is the vertical midpoint of the element (default).
  - `"bottom"`: Anchor `y` is the bottom edge; element extends upward (`y -> y + height`).
  - `"top"`: Anchor `y` is the top edge; element extends downward (`y - height -> y`).

### 2.3. Canvas Lifecycle Functions
The `drawlib.canvas` module manages global drawing state:

| Function | Signature / Options | Description |
| :--- | :--- | :--- |
| `config()` | `width=100, height=100, background_color="#ffffff", dpi=300, ...` | Configures dimensions, canvas background color, rasterization resolution, and base settings. |
| `clear()` | *(no arguments)* | Flushes all buffered shapes and resets canvas state. Essential in multi-image batch scripts to prevent bleeding. |
| `save()` | `file_path=None, image_format="png", ...` | Renders the display list to disk. When omitted, writes to automatic sequence paths (`1.png`, etc.). |
| `get_dimage()` | *(no arguments)* | Returns an in-memory `Dimage` representation of the current canvas without saving to disk. |
| `show()` | `grid=False` | Opens an interactive local GUI desktop window displaying the rendered canvas. |

### 2.4. Aspect Ratio & Dimension Heuristics
Selecting optimal canvas dimensions depends on the visual content:
- **Square `100x100`**: Ideal for network graphs, circular workflows, mindmaps, state diagrams, and entity-relationship models.
- **Widescreen 16:9 `160x90`**: Optimal for architectural component overviews, multi-tier cloud deployments, and web banners.
- **Horizontal Landscape `120x50` / `140x60`**: Standard format for sequence diagrams, linear flowcharts, and multi-step pipeline chevrons.
- **Compact Component `60x40` / `80x50`**: Sizing for focused UI cards, isolated data models, or individual legend blocks.

### 2.5. Grid Overlay for Fast Alignment
Estimating pixel-perfect coordinates by trial-and-error wastes developer time. Drawlib provides a built-in coordinate grid overlay:
- Pass `grid=True` to `show()` in interactive environments:
  ```python
  from drawlib.canvas import show
  show(grid=True)
  ```
- Or run CLI headless export with `--grid` / `-g`:
  ```bash
  drawlib export my_drawing.py -g -o scratch/debug_grid.png
  ```
The grid overlays major coordinate lines, 10-unit numeric labels, and 5-unit subdivisions to make element placement intuitive.

### 2.6. Multi-Image Generation Patterns (`clear()`)
When a Python script produces multiple sequential illustrations (e.g. presentation slides, step-by-step algorithm stages, or variant designs), call `clear()` between images to prevent canvas bleeding:

```python
from drawlib.canvas import clear, config, save
from drawlib.shapes import rectangle

# Figure 1: Step 1
config(width=100, height=50)
rectangle((30, 25), width=25, height=18, style="blue_flat", text="Stage 1")
save("stage1.png")
clear()

# Figure 2: Step 2 with fresh canvas
config(width=100, height=50)
rectangle((30, 25), width=25, height=18, style="blue_flat", text="Stage 1")
rectangle((70, 25), width=25, height=18, style="green_flat", text="Stage 2")
save("stage2.png")
```

### 2.7. Typography & Canvas Theming
Canvas defaults can be globally customized via `config()` or in `docs_config.py`:
- **`background_color`**: Any hex code (`"#ffffff"`, `"#1e1e1e"`), RGB tuple, or named CSS color.
- **`dpi`**: Output resolution. Standard web images use `150`–`200`; high-resolution print or PDF exports specify `300`.
- **`font_family`**: Base system font family or bundled open fonts (e.g. `"sans-serif"`, `"monospace"`, `"Roboto"`).
- **`margin`**: Outer canvas padding preventing shapes placed on boundaries from being clipped.

### 2.8. Coordinate Geometry Helpers (`drawlib.math`)
Drawlib provides built-in geometric math utilities in `drawlib.math` so developers and agents do not need to implement manual trigonometry:
- **`get_angle(p1, p2)`**: Computes the counter-clockwise angle in degrees (`0` to `360`) from point `p1` to point `p2`. Essential for rotating shapes, aligning labels along angled connectors, or orienting arrowheads.
- **`get_distance(p1, p2)`**: Calculates the Euclidean distance between two points. Useful for dynamic sizing or threshold checks.
- **`get_center_and_size(points)`**: Takes a collection of coordinate tuples `[(x1, y1), (x2, y2), ...]` and returns `((center_x, center_y), (width, height))`. This enables dynamic bounding boxes around arbitrary clusters of nodes with zero manual math:

```python
from drawlib.canvas import config, save
from drawlib.math import get_angle, get_center_and_size, get_distance
from drawlib.shapes import circle, rectangle

config(width=100, height=80)
nodes = [(25, 30), (45, 55), (75, 40)]

# Automatically compute bounding container surrounding all nodes
(cx, cy), (w, h) = get_center_and_size(nodes)
rectangle((cx, cy), width=w + 16, height=h + 16, style="gray_light", text="Subsystem Boundary", valign="top")

for xy in nodes:
    circle(xy, radius=6, style="blue_flat")

save()
```

---

## 3. Core Concept: Visual Styles, Fonts & Media

Drawlib features a cohesive visual system comprising color catalogs, multi-language typography, strongly-typed style objects, and seamless image embedding.

### 3.1. Color Models & Palettes (`drawlib.colors`)
Colors in Drawlib can be represented as RGB tuples `(r, g, b)`, RGBA tuples `(r, g, b, a)`, hex strings, or constants from curated palettes:
- **Hex & Alpha Helpers**:
  - `from_hex("#3498db", alpha=0.8)`: Converts standard hex codes into validated Drawlib RGBA tuples.
  - `with_alpha(color, alpha=0.5)`: Derives a new transparent color from any existing RGB or RGBA color.
  - `from_grayscale(128, alpha=1.0)`: Creates grayscale tones from 0 (black) to 255 (white).
- **Curated Palette Catalogs**:
  - **`ColorsDefault`**: Basic corporate primary palette (`Red`, `Green`, `Blue`, `Black`, `White`).
  - **`ColorsEssentials`**: Rich, modern UI palette (`Blue`, `Green`, `Red`, `Orange`, `Purple`, `Cyan`, `Yellow`, `Gray`, `LightGray`, `DarkGray`).
  - **`ColorsMonochrome`**: High-contrast grayscale shades (`Black`, `White`, `Gray`, `DarkGray`, `LightGray`).
  - **`Colors140`**: All 140 W3C standard CSS color constants (`Tomato`, `SteelBlue`, `MediumSeaGreen`, etc.).

### 3.2. Typography & Font System (`drawlib.fonts`)
Drawlib ensures dependable cross-platform rendering by bundling standard open fonts and managing font caching automatically:
- **Universal CJK + Latin Font (`Font`)**:
  - `Font.SERIF`, `Font.SANS_SERIF`, `Font.MONO_SPACE`: Automatically fall back across Latin, Japanese, Simplified Chinese, Traditional Chinese, and Korean characters without square box glyph corruption (豆腐).
- **Typography Collections**:
  - **`FontRoboto`**: Clean Google Roboto typeface with weights (`THIN`, `LIGHT`, `REGULAR`, `MEDIUM`, `BOLD`, `BLACK`).
  - **`FontMonoSpace`**: Monospace typefaces for code listings and console output (`ROBOTO_MONO_REGULAR`, `COURIER_REGULAR`).
  - **`FontSansSerif`** & **`FontSerif`**: Standard Western editorial typefaces.
  - **`FontJapanese`**, **`FontChinese`**, **`FontArabic`**: Dedicated regional typefaces.
- **Custom Fonts (`FontFile`)**:
  - Load local TTF/OTF files with automatic caching: `FontFile("assets/fonts/BrandFont.ttf")`.

### 3.3. Strongly-Typed Style Architecture (`drawlib.types`)
Every visual element in Drawlib is governed by clean, strongly-typed style objects:
- **`Style` Model**:
  - Encapsulates properties: `fill_color`, `line_color`, `line_width`, `line_style`, `text_size`, `text_color`, `text_font`, `text_weight`, and `alpha`.
  - Can be customized directly:
    ```python
    from drawlib.types import Style
    my_style = Style(fill_color=(240, 248, 255), line_color=(30, 144, 255), line_width=2)
    ```
  - **Immutability & Safety**: Use `style.copy()` when deriving modified variants to prevent mutation side-effects.
- **Extensible Base Classes**:
  - Subclass `BasePresetStyles` to define reusable brand style systems across a corporate team.
  - Inherit from `ColorsBase` and `FontBase` to structure enterprise palette and typography definitions.

### 3.4. Image & Media Embedding (`drawlib.images`)
Drawlib allows seamless integration of raster and vector graphic assets into diagrams:
- **`image()` Function**:
  - Renders external PNG, JPEG, SVG, or WebP images: `image((50, 40), width=24, image="assets/logo.png")`.
  - Automatic aspect ratio calculation: specifying only `width` automatically scales `height` proportionally.
  - Tinting & Alpha: Apply color overlays and transparency directly to embedded graphics.
- **In-Memory Diagram Nesting (`Dimage` & `get_dimage_from_code`)**:
  - `canvas.get_dimage()`: Captures the current canvas state as an in-memory `Dimage` object.
  - `get_dimage_from_code(code_str)`: Compiles an independent Drawlib script in memory and embeds the output inside another canvas, facilitating composite multi-diagram figures.

---

## 4. Core Concept: Documentation Creation (Docs as Code & tools)

Drawlib integrates a complete, standalone documentation compilation pipeline (`drawlib.doc_builder` and `drawlib.tools`). It compiles Markdown documents containing embedded ````drawlib```` code blocks into publication-ready static websites, GitHub-flavored Markdown, and headless vector PDFs without requiring external site generators.

### 4.1. Project Scaffolding Rule (`drawlib init`)
> **Important Scaffolding Rule**: Never create documentation project files or directories by hand from scratch.  
> Always use `drawlib init` to scaffold the standard structure, default configuration, and build scripts.

```bash
# List available starter templates:
drawlib init --list

# Scaffold a multi-page documentation website in the current repository:
drawlib init site --here

# Scaffold a multi-page documentation website in a new subfolder:
drawlib init site my_docs/

# Scaffold a single-page document or PDF report:
drawlib init simple my_doc/
drawlib init pdf my_report/
```

### 4.2. Standard Project Structure & Lifecycle
A standard documentation project initialized via `drawlib init site` follows this structure:

```text
my_project/
├── docs_src/                  # [SOURCE OF TRUTH] Only author/edit files here!
│   ├── index.md               # [MANDATORY] Root landing page
│   ├── navbar.md              # [MANDATORY] Sidebar navigation menu definition
│   ├── architecture/          # Chapter / topic subdirectories
│   │   └── index.md
│   └── workflow/
│       └── index.md
├── docs_config.py             # Global canvas defaults, custom styles, fonts
├── docs_build.sh              # Unified build automation script
├── docs/                      # [GENERATED] Rendered Markdown site for GitHub browsing
└── docs_html/                 # [GENERATED] Responsive static HTML site with sidebar
```

**The Golden Rule of Documentation**: Never manually edit files in `docs/` or `docs_html/`. All manual edits, additions, and updates must take place inside `docs_src/`. Build outputs are regenerated automatically.

### 4.3. Navigation Bar (`navbar.md`) Rules
For multi-page documentation sites, `docs_src/navbar.md` defines the navigation sidebar:
1. **Site Title (Brand Name)**: The first `# Heading 1` (e.g. `# Drawlib Docs`) defines the brand title shown in the top-left sidebar header.
2. **Category Headings**: `## Heading 2` defines categorized sections (e.g. `## 1. Architecture`). Bullets before any `##` heading are top-level items.
3. **Links**: Bullet items `- [Title](path/to/file.md)` define page links. Anchors (`#sec`) and external URLs are supported.
4. **Build-Time Link Validation**: Every local link is strictly validated at build time. If any target file is missing, the build halts with an informative error detailing the exact line number.

### 4.4. Embedded Drawing Code Blocks (` ```drawlib `)
In Markdown source files under `docs_src/`, embed illustrations using the ````drawlib```` language fence:

````markdown
```drawlib 600px center show-code caption:"System Architecture Overview"
config(width=120, height=50)
rectangle((25, 25), width=30, height=20, style=styles.blue_flat, text="Client", textstyle=styles.white_bold)
rectangle((95, 25), width=30, height=20, style=styles.green_flat, text="Service", textstyle=styles.white_bold)
line((40, 25), (80, 25), arrowhead="->", style=styles.bold)
```
````

**Block Header Options**:
- **Code Visibility**: `hide-code` (default, image only), `show-code` (code + image), `fold-code` (image + collapsed `<details>` dropdown).
- **Dimensions**: `400px`, `100%`, `w:600px`, `h:300px`.
- **Alignment**: `center`, `left`, `right`.
- **Caption & Filename**: `caption:"Figure Title"`, `file:custom_name.png`.

**Automatic Global Injection**: In `docs_src/` code blocks, all standard Drawlib domain symbols (`canvas`, `shapes`, `lines`, `text`, `icons`, `smartarts`, `charts`, `colors`) are automatically pre-imported. Boilerplate imports are not needed in Markdown blocks.

### 4.5. Build & Preview Commands
```bash
# Run full documentation build via script:
./docs_build.sh

# Or compile manually via CLI:
drawlib build html docs_src/ -o docs_html/ -c docs_config.py --css google
drawlib build markdown docs_src/ -o docs/ -c docs_config.py
drawlib build pdf docs_src/index.md -o output.pdf -c docs_config.py --css google

# Preview static HTML site locally with automatic link checking:
drawlib serve docs_html/

# Validate broken links without launching web server:
drawlib serve docs_html/ --check
```

### 4.6. Python Developer Tools API (`drawlib.tools`)
When you need to execute CLI operations programmatically (e.g. inside Python build automation, pytest verification suites, or automated CI pipelines), use `drawlib.tools`:

```python
from drawlib.tools import build_html, build_markdown, export_block

# Export a single diagram from a Markdown file
image_path = export_block(
    file_path="docs_src/architecture.md",
    block_id="1",
    output_path="scratch/preview.png",
    show_grid=True,
)

# Compile full HTML site programmatically
build_html(
    src="docs_src/",
    output="docs_html/",
    config="docs_config.py",
    css="google",
)
```

| Function | Equivalent CLI Command | Primary Use Case |
| :--- | :--- | :--- |
| `build_html()` | `drawlib build html` | Compile static documentation sites or standalone HTML files. |
| `build_markdown()` | `drawlib build markdown` | Render documentation for GitHub viewing with linked images. |
| `build_pdf()` | `drawlib build pdf` | Export print-ready PDFs via headless browser. |
| `export_block()` | `drawlib export` | Fast illustration rendering for AI self-verification and tests. |
| `init_project()` | `drawlib init` | Programmatic repository scaffolding. |
| `serve_docs()` | `drawlib serve` | Local preview server and link verification checks. |
| `clear_cache()` | `drawlib cache clear` | Cache cleanup. |

---

## 5. Topic Reference Catalog & Rules Commands

When writing or debugging Drawlib code, you can inspect detailed rules, full API signatures, and complete code examples on demand for any domain.

Execute `drawlib rules show <topic>` in your terminal or review the summarized rules below.
When called, Drawlib automatically compiles illustrations on demand, caches companion PNG images in `drawlib/_assets/rules/`, and provides relative image links that AI coding agents can directly inspect with their image viewing tools (`view_file`) for multimodal spatial verification.

```bash
# List all available topics and cache status:
drawlib rules list

# Show rules for a specific topic (builds illustrations on demand):
drawlib rules show <topic>

# Force recompile illustrations:
drawlib rules show <topic> --rebuild
```

---

### 5.1. CLI & Build Commands (`cli`)
- **Command**: `drawlib rules show cli`
- **Scope**: Document compilation (`build`), single illustration export (`export`), desktop preview (`show`), project scaffolding (`init`), local documentation server (`serve`), and cache management (`cache`).
- **Key Syntax**:
  ```bash
  drawlib build html docs_src/ -o docs_html/ --css google
  drawlib export script.py -g -o scratch/preview.png
  drawlib init site --here
  ```
- **When to read**: Refer to this rule when automating build pipelines, setting up CI/CD, configuring custom themes/templates, or debugging CLI flags.

---

### 5.2. Documentation Site Rules (`docs_build`)
- **Command**: `drawlib rules show docs_build`
- **Scope**: Multi-page documentation architecture, `navbar.md` authoring syntax, broken-link prevention, code block options, and agent authoring workflows.
- **Key Syntax**:
  ```markdown
  # Site Brand Name
  - [Home](index.md)
  ## Category Name
  - [Chapter 1](chapter1/index.md)
  ```
- **When to read**: Refer to this rule when adding chapters, configuring navigation sidebars, troubleshooting missing document errors, or structuring new documentation sites.

---

### 5.3. Shapes Primitives & Styling (`shapes`)
- **Command**: `drawlib rules show shapes`
- **Scope**: All 22 geometric shape functions including `rectangle`, `circle`, `donuts`, `ellipse`, `wedge`, `fan`, `arc`, `parallelogram`, `rhombus`, `trapezoid`, `triangle`, `regularpolygon`, `polygon`, `star`, `arrow`, `arrow_l`, `arrow_u`, `arrow_arc`, `arrow_polyline`, and `chevron`.
- **Key Syntax**:
  ```python
  from drawlib.shapes import circle, rectangle
  rectangle((30, 25), width=20, height=15, style="blue_flat", text="Box")
  circle((70, 25), radius=8, style="green_outline")
  ```
- **When to read**: Refer to this rule when selecting the right geometric primitive, styling shape borders and fills, rounding corners, rotating shapes, or embedding centered text inside containers.

---

### 5.4. Lines, Curves, & Arrowheads (`lines`)
- **Command**: `drawlib rules show lines`
- **Scope**: Straight lines (`line`), curved splines (`line_curved`), Bezier paths (`line_bezier1`, `line_bezier2`), multi-point chained lines (`lines`, `lines_curved`), and circular arcs (`line_arc`).
- **Key Syntax**:
  ```python
  from drawlib.lines import line, line_curved
  line((10, 20), (40, 20), arrowhead="->", style="bold")
  line_curved((50, 20), (80, 40), bend=0.3, arrowhead="<->", style="dashed")
  ```
- **When to read**: Refer to this rule when connecting diagram nodes, configuring arrowheads (`->`, `<-`, `<->`, `-`), routing complex paths, or adjusting curve bending parameters.

---

### 5.5. Text Rendering & Typography (`text`)
- **Command**: `drawlib rules show text`
- **Scope**: Standalone labels, multi-line paragraphs, text alignment (`halign`, `valign`), rotation angles, typography options (`TextStyle`), custom fonts, and background text boxes.
- **Key Syntax**:
  ```python
  from drawlib.text import text
  text((50, 80), "Architecture Diagram", style="title_bold", halign="center")
  text((10, 50), "Line 1\nLine 2", fontsize=12, color="#555555", halign="left")
  ```
- **When to read**: Refer to this rule when fine-tuning title typography, aligning table headers, formatting multiline captions, or rotating vertical axis labels.

---

### 5.6. Icons Library (`icons`)
- **Command**: `drawlib rules show icons`
- **Scope**: Vector and PNG icons from Phosphor, FontAwesome, and Google Cloud Platform (GCP) official architecture libraries.
- **Key Syntax**:
  ```python
  from drawlib.icons import font_icon, gcp, phosphor
  phosphor.desktop((20, 30), width=10, style="blue_flat")
  gcp.compute_engine((50, 30), width=12)
  font_icon((80, 30), "fa-database", width=10)
  ```
- **When to read**: Refer to this rule when enriching cloud architecture diagrams, UI mockups, server schemas, or process flows with standardized industry iconography.

---

### 5.7. Preset Styles & Color Palettes (`preset_styles`)
- **Command**: `drawlib rules show preset_styles`
- **Scope**: Systematic style naming rules (`<color>_<variant>`), built-in palettes (`ColorsDefault`, `ColorsMonochrome`, `ColorsEssentials`), pre-defined styles for shapes, lines, and text, and custom style registration.
- **Key Syntax**:
  ```python
  # Common preset styles: "blue_flat", "green_outline", "red_soft", "bold", "white_bold"
  rectangle((30, 30), width=20, height=10, style="purple_flat", textstyle="white_bold")
  ```
- **When to read**: Refer to this rule to maintain visual consistency, pick matching foreground/background colors, or define reusable corporate themes across a team.

---

### 5.8. Structured SmartArts Elements (`smartarts`)
- **Command**: `drawlib rules show smartarts`
- **Scope**: High-level visual abstractions including `Table`, `TreeNode` / `tree`, `MindMapNode` / `mindmap`, `BoxList`, `BulletPoints`, `ChevronProcess`, `Cycle`, `GridLayout`, `Pyramid`, `SourceCode`, and `bubblespeech`.
- **Key Syntax**:
  ```python
  from drawlib.smartarts import ChevronProcess, Table
  ChevronProcess((10, 20), width=80, height=15, items=["Plan", "Build", "Deploy"]).draw()
  Table((10, 50), data=[["Header A", "Header B"], ["Val 1", "Val 2"]]).draw()
  ```
- **When to read**: Refer to this rule when presenting structured data, comparison tables, step-by-step lifecycles, organizational trees, or formatted code snippets without manual geometry math.

---

### 5.9. Data Charts & Visualizations (`charts`)
- **Command**: `drawlib rules show charts`
- **Scope**: Statistical and planning charts: `BarChart` (grouped, stacked, horizontal), `LineChart`, `AreaChart`, `PieChart` / donut, `RadarChart`, `ScatterChart`, and `GanttChart`.
- **Key Syntax**:
  ```python
  from drawlib.charts import BarChart, BarSeries
  BarChart((10, 10), width=80, height=60, categories=["Q1", "Q2", "Q3"]) \
      .add_series(BarSeries("Revenue", [100, 140, 180], color="blue")) \
      .draw()
  ```
- **When to read**: Refer to this rule when plotting quantitative metrics, project management schedules, comparison radars, or trend analyses.

---

### 5.10. Domain Diagrams (`diagrams`)
- **Command**: `drawlib rules show diagrams`
- **Scope**: Specialized software engineering diagrams: `ArchitectureDiagram`, `FlowDiagram`, `SequenceDiagram`, `StateDiagram`, `ClassDiagram`, and `ERDiagram`.
- **Key Syntax**:
  ```python
  from drawlib.diagrams.flow import FlowDiagram
  flow = FlowDiagram((10, 10), width=80, height=60)
  start = flow.node("Start", shape="circle")
  step = flow.node("Process", shape="rectangle")
  flow.edge(start, step, label="execute")
  flow.draw()
  ```
- **When to read**: Refer to this rule when modeling UML designs, entity relationships, protocol handshakes, state machines, or distributed system microservices.

---

### 5.11. Canvas Lifecycle & Dimensions (`canvas`)
- **Command**: `drawlib rules show canvas`
- **Scope**: Canvas singleton (`canvas`), configuration parameters (`config`), coordinate grids, background transparency, image saving (`save`), in-memory Dimage generation (`get_dimage`), and canvas clearing (`clear`).
- **Key Syntax**:
  ```python
  from drawlib.canvas import clear, config, save
  config(width=140, height=70, background_color=(250, 250, 250))
  save("output.png")
  ```
- **When to read**: Refer to this rule when setting up canvas boundaries, debugging multi-image scripts, configuring coordinate grid overlays, or exporting in-memory illustrations.

---

### 5.12. Color Models, Catalogs & Palettes (`colors`)
- **Command**: `drawlib rules show colors`
- **Scope**: RGB/RGBA formats, standard 16 web colors (`Colors`), 140 CSS colors (`Colors140`), curated theme palettes (`ColorsDefault`, `ColorsMonochrome`), and conversion utilities (`from_hex`, `from_grayscale`, `with_alpha`).
- **Key Syntax**:
  ```python
  from drawlib.colors import Colors, ColorsDefault, from_hex, with_alpha
  c1 = from_hex("#3498db", alpha=0.8)
  c2 = with_alpha(ColorsDefault.Blue, 0.2)
  ```
- **When to read**: Refer to this rule when choosing accessible color schemes, parsing brand hex values, adjusting transparency, or creating custom palette classes.

---

### 5.13. Typography, Fonts & Cache (`fonts`)
- **Command**: `drawlib rules show fonts`
- **Scope**: Universal CJK + Latin font (`Font`), Western typography (`FontRoboto`, `FontSansSerif`, `FontMonoSpace`), non-Latin regional scripts (`FontJapanese`, `FontChinese`, `FontArabic`), custom font loading (`FontFile`), and cache management.
- **Key Syntax**:
  ```python
  from drawlib.fonts import Font, FontFile, FontRoboto
  custom_font = FontFile("fonts/brand.ttf")
  ```
- **When to read**: Refer to this rule when selecting typographic weights, rendering multi-language diagrams, formatting monospace source code, or loading custom brand typefaces.

---

### 5.14. Image & Graphic Embedding (`images`)
- **Command**: `drawlib rules show images`
- **Scope**: Embedding raster and vector images (`image`), aspect ratio handling, image transformation model (`Dimage`), color tinting, and dynamic in-memory diagram embedding (`get_dimage_from_code`).
- **Key Syntax**:
  ```python
  from drawlib.images import Dimage, get_dimage_from_code, image
  image((50, 30), width=20, image="logo.png")
  ```
- **When to read**: Refer to this rule when incorporating company logos, external architecture badges, screenshots, or composing nested diagrams dynamically.

---

### 5.15. Geometry & Coordinate Math (`math`)
- **Command**: `drawlib rules show math`
- **Scope**: Geometric derivations: counter-clockwise angle between two points (`get_angle`), Euclidean distance (`get_distance`), and automated bounding box calculation (`get_center_and_size`).
- **Key Syntax**:
  ```python
  from drawlib.math import get_angle, get_center_and_size, get_distance
  angle = get_angle(p1, p2)
  (cx, cy), (w, h) = get_center_and_size([(10, 20), (40, 50), (30, 10)])
  ```
- **When to read**: Refer to this rule when aligning text along slanted lines, distributing nodes radially along circular paths, or automatically bounding clusters of nodes.

---

### 5.16. Style Models, Base Classes & Types (`types`)
- **Command**: `drawlib rules show types`
- **Scope**: Strongly-typed `Style` model attributes (fill, line, typography, alignments), theme inheritance (`BasePresetStyles`), palette extension (`ColorsBase`), and Drawlib type alias conventions.
- **Key Syntax**:
  ```python
  from drawlib.types import BasePresetStyles, Style
  custom_style = Style(fill_color=(50, 100, 200), line_width=2, text_size=14)
  ```
- **When to read**: Refer to this rule when building reusable design systems, encapsulating corporate styles, or writing type-safe drawing utilities.

---

### 5.17. Developer Tools API (`tools`)
- **Command**: `drawlib rules show tools`
- **Scope**: Programmatic Python developer API for document compilation (`build_html`, `build_markdown`, `build_pdf`), single illustration extraction (`export_block`), project scaffolding (`init_project`), local server (`serve_docs`), and cache management.
- **Key Syntax**:
  ```python
  from drawlib.tools import build_html, export_block
  build_html("docs_src/", "docs_html/")
  export_block("docs_src/arch.md", "1", "output.png")
  ```
- **When to read**: Refer to this rule when automating build scripts in Python, writing test assertions with pytest, or triggering on-demand diagram exports from custom automation sidecars.

---

## 6. Autonomous AI Workflow & Implementation Guide

When an AI coding agent is tasked with creating, modifying, or reviewing Drawlib illustrations, adhere to the following workflow principles to guarantee deterministic, publication-quality results.

### 6.1. The Autonomous Self-Correction Loop

Never deliver unverified drawing code to the user. Always execute the autonomous feedback loop before reporting task completion:

```text
1. User Request ──> 2. AI Writes Code ──> 3. Render Image (-g) ──> 4. Multimodal Review
                           ▲                                                │
                           └──────── 5. Issues Found? Fix & Retry ──────────┘
                                                │ (Pass)
                                                ▼
                                        6. Human Inspection
```

1. **Step 1: Understand Requirements & Context**: Inspect the user's instructions and related repository context (source files, data models, APIs).
2. **Step 2: Generate Declarative Drawlib Code**: Write standard Python drawing code or embedded Markdown blocks using appropriate canvas bounds and semantic styles.
3. **Step 3: Headless Image Render with Coordinate Grid (`-g`)**: Render the canvas immediately to a temporary location using Drawlib's fast export command:
   ```bash
   # For a standalone Python script:
   uv run drawlib export scratch/preview.py -g -o scratch/preview.png

   # For embedded block 1 in a Markdown document:
   uv run drawlib export docs_src/my_doc.md 1 -g -o scratch/preview.png
   ```
4. **Step 4: Multimodal Self-Review (`view_file`)**: Use your image inspection capability to check the rendered grid image. Check for:
   - Overlapping shapes, clipped text boxes, or text colliding with borders.
   - Arrowhead routing that cuts through elements instead of connecting boundary edges cleanly.
   - Unbalanced whitespace, disproportionate element scales, or poorly centered groups.
5. **Step 5: Autonomous Coordinate Adjustment**: If any aesthetic or spatial defects are found, adjust coordinates, margins, or canvas size in the code and re-render. Repeat until the layout is clean.
6. **Step 6: Deliver & Human Verification**: Present the final diagram to the user.

---

### 6.2. Prototyping in Scratch Workspace & Image Presentation

If your environment or chat interface supports presenting images directly to the user (e.g. via artifact embedding, Markdown image links, or UI previews):

1. **Work in Temporary / Scratch Workspace First**:
   - Create a scratch prototype script (e.g. `scratch/test_diagram.py`) rather than immediately editing production files or documentation sources.
   - Execute the script to generate an image (e.g. `scratch/test_diagram.png`).
2. **Show the Rendered Image to the User**:
   - Present the rendered visual illustration directly to the user along with your explanation.
   - Inspecting an image is 10x faster and clearer for the user than reading raw 2D coordinate code.
3. **Promote to Production After Confirmation**:
   - Once the user approves the visual design, transfer the finalized code to the target Markdown document (`docs_src/`) or production Python module.

---

### 6.3. Prefer High-Level SmartArts & Diagrams over Raw Primitives

Avoid manually placing dozens of low-level `rectangle`, `circle`, and `line` primitives whenever a higher-level abstraction exists.

1. **Evaluate SmartArts & Domain Diagrams First**:
   - **Pipelines & Lifecycles**: Use `ChevronProcess` or `Cycle` instead of manual chevrons and arrow lines.
   - **Hierarchies & Organizations**: Use `TreeNode` / `tree` or `MindMapNode` / `mindmap` instead of calculating recursive tree node coordinates.
   - **Tabular Data & Comparisons**: Use `Table` instead of manually drawing grids of lines and text cells.
   - **Status Cards & Matrices**: Use `BoxList` or `GridLayout` instead of looping through offset formulas.
   - **Software Architecture & Flows**: Use `ArchitectureDiagram`, `FlowDiagram`, `SequenceDiagram`, or `ERDiagram`.
2. **Proactively Suggest High-Level Alternatives**:
   - If a user's prompt asks for a diagram that could be expressed as a structured SmartArt or Domain Diagram, proactively propose using the high-level module:
     > *"We can assemble this workflow using `ChevronProcess` from `drawlib.smartarts`, which automatically handles chevron geometry, arrow padding, and responsive spacing without manual coordinate math."*
3. **When to Use Raw Primitives (`shapes`, `lines`, `text`)**:
   - Use raw primitives when creating entirely custom, non-standard visual metaphors, bespoke UI mockups, or composite badges that do not fit into existing high-level components.

---

### 6.4. Implementation Checklist

- [ ] **Canvas Sizing**: Set explicit dimensions (`100x100`, `120x60`, `140x70`, `160x90`) appropriate for the diagram type.
- [ ] **Palette Consistency**: Use semantic preset styles (e.g. `style="blue_flat"`, `textstyle="white_bold"`) or official palettes (`ColorsDefault`, `ColorsMonochrome`) instead of hardcoded hex values.
- [ ] **Grid Overlay Validation**: Superimpose coordinate grids (`-g`) during self-correction to eliminate guesswork.
- [ ] **Clean Separation of Concerns**: Decouple data lists/dictionaries from drawing loops for maintainability.
