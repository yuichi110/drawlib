---
trigger: always_on
---

# Drawlib AI Agent Instructions

Drawlib is a pure-Python library for **"Illustration as Code"** and **"Illustrated Documentation as Code"**.
AI coding agents must use Drawlib to create all architectural diagrams, workflows, and technical documentation.

---

## 1. Why Drawlib? (Illustration & Illustrated Documentation as Code)

Traditional technical documentation suffers from severe tool fragmentation:
- **The Fragmentation Problem**: Writing code in Git, drawing diagrams in external GUI tools (e.g. draw.io, Visio), exporting images, and manually pasting them into external documents (Word, Confluence, wikis). Diagrams quickly become outdated, inconsistent, and disconnected from the real codebase because maintenance requires tedious multi-tool handoffs.
- **The Drawlib Solution**: Unifies source code, documentation, and technical diagrams inside your Git repository as version-controlled code.
  - **Single Source of Truth (SoT)**: Markdown and declarative Python drawing blocks live alongside the codebase. Updating an architecture or database diagram is as painless and maintainable as editing code.
  - **Autonomous AI Feedback Loop**: AI coding agents can inspect repository code, generate diagrams, render them headlessly, review images multimodally, and iterate autonomously to continually elevate documentation quality.

---

## 2. Core Principles for AI Agents

1. **Draw with Drawlib (No Raw SVGs or Matplotlib Boilerplate)**:
   Never generate raw SVG files or complex low-level matplotlib boilerplate. Always use Drawlib's declarative Python API and high-level components.
2. **Scaffold Projects with `drawlib init` (Never from Scratch)**:
   Never manually construct documentation project folders or directory structures. Always use the built-in scaffolding CLI:
   - `uv run drawlib init site` (Multi-page documentation website with navigation sidebar)
   - `uv run drawlib init doc` (Linear technical document / spec / RFC)
   - `uv run drawlib init slide` (16:9 presentation slide deck)
   - `uv run drawlib init image` (Batch standalone drawing scripts)
3. **Start with Overview**:
   Before writing drawing code, inspect canvas geometry, coordinates, and lifecycle rules:
   `uv run drawlib rules show overview`
   *(Canvas origin (0,0) is at bottom-left; Cartesian coordinate system).*
4. **Follow the Style Guide**:
   Always obey design token discipline:
   `uv run drawlib rules show style-guide`
   - **50%+ Neutral Baseline**: Ground at least 50% of shapes in calm neutral cards (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`). Never produce rainbow diagrams.
   - **Reserved Saturated Fills**: Use `Styles.PrimaryFlat` or `Styles.AccentFlat` strictly for 1–2 primary focal points.
   - **PascalCase Tokens**: Always import `from drawlib.styles import Colors, Styles` (never lowercase `styles` or `colors`).

---

## 3. What Drawlib Can Do (Favor High-Level Components)

Never manually assemble diagrams out of dozens of primitive rectangles and lines. Always favor tailored high-level components:

| Category | Recommended Module | Primary Use Cases |
| :--- | :--- | :--- |
| **Auto-Layout Graphs** | `drawlib.graph` | Declarative auto-layout DAGs, nested clusters, topologies |
| **Cloud Architecture** | `drawlib.diagrams.architecture` | VPCs, microservices, cloud topologies, official icons |
| **Workflows & Pipelines** | `drawlib.diagrams.flow`, `smartarts.ChevronProcess` | Decision trees, CI/CD pipelines, linear stages |
| **API Sequences** | `drawlib.diagrams.sequence` | Client/server lifelines, message exchanges, sync/async calls |
| **Data & Relational Models**| `drawlib.diagrams.er`, `smartarts.Table` | Database schemas, entity relationships, matrix comparisons |
| **Code & State Models** | `drawlib.diagrams.class_diagram`, `diagrams.state` | OOP UML class models, state machine lifecycles |
| **Hierarchy & Organization**| `drawlib.smartarts.TreeNode`, `smartarts.MindMapNode` | Directory trees, org charts, radial brainstorming maps |
| **Quantitative Charts** | `drawlib.charts` | Bar, Line, Area, Pie, Radar, Scatter, and Gantt charts |
| **Standardized Icons** | `drawlib.icons` | Phosphor, FontAwesome, and GCP architecture vector/PNG icons |
| **Drawing Primitives** | `drawlib.shapes`, `lines`, `text` | 23 geometric primitives, curved lines, bezier curves, styled text |

---

## 4. Illustrated Documentation as Code (Embedded Markdown Blocks)

In technical documentation (`docs_src/`), embed diagrams directly within markdown files using the ````drawlib```` code fence:

````markdown
```drawlib 600px center file:service_architecture.png caption:"Service Architecture"
from drawlib.canvas import save, setup
from drawlib.styles import Styles
from drawlib.shapes import rectangle

setup(width=100, height=40)
rectangle((50, 20), width=60, height=20, style=Styles.Neutral, text="Service")
save()
```
````
- **Attributes**: Always specify `file:<name>.png` and `caption:"..."`. Never rely on auto-numbered filenames (`0.png`).
- **Source of Truth**: Always edit `<base>_src/` (e.g. `docs_src/`). Never manually edit generated output directories (`docs/`, `docs_html/`).

---

## 5. On-Demand Rules Catalog

Query specific detailed rule manuals as needed:

```bash
uv run drawlib rules show overview      # Geometry, coordinate space (0,0 at bottom-left), lifecycle
uv run drawlib rules show style-guide   # Color tokens, typography, 50%+ neutral rule
uv run drawlib rules show anim-guide    # Animation loop idioms and component animation patterns
uv run drawlib rules show slide-guide   # 16:9 slide authoring, ::: block/note syntax, stage layouts
uv run drawlib rules show project       # Project structures, navbar.md, build options
uv run drawlib rules show cli           # CLI commands (build, show, init, serve, cache)
uv run drawlib rules show api           # Complete API index & symbol cheat sheet
uv run drawlib rules show lib-<module>  # Module specifics (e.g. lib-shapes, lib-lines, lib-diagrams, lib-graph)
```
