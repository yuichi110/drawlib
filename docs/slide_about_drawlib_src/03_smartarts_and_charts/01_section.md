::: block (0, 0) (1920, 1080)
```drawlib file:divider.svg
import utils

utils.draw_chapter_divider(
    chapter_num=3,
    title="SmartArts & Quantitative Charts",
    subtitle="Structured Business Visuals & Vector Data Plotting on a Single Canvas",
    topics=[
        "10 Automated SmartArt Components with Unified Lifecycle",
        "Process Pipelines (ChevronProcess, Cycle, BoxList)",
        "Hierarchies, Matrices & Tables (TreeNode, MindMap, Grid, Pyramid)",
        "7 Statistical & Project Charts (Bar, Line, Area, Pie, Radar, Scatter, Gantt)",
    ],
)
```
:::

::: note
- Welcome to Chapter 3: **SmartArts & Quantitative Charts**.
- Up to this point, we explored Drawlib's foundational canvas, primitives, icons, and the 7-color semantic design system.
- While primitives give you pixel-exact freedom, assembling recurring patterns like process chevrons, circular PDCA loops, directory trees, tables, or statistical charts out of raw rectangles and lines is tedious and error-prone.
- In this chapter, we introduce two high-level modules that automate complex geometric math while staying 100% native to the Drawlib vector canvas:
  1. `drawlib.smartarts`: 10 structured business and technical visual components with a unified 4-phase lifecycle.
  2. `drawlib.charts`: 7 statistical, relational, and project timeline charts that coexist directly alongside architecture diagrams on the same coordinate plane.
:::
