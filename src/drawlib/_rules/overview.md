# Drawlib Agent Drawing Guidelines

Drawlib is a modern Python diagramming and visualization library designed around the philosophy of **"Illustration as Code"**.  
It allows developers, system architects, and AI coding agents to create clean, publication-ready architectural schemas, workflows, data visualizations, and technical documentation using declarative, reproducible Python code.

This document serves as the high-level architectural foundation. When you need exhaustive function-by-function reference, refer to the on-demand topic rule commands detailed in [Section 4](#4-topic-reference-catalog--rules-commands).

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

```python
# Pattern A: Horizontal linear distribution with computed gaps
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import rectangle

config(width=120, height=40)
services = ["Auth API", "Core API", "Billing API", "Notify API"]
box_w, box_h = 20, 14
start_x, y, gap = 15, 20, 10

for i, name in enumerate(services):
    x = start_x + i * (box_w + gap) + (box_w / 2)
    rectangle((x, y), width=box_w, height=box_h, style="blue_flat", text=name, textstyle="white_bold")
    if i > 0:
        prev_right = start_x + (i - 1) * (box_w + gap) + box_w
        curr_left = start_x + i * (box_w + gap)
        line((prev_right, y), (curr_left, y), arrowhead="->", style="bold")

save()
```

```python
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
circle((center_x, center_y), radius=12, style="purple_flat", text="Data Hub", textstyle="white_bold")

# Satellite nodes
for i, label in enumerate(nodes):
    angle = (2 * math.pi / n) * i
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    circle((x, y), radius=8, style="green_flat", text=label, textstyle="white_bold")
    line((center_x, center_y), (x, y), arrowhead="->", style="bold")

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

---

## 3. Core Concept: Documentation Creation (Docs as Code)

Drawlib integrates a complete, standalone documentation compilation pipeline (`drawlib.doc_builder`). It compiles Markdown documents containing embedded ````drawlib```` code blocks into publication-ready static websites, GitHub-flavored Markdown, and headless vector PDFs without requiring external site generators.

### 3.1. Project Scaffolding Rule (`drawlib init`)
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

### 3.2. Standard Project Structure & Lifecycle
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

### 3.3. Navigation Bar (`navbar.md`) Rules
For multi-page documentation sites, `docs_src/navbar.md` defines the navigation sidebar:
1. **Site Title (Brand Name)**: The first `# Heading 1` (e.g. `# Drawlib Docs`) defines the brand title shown in the top-left sidebar header.
2. **Category Headings**: `## Heading 2` defines categorized sections (e.g. `## 1. Architecture`). Bullets before any `##` heading are top-level items.
3. **Links**: Bullet items `- [Title](path/to/file.md)` define page links. Anchors (`#sec`) and external URLs are supported.
4. **Build-Time Link Validation**: Every local link is strictly validated at build time. If any target file is missing, the build halts with an informative error detailing the exact line number.

### 3.4. Embedded Drawing Code Blocks (` ```drawlib `)
In Markdown source files under `docs_src/`, embed illustrations using the ````drawlib```` language fence:

````markdown
```drawlib 600px center show-code caption:"System Architecture Overview"
config(width=120, height=50)
rectangle((25, 25), width=30, height=20, style="blue_flat", text="Client")
rectangle((95, 25), width=30, height=20, style="green_flat", text="Service")
line((40, 25), (80, 25), arrowhead="->", style="bold")
```
````

**Block Header Options**:
- **Code Visibility**: `hide-code` (default, image only), `show-code` (code + image), `fold-code` (image + collapsed `<details>` dropdown).
- **Dimensions**: `400px`, `100%`, `w:600px`, `h:300px`.
- **Alignment**: `center`, `left`, `right`.
- **Caption & Filename**: `caption:"Figure Title"`, `file:custom_name.png`.

**Automatic Global Injection**: In `docs_src/` code blocks, all standard Drawlib domain symbols (`canvas`, `shapes`, `lines`, `text`, `icons`, `smartarts`, `charts`, `colors`) are automatically pre-imported. Boilerplate imports are not needed in Markdown blocks.

### 3.5. Build & Preview Commands
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

---

## 4. Topic Reference Catalog & Rules Commands

When writing or debugging Drawlib code, you can inspect detailed rules, full API signatures, and complete code examples on demand for any domain.

Execute `drawlib rules show <topic>` in your terminal or review the summarized rules below.

```bash
# List all available topics:
drawlib rules list

# Show rules for a specific topic:
drawlib rules show <topic>
```

---

### 4.1. CLI & Build Commands (`cli`)
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

### 4.2. Documentation Site Rules (`docs_build`)
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

### 4.3. Shapes Primitives & Styling (`shapes`)
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

### 4.4. Lines, Curves, & Arrowheads (`lines`)
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

### 4.5. Text Rendering & Typography (`text`)
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

### 4.6. Icons Library (`icons`)
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

### 4.7. Preset Styles & Color Palettes (`preset_styles`)
- **Command**: `drawlib rules show preset_styles`
- **Scope**: Systematic style naming rules (`<color>_<variant>`), built-in palettes (`ColorsDefault`, `ColorsMonochrome`, `ColorsEssentials`), pre-defined styles for shapes, lines, and text, and custom style registration.
- **Key Syntax**:
  ```python
  # Common preset styles: "blue_flat", "green_outline", "red_soft", "bold", "white_bold"
  rectangle((30, 30), width=20, height=10, style="purple_flat", textstyle="white_bold")
  ```
- **When to read**: Refer to this rule to maintain visual consistency, pick matching foreground/background colors, or define reusable corporate themes across a team.

---

### 4.8. Structured SmartArts Elements (`smartarts`)
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

### 4.9. Data Charts & Visualizations (`charts`)
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

### 4.10. Domain Diagrams (`diagrams`)
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

## 5. Agent Pair-Programming & Implementation Checklist

When tasked with generating or modifying Drawlib illustrations:

1. **Check Canvas Size & Aspect Ratio**:
   - Small icons / single components: `(60, 40)` or `(80, 50)`.
   - Standard architecture / flowcharts: `(120, 60)` or `(140, 70)`.
   - Comprehensive system overviews: `(160, 90)` (16:9) or `(120, 100)`.
2. **Prioritize High-Level Modules**:
   - Use `smartarts` or `diagrams` when applicable instead of assembling hundreds of raw rectangles and lines manually.
3. **Use Consistent Preset Styles**:
   - Prefer standard style strings (e.g. `style="blue_flat"`, `textstyle="white_bold"`) over hardcoded hex values to maintain clean aesthetic balance.
4. **Inspect with Fast Verification Commands**:
   - Do not rebuild the entire documentation site to test a single diagram edit.
   - Use `drawlib export <file> <index> -g -o scratch/check.png` to immediately verify visual results with a coordinate grid overlay.
