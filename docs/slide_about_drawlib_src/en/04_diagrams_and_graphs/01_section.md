::: block xy=(0, 0) width=1920 height=1080
```drawlib file=divider.svg
import utils

utils.draw_chapter_divider(
    chapter_num=4,
    title="Domain Diagrams & Auto-Layout Graphs",
    subtitle="6 Purpose-Built Software Diagram Engines & 5 Declarative Graph Solvers",
    topics=[
        "Cloud & Microservice Topologies (ArchitectureDiagram)",
        "Workflows & API Lifelines (FlowDiagram, SequenceDiagram)",
        "Data & OOP Structural Models (ERDiagram, ClassDiagram, StateDiagram)",
        "Declarative Auto-Layout Engine (drawlib.graph: 5 Specialized Solvers)",
    ],
)
```
:::

::: note
- Welcome to Chapter 4: **Domain Diagrams & Auto-Layout Graphs**.
- Software architecture documentation requires standard formal notations: cloud network topologies, ISO 5807 swimlane flowcharts, chronological UML sequence lifelines, Crow's Foot database schemas, UML 2.0 class hierarchies, and finite state machines.
- In the first half of this chapter, we explore `drawlib.diagrams`—six purpose-built engines where you specify clean node coordinates while Drawlib handles boundary clipping, orthogonal Z-bends, row-level foreign key anchoring, and group bounding boxes.
- In the second half, we explore `drawlib.graph`—five pure coordinate layout solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, and `GridGraph`) that compute `GraphLayout` coordinates via `get_layout()` (`print(layout)` and `layout.offset()`) for seamless 2-step rendering with `drawlib.diagrams` and `drawlib.shapes`.
:::
