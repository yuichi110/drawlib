# Release Notes & Migration Guide

## Version 0.3.0

*Release Date: 2026/09/21*

Version 0.3.0 represents a major architectural milestone for Drawlib, transforming it from a raw vector drawing tool into a comprehensive **"Illustration & Documentation as Code"** platform engineered for both software developers and **autonomous AI coding agents**.

---

### Highlights & New Features

#### 1. Modern Flat Package Architecture
- Consolidated legacy version-namespaced packages into a modern, standard flat package structure (`drawlib`).
- Clean, ergonomic public imports directly from domain modules:
  - `drawlib.canvas`
  - `drawlib.shapes`, `drawlib.lines`, `drawlib.text`
  - `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`
  - `drawlib.styles`, `drawlib.preset_colors`, `drawlib.preset_styles`

#### 2. Built-in Integrated Documentation Builder
- Native Markdown and HTML compiler (`drawlib build html`, `drawlib build markdown`, `drawlib build pdf`).
- Compiles Markdown documents containing ````drawlib```` code blocks into:
  - Responsive multi-page static HTML documentation sites (`docs_html/`).
  - GitHub-optimized Markdown documents with embedded images (`docs/`).
  - Print-ready vector PDF documents (`docs.pdf`).
- Intelligent content-hash caching prevents unnecessary re-rendering of unchanged diagrams.

#### 3. High-Level Technical Diagrams (`drawlib.diagrams`)
- **ER Diagrams (`drawlib.diagrams.er.ERDiagram`)**: Full support for Information Engineering (IE / Crow's Foot) notation, table entity compartments, and automatic orthogonal routing.
- **UML Class Diagrams (`drawlib.diagrams.class_diagram.ClassDiagram`)**: 3-compartment class cards, stereotypes (`«interface»`), visibility indicators, and relationship methods (`inherit()`, `realize()`, `composite()`, `aggregate()`, `associate()`, `depend()`).
- **State Machine Diagrams (`drawlib.diagrams.state_diagram.StateDiagram`)**: Declarative statecharts with initial/final pseudo-states, internal activity compartments (`entry`, `do`, `exit`), curved transitions with bend control, and self-loops.
- **Flow Diagrams (`drawlib.diagrams.flow.FlowDiagram`)**: Standard flowchart symbols (ISO 5807 / JIS X 0121), decision branching, T-junction merging, and swimlanes (`Lane`).
- **Architecture Diagrams (`drawlib.diagrams.architecture.ArchitectureDiagram`)**: Cloud topologies, cluster groups, Phosphor and official GCP vector icons.

#### 4. Pure-Python Declarative Charts (`drawlib.charts`)
- Zero external plotting dependencies:
  - **BarChart**: Vertical/horizontal, grouped, and stacked.
  - **LineChart**: Straight segments, smoothed spline curves, and custom markers.
  - **AreaChart**: Overlapping and cumulative stacked area plots.
  - **PieChart**: Solid pies and donut rings with center KPI badges.
  - **RadarChart**: Multiaxis spider webs and concentric circular rings.
  - **ScatterChart**: 2D scatter and bubble plots with custom marker shapes.
  - **GanttChart**: Project schedules, progress bars, milestones, and task dependency arrows.

#### 5. New SmartArts (`drawlib.smartarts`)
- **`ChevronProcess`**: Sequential chevron process pipelines with descriptions, configurable angles, and flat starts.
- **`Cycle`**: Circular loops (PDCA, life cycles, radial cycles with center topics).

#### 6. AI Agent Guidelines & Rule System (`drawlib rules`)
- Integrated on-demand manual accessible via CLI:
  - `drawlib rules show <topic>`: Inject concise syntax documentation directly into agent context windows.
  - `drawlib rules list`: Explore all available drawing rules.
- Autonomous visual self-correction loop via coordinate grid overlay (`drawlib show -g`).

#### 7. Project Scaffolding (`drawlib init`)
- Quickly scaffold complete starter projects for four primary use cases:
  - `drawlib init site`: Multi-page documentation website.
  - `drawlib init simple`: Single specification / RFC document.
  - `drawlib init pdf`: Formal technical PDF report.
  - `drawlib init image`: Standalone Python illustration batch project.

---

### Breaking Changes & Migration from v0.2

If you are upgrading from Drawlib v0.2, review the following required changes:

1. **Python 3.11+ Required**: Python 3.10 and earlier are no longer supported.
2. **Top-Level CLI `drawlib export` Removed**:
   - Use `drawlib show input.py -o output.png` instead.
3. **Legacy `dsart` Namespace Removed**:
   - Change `from drawlib.apis import dsart` to:
     ```python
     from drawlib.smartarts import Table, Tree, ChevronProcess, Cycle
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
