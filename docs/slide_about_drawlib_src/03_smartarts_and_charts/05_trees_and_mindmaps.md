::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Hierarchies & Brainstorming (`TreeNode` & `MindMapNode`)
:::

::: block (80, 140) (660, 840) compact
## Two Complementary Tree Engines

### 1. `TreeNode` — Directory & Package Hierarchies
- **Top-Left Anchored**: Steps downward row-by-row with crisp orthogonal `├` and `└` connector lines.
- **Cascading Root Styles**: Set `text_style`, `line_style`, and margins once on the root `TreeNode`; all descendants inherit them automatically.
- **Custom Icon Attachments**: Use `TreeNode.register_drawing_item(...)` and `.set_drawing_item(name)` to prepend or append Phosphor icons (`phosphor.folder`, `phosphor.file_py`, `phosphor.file_code`).

### 2. `MindMapNode` — Two-Pass Radial & Org Trees
- **Pass 1 (Bottom-Up Measurement)**: Recursively measures exact subtree bounding heights and widths so branches never collide.
- **Pass 2 (Orthogonal Routing)**: Routes right-angled junction lines from the center root node across all 4 directions (`branch="left"`, `"right"`, `"top"`, `"bottom"`).
- **Flexible Node Shapes**: Mix `"oval"`, `"rectangle"`, and borderless `"none"` leaf labels.
:::

::: block (780, 140) (1060, 840)
```drawlib file:trees_and_mindmaps.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import MindMapNode, TreeNode
from drawlib.styles import Colors, Styles
from drawlib.text import text

clear()
setup(width=106, height=84)

# 1. Left Card: Repository TreeNode with Phosphor Icons
rectangle((21, 42), width=38, height=78, r=2.0, style=Styles.NeutralFlat)
text(
    (5, 76.5),
    "Monorepo Structure (TreeNode)",
    style=Styles.DarkBold.patch(text_size=9.2, text_halign="left"),
)

TreeNode.register_drawing_item(
    name="dir_icon",
    location="before",
    padding_width=3.8,
    function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary),
    args={"width": 2.6},
)
TreeNode.register_drawing_item(
    name="py_icon",
    location="before",
    padding_width=3.8,
    function=phosphor.file_py,
    style=Styles.Secondary.patch(icon_color=Colors.Secondary),
    args={"width": 2.6},
)
TreeNode.register_drawing_item(
    name="cfg_icon",
    location="before",
    padding_width=3.8,
    function=phosphor.file_code,
    style=Styles.Dark.patch(icon_color=Colors.Dark),
    args={"width": 2.6},
)

repo_tree = TreeNode(
    "drawlib-service/",
    text_style=Styles.DarkBold.patch(text_size=8.5),
    line_style=Styles.Muted.patch(line_width=1.0),
    line_horizontal_margin=2.4,
    line_horizontal_length=2.6,
    line_vertical_margin=5.6,
    children=[
        TreeNode(
            "src/api/",
            children=[
                TreeNode("router.py", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("py_icon"),
                TreeNode("auth.py", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("py_icon"),
                TreeNode("schemas.py", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("py_icon"),
            ],
        ).set_drawing_item("dir_icon"),
        TreeNode(
            "src/workers/",
            children=[
                TreeNode(" billing_job.py", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("py_icon"),
                TreeNode(" mailer.py", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("py_icon"),
            ],
        ).set_drawing_item("dir_icon"),
        TreeNode(
            "deploy/",
            children=[
                TreeNode("k8s-prod.yaml", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("cfg_icon"),
                TreeNode("Dockerfile", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("cfg_icon"),
            ],
        ).set_drawing_item("dir_icon"),
        TreeNode("pyproject.toml", text_style=Styles.Dark.patch(text_size=8.0)).set_drawing_item("cfg_icon"),
    ],
).set_drawing_item("dir_icon")

repo_tree.draw(xy=(6, 70))

# 2. Right Card: 4-Directional MindMapNode
rectangle((72, 42), width=60, height=78, r=2.0, style=Styles.MutedOutline)
text(
    (45, 76.5),
    "4-Way System Taxonomy (MindMapNode)",
    style=Styles.DarkBold.patch(text_size=9.2, text_halign="left"),
)

txt_root = Styles.WhiteBold.patch(text_size=8.0)
txt_branch = Styles.DarkBold.patch(text_size=7.5)
txt_leaf = Styles.Dark.patch(text_size=7.2)

mindmap = MindMapNode(
    "Platform Core",
    shape="oval",
    size=(19, 9),
    style=Styles.PrimaryFlat,
    text_style=txt_root,
    line_style=Styles.DarkBold.patch(line_width=1.2),
    line_length=6.0,
    horizontal_margin=2.5,
    vertical_margin=2.8,
    children=[
        MindMapNode(
            "Edge Clients",
            branch="left",
            shape="rectangle",
            size=(15, 6.5),
            r=1.0,
            style=Styles.PrimaryNeutral,
            text_style=txt_branch,
            children=[
                MindMapNode("Web SPA", shape="none", text_style=txt_leaf),
                MindMapNode("Mobile SDK", shape="none", text_style=txt_leaf),
            ],
        ),
        MindMapNode(
            "Microservices",
            branch="right",
            shape="rectangle",
            size=(16, 6.5),
            r=1.0,
            style=Styles.SecondaryNeutral,
            text_style=txt_branch,
            children=[
                MindMapNode("Order API", shape="none", text_style=txt_leaf),
                MindMapNode("Payment", shape="none", text_style=txt_leaf),
            ],
        ),
        MindMapNode(
            "Observability",
            branch="top",
            shape="rectangle",
            size=(16, 6.5),
            r=1.0,
            style=Styles.BlueNeutral,
            text_style=txt_branch,
            children=[
                MindMapNode("Traces", shape="none", text_style=txt_leaf),
                MindMapNode("Metrics", shape="none", text_style=txt_leaf),
            ],
        ),
        MindMapNode(
            "Data Stores",
            branch="bottom",
            shape="rectangle",
            size=(16, 6.5),
            r=1.0,
            style=Styles.TealNeutral,
            text_style=txt_branch,
            children=[
                MindMapNode("PostgreSQL", shape="none", text_style=txt_leaf),
                MindMapNode("Redis Cache", shape="none", text_style=txt_leaf),
            ],
        ),
    ],
)

mindmap.draw(xy=(72, 39))

save()
```
:::

::: note
- This slide compares Drawlib's two hierarchical SmartArt components: `TreeNode` and `MindMapNode`.
- **Left (`TreeNode`)**: Designed for vertical directory and package listings. Using `TreeNode.register_drawing_item`, we bind Phosphor vector icons (`phosphor.folder`, `phosphor.file_py`, `phosphor.file_code`) that automatically align with the orthogonal tree lines.
- **Right (`MindMapNode`)**: Uses a two-pass layout algorithm to measure subtree extents first and then route orthogonal connectors in all four directions (`branch="left"`, `"right"`, `"top"`, `"bottom"`) around the central `"Platform Core"` oval node.
:::
