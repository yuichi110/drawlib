# Release Notes & Migration Guide

## Version 0.3.0

*Release Date: 2026/09/21*

Version 0.3.0 represents a major architectural milestone for Drawlib, transforming it from a raw vector drawing tool into a comprehensive **"Illustration & Documentation as Code"** platform engineered for both software developers and **autonomous AI coding agents**.

---

### Highlights & New Features

#### 1. Modern Flat Package Architecture
- Consolidated legacy version-namespaced packages into a modern, standard flat package structure (`drawlib`).
- Clean, ergonomic public imports directly from domain modules:
  - `drawlib.canvas`, `drawlib.math`, `drawlib.types`, `drawlib.fonts`
  - `drawlib.shapes`, `drawlib.lines`, `drawlib.text`, `drawlib.icons`, `drawlib.images`
  - `drawlib.graph`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`
  - `drawlib.anim`, `drawlib.slide`, `drawlib.tools`
  - `drawlib.styles`, `drawlib.preset_colors`, `drawlib.preset_styles`, `drawlib.utils`

#### 2. Built-in Integrated Documentation Builder, Slide Compiler & Developer Tools (`drawlib.tools`)
- Native Markdown, HTML, Slide, and PDF compiler (`drawlib build html`, `drawlib build markdown`, `drawlib build pdf`, `drawlib build slide`, `drawlib build image`).
- Compiles Markdown documents containing ````drawlib```` code blocks into:
  - Responsive multi-page static HTML documentation sites (`docs_html/`).
  - GitHub-optimized Markdown documents with embedded images (`docs/`).
  - Print-ready vector PDF documents (`doc.pdf` / `slide.pdf`).
  - Interactive 16:9 widescreen HTML presentation decks (`slide_html/`).
- **SQLite Incremental Build Cache (`.drawlib/cache.db`)**: Deterministic SHA-256 content-hash caching of code blocks, `styles.py`, `utils.py`, and local assets prevents unnecessary re-rendering of unchanged diagrams.
- **Programmatic Developer API (`drawlib.tools`)**: Full Python API (`build_html`, `build_markdown`, `build_pdf`, `build_slide`, `build_image`, `export_code_block`, `init_project`, `serve_docs`, `list_cache`, `download_cache`, `clear_cache`) for CI/CD and custom automation.

#### 3. Auto-Layout Graph Engine (`drawlib.graph`)
- Five specialized auto-layout graph solvers that eliminate manual coordinate math and support nested `Cluster` containers:
  - **`LayerGraph`**: Sugiyama-style hierarchical DAG layout.
  - **`ArchitectureGraph`**: Cloud and system topology solver with semantic tier alignment.
  - **`TreeGraph`**: Balanced parent-child hierarchy layout.
  - **`RadialGraph`**: Concentric radial ring layout.
  - **`GridGraph`**: Structured matrix placement solver.
- **Code Export (`export_code()`)**: Automatically emits clean, editable Drawlib primitive Python code from computed graph layouts for fine-grained customization.

#### 4. High-Level Technical Diagrams (`drawlib.diagrams`)
- **Architecture Diagrams (`drawlib.diagrams.architecture.ArchitectureDiagram`)**: Cloud topologies, nested cluster groups, and Phosphor / official GCP vector icons.
- **Flow Diagrams (`drawlib.diagrams.flow.FlowDiagram`)**: Standard flowchart symbols (ISO 5807 / JIS X 0121), decision branching, T-junction merging, and swimlanes (`Lane`).
- **Sequence Diagrams (`drawlib.diagrams.sequence.SequenceDiagram`)**: Client/server lifelines, activation bars, sync/async message arrows, self-calls, and interaction frames (`alt`, `opt`, `loop`, `par`).
- **ER Diagrams (`drawlib.diagrams.er.ERDiagram`)**: Full support for Information Engineering (IE / Crow's Foot) notation, table entity compartments, and automatic orthogonal routing.
- **UML Class Diagrams (`drawlib.diagrams.class_diagram.ClassDiagram`)**: 3-compartment class cards, stereotypes (`«interface»`), visibility indicators, and relationship methods (`inherit()`, `realize()`, `composite()`, `aggregate()`, `associate()`, `depend()`).
- **State Machine Diagrams (`drawlib.diagrams.state.StateDiagram`)**: Declarative statecharts with initial/final pseudo-states, internal activity compartments (`entry`, `do`, `exit`), curved transitions with bend control, and self-loops.

#### 5. Pure-Python Declarative Charts (`drawlib.charts`)
- Zero external plotting dependencies:
  - **BarChart**: Vertical/horizontal, grouped, and stacked.
  - **LineChart**: Straight segments, smoothed spline curves, and custom markers.
  - **AreaChart**: Overlapping and cumulative stacked area plots.
  - **PieChart**: Solid pies and donut rings with center KPI badges.
  - **RadarChart**: Multiaxis spider webs and concentric circular rings.
  - **ScatterChart**: 2D scatter and bubble plots with custom marker shapes.
  - **GanttChart**: Project schedules, progress bars, milestones, and task dependency arrows.

#### 6. Expanded SmartArts & Geographic Maps (`drawlib.smartarts`)
- **`GeoMap`**: Offline vector world, regional, and country maps (`World`, `Asia`, `Europe`, `USA`, `Japan`, etc.) with country/prefecture highlighting, pins, connections, and choropleth coloring.
- **`TreeNode`** & **`MindMapNode`**: Hierarchical node trees and radial brainstorming mind maps.
- **`SourceCode`**: Syntax-highlighted source code cards with line numbers, window chrome, and dark/light themes.
- **`ChevronProcess`** & **`Cycle`**: Sequential chevron process pipelines and radial circular life cycles with center hubs.
- **`Table`**, **`GridLayout`**, **`Pyramid`**, **`BoxList`**, **`BulletPoints`**: Structured tabular and card-based visual components.

#### 7. Multi-Frame Animations (`drawlib.anim`) & 16:9 Presentation Stage (`drawlib.slide`)
- **`drawlib.anim.Animation`**: Declarative multi-frame animation builder exporting lossless **APNG** and **Animated WebP** with frame context managers (`with anim.frame():`), configurable FPS, and interpolation helpers in `drawlib.math`.
- **`drawlib.slide`**: Universal `1920x1080` (16:9 widescreen) presentation coordinate stage with Markdown layout containers (`::: block`, `::: note`), Presenter View (`?presenter=1`), and the `current_slide` runtime proxy (`SlideContext`, `BoundingBox`).

#### 8. AI Agent Guidelines & Rule System (`drawlib rules`)
- Integrated on-demand manual accessible via CLI:
  - `drawlib rules show <topic>`: Inject concise syntax documentation directly into agent context windows.
  - `drawlib rules list`: Explore all available drawing rules.
- Autonomous visual self-correction loop via coordinate grid overlay (`drawlib show -g`).

#### 9. Project Scaffolding (`drawlib init`)
- Quickly scaffold complete starter projects for four primary use cases:
  - `drawlib init doc`: Linear technical document (HTML, PDF, Markdown, images).
  - `drawlib init site`: Multi-page documentation website.
  - `drawlib init slide`: 16:9 presentation slide deck (web & vector PDF).
  - `drawlib init images`: Standalone Python illustration batch project.

---

### Breaking Changes & Migration from v0.2

If you are upgrading from Drawlib v0.2, review the following required changes:

1. **Python 3.11+ Required**: Python 3.10 and earlier are no longer supported.
2. **Top-Level CLI `drawlib export` Removed**:
   - Use `drawlib show input.py -o output.png` instead.
3. **Legacy `dsart` Namespace Removed & `Tree` Renamed to `TreeNode`**:
   - Change `from drawlib.apis import dsart` to:
     ```python
     from drawlib.smartarts import Table, TreeNode, MindMapNode, ChevronProcess, Cycle, GeoMap, SourceCode
     ```
4. **Semantic Style Naming Normalized**:
   - Styles tokens unified to PascalCase (`Styles.PrimaryFlat`, `Styles.AccentBold`). Legacy snake-case style attributes are completely removed.
5. **Diagram Class Naming Unified**:
   - All diagram containers follow PascalCase with the `Diagram` suffix:
     - `ArchitectureDiagram`
     - `ERDiagram`
     - `FlowDiagram`
     - `SequenceDiagram`
     - `ClassDiagram`
     - `StateDiagram`

---

## Version 0.2.x Archive

- **v0.2.3** (2024/09/08): Added block arrow functions (`arrow_polyline`, `arrow_l`, `arrow_u`, `arrow_arc`) and initial SmartArts (`Table`, `Tree`, `GridLayout`, `Pyramid`, `BoxList`, `BulletPoints`).
- **v0.2.2** (2024/07/02): Initial public release of Drawlib 0.2.
