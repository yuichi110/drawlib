::: block xy=(0, 0) width=1920 height=1080
```drawlib file=ch4_divider.svg
import utils

utils.draw_chapter_divider(
    4,
    "Diagrams, Graphs & Animations",
    subtitle="6 Engineering Diagram Engines, 5 Solvers & APNG",
    topics=[
        "Cloud Topology (ArchitectureDiagram)",
        "Flowcharts & API Sequence Diagrams",
        "UML Class, ER & State Machines",
        "Auto-Layout Graphs & Animations",
    ],
    total_chapters=6,
)
```
:::

::: note
**Chapter 4 Overview — Engineering Diagrams, Auto-Layout Graphs & Animations**:
- In Chapter 3 we explored SmartArts and statistical Charts for executive storytelling and data visualization. Chapter 4 moves into **deep software and systems engineering**.
- First, we cover Drawlib's **6 purpose-built diagram engines** (`drawlib.diagrams`): `ArchitectureDiagram` for multi-tier cloud topologies, `FlowDiagram` and `SequenceDiagram` for workflows and API protocols, and `ClassDiagram`, `ERDiagram`, and `StateDiagram` for domain modeling.
- Next, we examine **`drawlib.graph`**, Drawlib's pure-Python coordinate solver suite (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, and `GridGraph`) that eliminates manual `(x, y)` math while preserving manual fine-tuning via `offset()`.
- Finally, we demonstrate **`drawlib.anim`**, bringing declarative frame-based APNG and Animated WebP motion to every module in Drawlib with interactive presentation playback and automatic PDF/PPTX frame extraction.
:::
