---
trigger: always_on
---

# Drawlib AI Agent Instructions

Drawlib is a pure-Python library for **"Illustration as Code"** and **"Documentation as Code"**.
It enables AI coding agents and developers to generate clean, reproducible architectural diagrams, workflows, and technical visualizations using declarative Python code.

---

## 1. What Drawlib Can Do

Avoid manually writing SVGs or plotting with low-level matplotlib boilerplate. Drawlib provides tailored high-level components:

| Diagram Category | Recommended High-Level Module | What It Draws |
| :--- | :--- | :--- |
| **Cloud & Microservices** | `drawlib.diagrams.architecture.ArchitectureDiagram` | Cloud topologies, VPCs, clusters, icons |
| **Pipelines & Workflows** | `drawlib.smartarts.ChevronProcess`, `FlowDiagram` | Linear stages, decision gates, branching flows |
| **Hierarchy & Organization**| `drawlib.smartarts.tree`, `TreeNode` | Directory trees, org charts, taxonomy trees |
| **Radial Concepts & Maps** | `drawlib.smartarts.mindmap`, `MindMapNode` | Brainstorming nodes, radial feature maps |
| **Relational Data & Tables** | `drawlib.smartarts.Table` | Comparison matrix, schemas, data tables |
| **API Sequences & Protocols**| `drawlib.diagrams.sequence.SequenceDiagram` | Client/server lifelines, message flows, notes |
| **Quantitative Charts** | `drawlib.charts` (Bar, Line, Pie, Radar, Gantt) | Trend plots, project schedules, metrics |
| **Drawing Primitives** | `drawlib.shapes`, `drawlib.lines`, `drawlib.text` | 22 shapes, curved/bezier lines, styled text |
| **Standardized Icons** | `drawlib.icons` (Phosphor, FontAwesome, GCP) | Vector and official cloud architecture icons |

> **Rule**: When tasked with creating a diagram, always favor high-level components (`smartarts`, `diagrams`, `charts`) over assembling dozens of raw rectangles and lines by hand.

---

## 2. Autonomous AI Workflow & Feedback Loop

Always execute this self-correction loop when creating or modifying diagrams:

```text
1. Inspect Context ──> 2. Prototype in Scratch ──> 3. Render Image (-g) ──> 4. Multimodal Review
                                ▲                                                    │
                                └──────── 5. Issues Found? Fix & Retry ──────────────┘
                                                     │ (Pass)
                                                     ▼
                                             6. Present to User
```

1. **Inspect Context**: Check real repository files (`models.py`, API routes, configurations) so diagrams accurately reflect actual code.
2. **Prototype in Scratch**: Write drawing code in `scratch/test_diagram.py` or test a specific embedded block rather than modifying production assets blindly.
3. **Render Immediately with Coordinate Grid (`-g`)**:
   ```bash
   uv run drawlib show scratch/test_diagram.py -g -o scratch/test_diagram.png
   # Or for Markdown embedded block 1:
   uv run drawlib show docs_src/doc.md 1 -g -o scratch/test_diagram.png
   ```
4. **Multimodal Self-Review (`view_file`)**:
   Inspect `scratch/test_diagram.png` with your image viewing tool (`view_file`). Check for:
   - Text clipping or label overflow outside shapes.
   - Arrowhead misalignment or awkward line overlaps.
   - Missing perimeter margins (elements too close to canvas edges).
   - Poor color contrast (e.g. dark text on dark fill).
5. **Auto-Adjust & Iterate**: Fix coordinates and re-export until the layout is balanced and visually clear.
6. **Present to User**: Deliver clean code and verified illustrations.

---

## 3. Quickstart Example

```python
from drawlib.canvas import clear, save, setup
from drawlib.styles import Styles
from drawlib.lines import line
from drawlib.shapes import rectangle

setup(width=120, height=50)

# 1. Background / Boundary Container
rectangle((60, 25), width=108, height=38, style=Styles.muted_dashed)

# 2. Main Services
rectangle((30, 25), width=32, height=18, style=Styles.accent_flat, text="Client App", textstyle=Styles.white_bold)
rectangle((90, 25), width=32, height=18, style=Styles.primary_flat, text="API Gateway", textstyle=Styles.white_bold)

# 3. Connection
line((46, 25), (74, 25), arrowhead="->", style=Styles.bold)

save()
```

---

## 4. Documentation as Code

Drawlib unifies technical documentation and architectural illustrations as version-controlled code. Instead of managing static, out-of-sync PNGs or complex vector drawing tools, you embed declarative Python drawing blocks directly inside Markdown documents.

### 4.1. Embedded Code Blocks (`drawlib`)
Write diagrams inline within your Markdown documents using the ````drawlib```` code fence:

````markdown
# Service Architecture

The system communicates via asynchronous message queues:

```drawlib 600px center caption:"Event-Driven Microservices"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=100, height=40)
rectangle((25, 20), width=30, height=18, style=Styles.blue_flat, text="Publisher", textstyle=Styles.white_bold)
rectangle((75, 20), width=30, height=18, style=Styles.green_flat, text="Consumer", textstyle=Styles.white_bold)
line((40, 20), (60, 20), arrowhead="->", style=Styles.bold)
```
````

**Key Code Block Attributes**:
- **Code Display**: `hide-code` *(default)*, `show-code` (displays code above image), `fold-code` (collapsible `<details>` block).
- **Dimensions & Alignment**: `600px`, `100%`, `center` *(default)*, `left`, `right`.
- **Caption & Asset Name**: `caption:"Description"` (renders `<figcaption>`), `file:custom_name.png`.

### 4.2. Standard Project Scaffolding (`drawlib init`)
Never create documentation project structures manually. Always scaffold them with `drawlib init`:
- **`site`**: Multi-page documentation website (`docs_html/`) and GitHub-ready Markdown (`docs/`) with sidebar navigation (`navbar.md`).
- **`simple`**: Single-document technical spec / RFC (`docs_html/index.html` + `docs/index.rendered.md`).
- **`pdf`**: Multi-chapter formal technical reports and design documents (`docs.pdf`).
- **`image`**: Standalone Python drawing scripts generating image batches (`images_src/` -> `images/`).

### 4.3. Source of Truth & Build Pipeline
- **Source of Truth**: Always edit Markdown and drawing scripts inside `<base>_src/` (e.g. `docs_src/` or `images_src/`).
- **Never Edit Output Folders**: Output folders (`docs/`, `docs_html/`, `images/`) are generated artifacts overwritten on each build.
- **Build**: Run `./build.sh` (or `uv run drawlib build html docs_src/ -o docs_html/`).
- **Preview & Link Verification**: Run `uv run drawlib serve docs_html/` (or `--check` for headless validation).

> **Deep Dive**: For complete project structure rules, `navbar.md` navigation authoring, and compilation flags, run:  
> `uv run drawlib rules show project`

---

## 5. On-Demand Rules Catalog

Drawlib provides comprehensive, focused rule manuals that you can query via terminal on demand:

### General Guidelines
| Command | Topic | Primary Focus |
| :--- | :--- | :--- |
| `uv run drawlib rules show agent-instruction` | `agent-instruction` | This bootstrap manual (purpose, capabilities, workflow loop). |
| `uv run drawlib rules show overview` | `overview` | Canvas coordinate space `(0,0)` at bottom-left, Cartesian geometry, lifecycle (`setup`, `clear`, `save`). |
| `uv run drawlib rules show style-guide` | `style-guide` | 6-color semantic system, primary anchor, padding, grid alignment, typography hierarchy. |
| `uv run drawlib rules show project` | `project` | Project scaffolding (`init`), 4 template types (`site`, `simple`, `pdf`, `image`), `docs_src/`, `navbar.md`, builds. |
| `uv run drawlib rules show cli` | `cli` | Complete command line interface (`build`, `show`, `init`, `serve`, `cache`, `rules`). |

### Library Modules (`drawlib.*`)
| Command | Topic | Primary Focus |
| :--- | :--- | :--- |
| `uv run drawlib rules show lib-canvas` | `lib-canvas` | Canvas sizing, grid overlays, background transparency, in-memory Dimage. |
| `uv run drawlib rules show lib-shapes` | `lib-shapes` | 22 shape primitives (rectangles, circles, wedges, polygons, chevrons). |
| `uv run drawlib rules show lib-lines` | `lib-lines` | Straight, curved, bezier, chained lines, and arrowheads (`->`, `<->`, `-`). |
| `uv run drawlib rules show lib-text` | `lib-text` | Alignments (`halign`, `valign`), rotation, multiline text, font styles. |
| `uv run drawlib rules show lib-colors` | `lib-colors` | Color model, RGB/hex conversion, palettes (`DefaultColors`, `MonochromeColors`, `GoogleColors`). |
| `uv run drawlib rules show lib-styles` | `lib-styles` | Dynamic runtime theming, `styles.py`, `utils.py`, CLI injection flags. |
| `uv run drawlib rules show lib-preset-styles`| `lib-preset-styles` | Systematic naming matrix (`<color>_<variant>`), 6 semantic roles (4 for monochrome), 10 variants. |
| `uv run drawlib rules show lib-fonts` | `lib-fonts` | Universal CJK+Latin typography, regional scripts, custom font files. |
| `uv run drawlib rules show lib-images` | `lib-images` | Embedding images, scaling, tinting, `Dimage` transformations. |
| `uv run drawlib rules show lib-icons` | `lib-icons` | Phosphor, FontAwesome, and GCP architecture vector and PNG icons. |
| `uv run drawlib rules show lib-math` | `lib-math` | Angle (`get_angle`), distance (`get_distance`), bounding box (`get_center_and_size`). |
| `uv run drawlib rules show lib-types` | `lib-types` | `Style` dataclass, `BaseStyles`, type aliases and validation. |
| `uv run drawlib rules show lib-smartarts` | `lib-smartarts` | Tables, tree hierarchies, mindmaps, cycle loops, process chevrons. |
| `uv run drawlib rules show lib-charts` | `lib-charts` | Bar, Line, Area, Pie, Radar, Scatter, and Gantt charts. |
| `uv run drawlib rules show lib-diagrams` | `lib-diagrams` | Architecture, Flow, Sequence, State, Class, and ER diagrams. |
| `uv run drawlib rules show lib-tools` | `lib-tools` | Programmatic Python API for compilation, diagram export, and CI/CD. |

Run `uv run drawlib rules list` at any time to inspect all available rule topics and cache status.
