# Release Notes



# Version 0.3.0

## Release date: 2026/09/21

## New features

- **Modern Flat Package Architecture**:
  - Refactored library layout from legacy version-namespaced structure to standard flat package (`drawlib`).
  - Unified public interface via `drawlib.apis` facade.
- **Built-in Document Builder**:
  - Added native Markdown / HTML document compiler (`drawlib doc-builder` and `build_document()`).
  - Automatically compiles markdown with `drawlib` code blocks into responsive HTML, rendered Markdown, or PDF.
- **ER Diagrams (`drawlib.diagrams.er`)**:
  - Declarative Entity-Relationship diagrams with full support for IE (Crow's Foot) notation.
  - Automatic right-angled orthogonal routing, column-level anchoring, and custom styling.
- **UML Class Diagrams (`drawlib.diagrams.class_diagram`)**:
  - Declarative UML Class diagramming with 3-compartment class cards, stereotypes (`«interface»`), abstract classes, and typed attributes/methods.
  - Intuitive verb-based connection methods: `inherit()`, `realize()`, `composite()`, `aggregate()`, `associate()`, `depend()`.
  - Full UML 2.0 marker support: hollow generalization triangles, solid/hollow aggregation diamonds, open dependency arrows, multiplicities, role names, and boundary-clipped routing.
- **State Diagrams (`drawlib.diagrams.state_diagram`)**:
  - Declarative Statechart and Finite State Machine (FSM) diagramming module.
  - Support for 5 node shapes (`"box"`, `"oval"`, `"circle"`, `"double_circle"`, `"text_only"`), internal activity compartments (`entry`, `do`, `exit`), and pseudo-states (`InitialState`, `FinalState`, `ChoiceState`, `ForkJoinState`).
  - Native curved arc transitions (`line_curved`) with `bend` control, automatic self-transition loops (`A ↺ A`), bidirectional pairs (`A ⇄ B`), and formal label formatting (`event [guard] / action`).
- **Flow Diagrams (`drawlib.diagrams.flow`)**:
  - Declarative flowchart and workflow diagramming module adhering to standard flowchart symbols (ISO 5807 / JIS X 0121).
  - Shape-centric nodes (`Process`, `Decision`, `Start`, `End`, `Data`) inheriting Drawlib shape styling.
  - First-class T-junction branching/merging (`Junction`) and flat global coordinate swimlanes (`Lane`).
- **SmartArts (`drawlib.smartarts`)**:
  - Added `ChevronProcess`: Sequential chevron (arrowhead block) process pipelines with supporting descriptions, customizable arrowhead angles, auto-palette theming, and flat-start options.
  - Added `Cycle`: Circular and cyclical process diagrams (PDCA, life cycles, radial cycles with center topic, circular arc arrows, and circle/rectangle node shapes).
- **Charts Module (`drawlib.charts`)**:
  - Pure-Python declarative charting engine without external visualization dependencies.
  - Features `BarChart` (vertical/horizontal, grouped/stacked), `LineChart` (straight/smooth curves, custom markers), `AreaChart` (overlapping and cumulative stacked areas), `PieChart` (solid pie, donut rings with center KPI badges, exploded slices), `RadarChart` (spider webs, concentric circular rings), `ScatterChart` (2D scatter and bubble plots, custom markers, individual and series points), and `GanttChart` (project roadmaps, progress bars, sections, milestones, dependency arrows).
  - First-class support for logarithmic scales, fully customizable ticks/gridlines, and automatic legend layout.
- **Headless PDF Export**:
  - PDF generation uses existing system Chromium-based browsers (Chrome, Chromium, Edge) without requiring Playwright.
- **On-Demand Release Assets**:
  - Assets such as icon sets and fonts are downloaded dynamically from GitHub Releases (`v0.3`), significantly reducing the PyPI package footprint.
- **Unified Developer CLI (`dcli`)**:
  - Integrated CLI tooling for linting (`ruff`), type checking (`ty`), asset management, and documentation builds.
- **Single Block Image Export & CLI Preview Enhancements**:
  - Added `drawlib export` CLI command for extracting and rendering a single illustration from Python scripts or Markdown files directly to an image file.
  - Full support for `--config` (`-c`) to apply custom document themes and settings, `--output` (`-o`) for explicit destination path, and `--grid` (`-g`) for coordinate overlay.
  - Added `-o` / `--output` support to `drawlib show` for headless environments and automated scripts, suppressing GUI display when output path is specified.

## Requirements & Breaking changes

- Python >= 3.11 is now required.
- Package modules are directly accessible (e.g. `drawlib.canvas`, `drawlib.shapes`, `drawlib.smartarts`).
- The legacy `dsart` facade is removed in favor of direct imports from `drawlib.smartarts` (e.g., `from drawlib.smartarts import Table, SourceCode, bubblespeech`).
- In `drawlib.diagrams`, diagram classes are uniformly named:
  - `drawlib.diagrams.architecture.ArchitectureDiagram`
  - `drawlib.diagrams.er.ERDiagram`
  - `drawlib.diagrams.flow.FlowDiagram`
  - `drawlib.diagrams.sequence.SequenceDiagram`
  - These can now also be imported directly from `drawlib.diagrams` (e.g., `from drawlib.diagrams import ArchitectureDiagram, ERDiagram, FlowDiagram, SequenceDiagram`).



# Version 0.2.3



## Release data: 2024/09/08



## Commit: `4cc6e6e <https://github.com/yuichi110/drawlib/commit/4cc6e6ef2a72baeaf7e5405988d20f551e2eae3a>`_



## New features


Adding shape arrow functions.

- `arrow_polyline()`
- `arrow_l()`
- `arrow_u()`
- `arrow_arc()`

Adding smart arts.

- `dsart.BoxList`
- `dsart.BulletPoints`
- `dsart.GridLayout`
- `dsart.Pyramid`
- `dsart.Table`
- `dsart.Tree`

Adding style model attribute.

- `ShapeTextStyle.xy_abs_shift`



## Breaking changes


Change arg names 

- From `from_angle` to `angle_start`
- From `to_angle` to `angle_end`

At these functions.

- `arc()`
- `fan()`
- `wedge()`

Change arg names at function `dsart.bubblespeech()`.

- From `tail_from_ratio` to `tail_start_ratio`
- From `tail_to_ratio` to `tail_end_ratio`


# 0.2.2



## Release data: 2024/07/02



## Commit: `fa1d90a <https://github.com/yuichi110/drawlib/commit/fa1d90a4a45fb3edab2cbafddfa04ef23d6a5691>`_


First release of Drawlib `0.2`.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
