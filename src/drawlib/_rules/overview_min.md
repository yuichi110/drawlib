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

1. **Inspect Context**: Check real repository files (`models.py`, API routes, config) to ground the diagram in actual code.
2. **Prototype in Scratch Directory**: Write temporary code in `scratch/test_diagram.py` instead of directly modifying production files.
3. **Render Immediately with Coordinate Grid (`-g`)**:
   ```bash
   uv run drawlib export scratch/test_diagram.py -g -o scratch/test_diagram.png
   # Or for Markdown embedded block 1:
   uv run drawlib export docs_src/doc.md 1 -g -o scratch/test_diagram.png
   ```
4. **Multimodal Self-Review (`view_file`)**: Inspect `scratch/test_diagram.png`. Check for overlaps, text clipping, bad arrow routing, or uneven whitespace.
5. **Auto-Adjust & Iterate**: Fix coordinates and re-export until the layout is balanced.
6. **Show Rendered Image to User**: Present the image to the user for quick visual sign-off before committing.

**Related Rules**:
- CLI & Fast Verification: `uv run drawlib rules show cli`

---

## 2. Core Concepts: Canvas & Geometry

- **Origin `(0, 0)`**: Strictly at the **bottom-left corner**. X increases to the right; Y increases upward.
- **Default Center Anchor**: Shape and text coordinates `(x, y)` define the geometric **center** by default.
- **Canvas Sizing Heuristics**:
  - Small component / badge: `config(width=80, height=40)`
  - Standard architecture / flowchart / sequence: `config(width=140, height=70)`
  - Widescreen 16:9 system overview: `config(width=160, height=90)`
- **Multi-Image Scripts**: Always call `clear()` between sequential images to avoid canvas bleeding.

```python
from drawlib.canvas import clear, config, save
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=120, height=50)
rectangle((30, 25), width=28, height=16, style="blue_flat", text="Service A", textstyle="white_bold")
rectangle((90, 25), width=28, height=16, style="green_flat", text="Service B", textstyle="white_bold")
line((44, 25), (76, 25), arrowhead="->", style="bold")
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

## 4. Visual Styles & Palettes

- **Preset Naming Pattern**: `<color>_<variant>`
  - Variants: `flat`, `outline`, `soft`, `bold`, `light`
  - Examples: `style="blue_flat"`, `style="green_outline"`, `style="purple_flat"`
  - Text Styles: `textstyle="white_bold"`, `textstyle="bold"`
- **Line Styles**: `style="bold"`, `style="light"`, `style="dashed"`, `arrowhead="->"` (`<-`, `<->`, `-`)
- **Avoid Magic Hex Codes**: Use preset style strings or official palette objects (`ColorsDefault`, `ColorsMonochrome`, `ColorsEssentials`) for aesthetic consistency.

**Related Rules**:
- Preset Styles & Palettes Detail: `uv run drawlib rules show preset_styles`
- Colors & Hex Conversion: `uv run drawlib rules show colors`
- Typography & Fonts: `uv run drawlib rules show fonts`
- Style Models & Types: `uv run drawlib rules show types`
- Icons Library Detail: `uv run drawlib rules show icons`
- Images & Logos Embedding: `uv run drawlib rules show images`

---

## 5. Documentation as Code (`doc_builder`)

Embed illustrations in standard Markdown files (`docs_src/*.md`):

````markdown
```drawlib fold-code 600px center caption:"System Architecture"
config(width=120, height=50)
rectangle((30, 25), width=25, height=15, style="blue_flat", text="Client")
rectangle((90, 25), width=25, height=15, style="green_flat", text="API Gateway")
line((42.5, 25), (77.5, 25), arrowhead="->", style="bold")
```
````

Compile without external tools (zero Sphinx / MkDocs):
```bash
# Responsive HTML site:
uv run drawlib build html docs_src/ -o docs_html/

# GitHub-optimized Markdown:
uv run drawlib build markdown docs_src/ -o docs/

# Print-ready vector PDF:
uv run drawlib build pdf docs_src/index.md -o output.pdf
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
uv run drawlib rules show tools         # Python developer API: build, export, cache, template
uv run drawlib rules show cli           # build, export, show, init, serve, cache commands
uv run drawlib rules show docs_build    # multi-page docs structure, navbar.md rules
```
