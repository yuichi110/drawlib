# Drawlib Agent Drawing Guidelines (Minimal)

Drawlib is a pure-Python library for **"Illustration as Code"** and **"Documentation as Code"**.
It enables developers and AI coding agents to create architectural schemas, workflows, and technical diagrams using declarative, reproducible Python code.

> **Note**: This is a concise, context-optimized guide (<10k characters). If you need the exhaustive, comprehensive architectural manual and deep conceptual explanations, run:
> ```bash
> uv run drawlib rules show overview
> ```

---

## 1. Autonomous AI Workflow & Feedback Loop

When tasked with generating or updating Drawlib diagrams, execute this self-correction loop before handing results to the user:

```text
1. User Request ──> 2. AI Writes Code ──> 3. Render Image (-g) ──> 4. Multimodal Review
                           ▲                                                │
                           └──────── 5. Issues Found? Fix & Retry ──────────┘
                                                │ (Pass)
                                                ▼
                                        6. Human Inspection
```

1. **Inspect Context**: Check real repository files (`models.py`, API routes, config) to ground the diagram in code.
2. **Prototype in Scratch**: Write code in `scratch/test_diagram.py` instead of directly modifying production files.
3. **Render Immediately with Coordinate Grid (`-g`)**:
   ```bash
   uv run drawlib export scratch/test_diagram.py -g -o scratch/test_diagram.png
   # Or for Markdown embedded block 1:
   uv run drawlib export docs_src/doc.md 1 -g -o scratch/test_diagram.png
   ```
4. **Multimodal Self-Review (`view_file`)**: Inspect `scratch/test_diagram.png`. Check for overlaps, text clipping, bad routing, or uneven whitespace.
5. **Auto-Adjust & Iterate**: Fix coordinates and re-export until the layout is balanced.
6. **Show Rendered Image to User**: Present the image to the user for quick visual sign-off before committing.

**Related Rules**:
- CLI & Fast Verification: `uv run drawlib rules show cli`

---

## 2. Core Concepts: Canvas & Geometry

- **Origin `(0, 0)`**: Strictly at the **bottom-left corner**. X increases rightward; Y increases upward.
- **Default Center Anchor**: Shape and text coordinates `(x, y)` define the geometric **center** by default.
- **Canvas Sizing**: `80x40` (badges), `140x70` (flows/architecture/sequence), `160x90` (widescreen).
- **Multi-Image Scripts**: Always call `clear()` between sequential images to avoid canvas bleeding.
- **In-Memory Rendering (`canvas`)**: `canvas.get_dimage()` captures the canvas as an in-memory `Dimage` object.
- **Geometry Helpers (`drawlib.math`)**:
  - `get_angle(p1, p2)`: Counter-clockwise angle (0–360°) from `p1` to `p2` for rotating shapes or angled labels.
  - `get_distance(p1, p2)`: Euclidean distance between coordinates.
  - `get_center_and_size(points)`: Returns `((cx, cy), (w, h))` bounding box around multiple points for dynamic containers.

```python
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.config import styles
from drawlib.shapes import rectangle
from drawlib.text import text

setup(width=120, height=50)
rectangle((30, 25), width=28, height=16, style=styles.blue_flat, text="Service A", textstyle=styles.white_bold)
rectangle((90, 25), width=28, height=16, style=styles.green_flat, text="Service B", textstyle=styles.white_bold)
line((44, 25), (76, 25), arrowhead="->", style=styles.bold)
save()
```

**Related Rules**:
- Canvas & Sizing Detail: `uv run drawlib rules show canvas`
- Shapes Detail (22 primitives): `uv run drawlib rules show shapes`
- Lines & Routing Detail: `uv run drawlib rules show lines`
- Text & Fonts Detail: `uv run drawlib rules show text`
- Math & Coordinate Helpers: `uv run drawlib rules show math`

---

## 3. High-Level Abstractions: Prefer SmartArts & Diagrams

Avoid manually placing dozens of low-level `rectangle` and `line` primitives when a structured component fits:

| Diagram Purpose | Recommended High-Level Module | Alternative |
| :--- | :--- | :--- |
| **Linear Pipeline / Stages** | `drawlib.smartarts.ChevronProcess` | Manual chevrons |
| **Hierarchical Tree / Org** | `drawlib.smartarts.tree`, `TreeNode` | Manual recursive math |
| **Central Mind Map** | `drawlib.smartarts.mindmap`, `MindMapNode` | Manual radial math |
| **Tabular Data / Matrix** | `drawlib.smartarts.Table` | Grid of lines & text |
| **Card Grids / Status Lists** | `drawlib.smartarts.GridLayout`, `BoxList` | Nested coordinate loops |
| **Circular Feedback Loop** | `drawlib.smartarts.Cycle` | Manual arcs & arrows |
| **Flowchart / State Machine** | `drawlib.diagrams.flow.FlowDiagram` | Raw boxes and lines |
| **Microservices & Cloud** | `drawlib.diagrams.architecture.ArchitectureDiagram` | Raw icons and lines |
| **API Sequences & Protocols**| `drawlib.diagrams.sequence.SequenceDiagram` | Raw lifelines & text |
| **Database Schema / ER** | `drawlib.diagrams.er.ERDiagram` | Raw entity boxes |

> **Rule**: If a user requests a workflow, tree, table, or sequence diagram, proactively propose and use these high-level components.

**Related Rules**:
- SmartArts Components Detail: `uv run drawlib rules show smartarts`
- Domain Diagrams Detail: `uv run drawlib rules show diagrams`
- Charts & Visualizations Detail: `uv run drawlib rules show charts`

---

## 4. Visual Styles, Fonts & Media

- **Dynamic Configuration & Styles (`drawlib.config`)**:
  - `drawlib.config` manages runtime configuration, merging defaults with custom `--config` overlays.
  - **Rule (Config vs Preset Styles)**: If styles might be customized or themed via options (e.g. CLI `--config`), **always reference `styles` from `drawlib.config` (`from drawlib.config import styles`) rather than `drawlib.preset_styles`**. Because `config` is replaceable at runtime, using `config.styles` allows seamless theme switching and style patches across all diagrams without editing drawing code.
- **Preset Naming Pattern**: `<color>_<variant>` (`style=styles.blue_flat`, `style=styles.green_outline`, `style=styles.purple_flat`, `style=styles.bold`, `textstyle=styles.white_bold`).
- **Colors (`drawlib.colors`)**: Curated palettes (`ColorsDefault`, `ColorsMonochrome`, `ColorsEssentials`, `Colors140`) and helpers (`from_hex("#3498db", alpha=0.8)`, `with_alpha(color, 0.5)`).
- **Typography & Fonts (`drawlib.fonts`)**: Universal CJK+Latin `Font` (no glyph boxes), `FontRoboto` (weights), `FontMonoSpace` (code/logs), and `FontFile("brand.ttf")`.
- **Style Models & Types (`drawlib.types`)**: `Style` dataclass (`fill_color`, `line_width`, `text_size`, etc.). Use `style.copy()` for safe derivation. Subclass `BasePresetStyles` for custom themes.
- **Image Embedding (`drawlib.images`)**: `image((x, y), width=w, image="logo.png")` (auto aspect ratio). In-memory embedding via `canvas.get_dimage()` and `get_dimage_from_code()`.

**Related Rules**:
- Configuration & Dynamic Theming: `uv run drawlib rules show config`
- Preset Styles & Palettes Detail: `uv run drawlib rules show preset_styles`
- Colors & Hex Conversion: `uv run drawlib rules show colors`
- Typography & Fonts: `uv run drawlib rules show fonts`
- Style Models & Types: `uv run drawlib rules show types`
- Icons Library Detail: `uv run drawlib rules show icons`
- Images & Logos Embedding: `uv run drawlib rules show images`

---

## 5. Documentation as Code (`doc_builder` & `tools`)

Embed illustrations in standard Markdown files (`docs_src/*.md`):

````markdown
```drawlib fold-code 600px center caption:"System Architecture"
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.lines import line
from drawlib.shapes import rectangle

setup(width=120, height=50)
rectangle((30, 25), width=25, height=15, style=styles.blue_flat, text="Client")
rectangle((90, 25), width=25, height=15, style=styles.green_flat, text="API Gateway")
line((42.5, 25), (77.5, 25), arrowhead="->", style=styles.bold)
```
````

Compile via CLI without external tools (zero Sphinx / MkDocs):
```bash
uv run drawlib build html docs_src/ -o docs_html/      # Static HTML site
uv run drawlib build markdown docs_src/ -o docs/       # GitHub Markdown
uv run drawlib build pdf docs_src/index.md -o out.pdf  # Vector PDF
```

**Python Developer Tools API (`drawlib.tools`)**:
Execute compilation and diagram extraction directly from Python code, CI/CD, or test suites:
```python
from drawlib.tools import build_html, export_block
export_block("docs_src/arch.md", "1", "scratch/preview.png", grid=True)
build_html("docs_src/", "docs_html/", config_path="docs_config.py")
```

**Related Rules**:
- Documentation Site & Navbar Rules: `uv run drawlib rules show docs_build`
- Project Scaffolding & Build CLI: `uv run drawlib rules show cli`
- Python Developer Tools API: `uv run drawlib rules show tools`

---

## 6. On-Demand Detailed Rules Catalog

When you need complete function signatures and comprehensive code examples, run:

```bash
uv run drawlib rules show canvas        # Canvas config, sizing, coordinates, clear/save
uv run drawlib rules show shapes        # 22 shapes: circle, rectangle, wedge, chevron...
uv run drawlib rules show lines         # line, line_curved, lines, Bezier paths, arrowheads
uv run drawlib rules show text          # text alignment, fonts, formatting, text boxes
uv run drawlib rules show colors        # Colors, Colors140, palettes, hex conversion
uv run drawlib rules show fonts         # Font classes, weights, CJK/regional scripts, cache
uv run drawlib rules show images        # Embedding images, scaling, tinting, Dimage model
uv run drawlib rules show math          # get_angle, get_distance, get_center_and_size
uv run drawlib rules show types         # Style model, ColorsBase, FontBase, type conventions
uv run drawlib rules show smartarts     # Table, TreeNode, ChevronProcess, MindMap, Cycle
uv run drawlib rules show diagrams      # Architecture, Flow, Sequence, State, ER, Class
uv run drawlib rules show charts        # Bar, Line, Area, Pie, Radar, Scatter, Gantt
uv run drawlib rules show icons         # Phosphor, FontAwesome, and GCP architecture icons
uv run drawlib rules show preset_styles # Full style naming matrix and palette catalogs
uv run drawlib rules show config        # Dynamic config, custom theme overlays, CLI options
uv run drawlib rules show tools         # Python developer API: build, export, cache, template
uv run drawlib rules show cli           # build, export, show, init, serve, cache commands
uv run drawlib rules show docs_build    # multi-page docs structure, navbar.md rules
```
