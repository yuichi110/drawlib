::: block (0, 0) (1920, 1080)
```drawlib file:divider.svg
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
- In the second half, we explore `drawlib.graph`—five declarative auto-layout solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, and `GridGraph`) that compute coordinates automatically while allowing post-calculation tweaks (`layout.offset()`) and standalone Python code export (`g.export_code()`).
:::
