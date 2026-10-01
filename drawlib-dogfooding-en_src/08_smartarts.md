# Chapter 8: SmartArts (Structured Infographics)

`drawlib.smartarts` automatically arranges structured visual infographics without requiring manual coordinate math for individual shapes.

## 8.1 Available SmartArt Components

- **`ChevronProcess`**: Sequential arrow blocks for deployment pipelines and development phases.
- **`Table`**: Structured comparison matrices with header styling and custom borders.
- **`MindMapNode`**: Radial and branching idea maps.
- **`TreeNode`**: Hierarchical organization charts and directory trees.
- **`bubblespeech`**: Pointed callouts and annotations.

## 8.2 Release Pipeline and Feature Matrix Example

```drawlib 620px center file:fig_smartarts_sample.png caption:"Figure 8.1: Release Pipeline and Feature Comparison Matrix"
from drawlib.canvas import setup
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Styles

setup(width=110, height=65)

# 1. Pipeline Definition (ChevronProcess)
pipeline = ChevronProcess(
    default_style=Styles.PrimaryFlat,
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
    default_textstyle=Styles.WhiteBold,
    default_description_style=Styles.Muted,
)
pipeline.extend(
    texts=["1. Spec", "2. Develop", "3. Test", "4. Deploy"],
    descriptions=["Task triage", "AI pair-prog", "pytest verify", "CI delivery"],
)
pipeline.draw(xy=(8, 48), width=94, height=12)

# 2. Feature Matrix (Table)
table = Table(
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold,
    default_text_style=Styles.Primary,
    border_style=Styles.MutedLight,
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
