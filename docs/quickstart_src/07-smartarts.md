# 7. SmartArts: High-Level Visual Components

`drawlib.smartarts` provides presentation-ready visual layouts inspired by enterprise presentation tools. Instead of assembling dozens of individual shapes and calculating complex offsets by hand, SmartArt components encapsulate layout geometry and item spacing.

## Available SmartArt Components

| Component | Anchor Point | Typical Use Case |
| :--- | :--- | :--- |
| **`ChevronProcess`** | Bottom-Left `(x, y)` | Linear stages, CI/CD delivery pipelines, sequential workflows |
| **`Table`** | Top-Left `(x, y)` | Service matrices, SLA comparison tables, schema summaries |
| **`TreeNode`** | Top-Left `(x, y)` | Directory trees, organization charts, package hierarchies |
| **`MindMapNode`** | Center `(x, y)` | Brainstorming nodes, radial feature maps, architectural taxonomy |
| **`Cycle`** | Center `(x, y)` | Feedback loops, continuous monitoring lifecycles, SRE runbooks |
| **`Pyramid`** | Bottom-Left `(x, y)` | Testing pyramids, security tier models, priority hierarchies |
| **`BoxList`** | Top-Left `(x, y)` | Feature checklists, component listings, vertical card stacks |
| **`BulletPoints`** | Top-Left `(x, y)` | Bulleted textual summaries, key takeaways, architectural principles |
| **`GridLayout`** | Bottom-Left `(x, y)` | Uniform grid arrangements, dashboard widgets, matrix cells |
| **`SourceCode`** | Top-Left `(x, y)` | Syntax-highlighted code blocks with line numbering |

> [!NOTE]
> For pointing speech bubbles and callout annotations, use `bubblespeech` from `drawlib.shapes`.

## Linear Workflow: `ChevronProcess`

`ChevronProcess` creates connected pipeline chevrons with automatic text and description formatting:

```drawlib 640px center file:smartarts_cicd.png caption:"Figure 7.1: Automated CI/CD Pipeline via ChevronProcess"
from drawlib.canvas import setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=120, height=36)

pipeline = ChevronProcess(
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10),
    description_style=Styles.White.patch(text_size=8),
    corner_angle=60.0,
    spacing=1.8,
    flat_left_end=True,
)

pipeline.add("1. Commit", description="Git Push", style=Styles.PrimaryFlat)
pipeline.add("2. Test", description="pytest / linter", style=Styles.SecondaryFlat)
pipeline.add("3. Build", description="Docker Container", style=Styles.AccentFlat)
pipeline.add("4. Deploy", description="Cloud Run (Prod)", style=Styles.SuccessFlat)

pipeline.draw(xy=(10, 8), width=100, height=20)
```

## Relational Tables: `Table`

The `Table` component draws structured tabular data with configurable headers, alternating row colors, and border separators:

```drawlib 640px center file:smartarts_sla_table.png caption:"Figure 7.2: Microservice SLA & Metric Table"
from drawlib.canvas import setup
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

setup(width=120, height=52)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Primary.patch(text_size=9),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=9.5),
    border_style=Styles.MutedThin,
)

table.set_style_cell_evenodd(
    even_color=Colors.White,
    even_text_style=Styles.Primary.patch(text_size=9),
    odd_color=Colors.Gray1,
    odd_text_style=Styles.Primary.patch(text_size=9),
)

table.draw(
    xy=(15, 46),
    width=90,
    height=40,
    data=[
        ["Service", "Tier", "Target SLA", "Avg Latency", "Status"],
        ["Auth API", "Tier 0", "99.99%", "12 ms", "HEALTHY"],
        ["Cart API", "Tier 1", "99.95%", "24 ms", "HEALTHY"],
        ["Order API", "Tier 1", "99.95%", "35 ms", "HEALTHY"],
        ["Analytics", "Tier 2", "99.90%", "142 ms", "DEGRADED"],
    ],
)
```
