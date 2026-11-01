# Chapter 8: SmartArts (Structured Infographics)

`drawlib.smartarts` automatically arranges structured visual infographics without requiring manual coordinate math for individual shapes. SmartArt components position their bounding box using the **bottom-left coordinate `(x0, y0)`** in `.draw(xy=...)` (`Table` supports `align="bottom_left"` or the default `align="top_left"`).

## 8.1 Available SmartArt Components

- **`ChevronProcess`**: Sequential arrow blocks for deployment pipelines and development phases.
- **`Table`**: Structured comparison matrices with header styling and custom borders.
- **`GeoMap`**: Offline vector maps for the world, regions, and Japan prefectures with country/prefecture highlights, pin markers, and inter-site connection arcs.
- **`MindMapNode`**: Radial and branching idea maps.
- **`TreeNode`**: Hierarchical organization charts and directory trees.
- **`Cycle`**: Continuous feedback loops and lifecycle workflows.
- **`Pyramid`**: Testing pyramids, security tier models, and priority hierarchies.
- **`BoxList` / `BulletPoints`**: Organized card stacks and bulleted summaries.
- **`GridLayout`**: Matrix-based dashboard layouts.
- **`SourceCode`**: Syntax-highlighted code blocks with line numbering.

> [!NOTE]
> For pointing speech bubbles and callout annotations, use `bubblespeech` from `drawlib.shapes`.

## 8.2 Release Pipeline and Feature Matrix Example

```drawlib align=center file=fig_smartarts_sample.png caption="Figure 8.1: Release Pipeline and Feature Comparison Matrix"
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Styles

setup(width=110, height=65)

# 1. Pipeline Definition (ChevronProcess: PrimaryNeutral baseline + PrimaryFlat focal step)
pipeline = ChevronProcess(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.add("1. Spec", description="Task triage")
pipeline.add(
    "2. Develop",
    description="AI pair-prog",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=9.5),
)
pipeline.add("3. Test", description="pytest verify")
pipeline.add("4. Deploy", description="CI delivery")
pipeline.draw(xy=(6, 46), width=98, height=14)

# 2. Feature Matrix (Table)
table = Table(
    cell_style=Styles.Neutral,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.Muted,
)
table.draw(
    xy=(6, 6),
    width=98,
    height=35,
    align="bottom_left",
    data=[
        ["Category", "Primary Components", "Key Benefit"],
        ["SmartArts", "ChevronProcess, Table, GeoMap", "No manual coordinate calculations"],
        ["Diagrams", "Architecture, Sequence, Flow", "Standardized system architecture"],
        ["Charts", "Gantt, Bar, Line, Pie, Scatter", "Timeline and quantitative tracking"],
    ],
)

save()
```
