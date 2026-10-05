# Chapter 8: SmartArts (Structured Infographics)

`drawlib.smartarts` automatically arranges structured visual infographics without requiring manual coordinate math for individual shapes.

## 8.1 Available SmartArt Components

- **`ChevronProcess`**: Sequential arrow blocks for deployment pipelines and development phases.
- **`Table`**: Structured comparison matrices with header styling and custom borders.
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

```drawlib 620px center file:fig_smartarts_sample.png caption:"Figure 8.1: Release Pipeline and Feature Comparison Matrix"
from drawlib.canvas import setup
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Styles

setup(width=110, height=65)

# 1. Pipeline Definition (ChevronProcess)
pipeline = ChevronProcess(
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold,
    description_style=Styles.Muted,
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.extend(
    texts=["1. Spec", "2. Develop", "3. Test", "4. Deploy"],
    styles=Styles.PrimaryFlat,
    descriptions=["Task triage", "AI pair-prog", "pytest verify", "CI delivery"],
)
pipeline.draw(xy=(8, 48), width=94, height=12)

# 2. Feature Matrix (Table)
table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark,
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold,
    border_style=Styles.MutedDashed,
)
table.draw(
    xy=(8, 42),
    width=94,
    height=34,
    data=[
        ["Category", "Primary Components", "Key Benefit"],
        ["SmartArts", "ChevronProcess, Table, MindMap", "No manual coordinate calculations"],
        ["Diagrams", "Architecture, Sequence, Flow", "Standardized system architecture"],
        ["Charts", "Gantt, Bar, Line, Pie", "Timeline and quantitative tracking"],
    ],
)
```
