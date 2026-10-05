# Tree Component

The `TreeNode` component renders hierarchical tree structures, such as codebase directory trees, organizational hierarchy charts, and taxonomy categorizations. 
It automates vertical branch alignment, indentation levels, and tree connector lines.

---

## 1. Quick Example: Project Directory Hierarchy

```drawlib 600px center file:tree_project_structure.png caption:"Project File Structure with TreeNode"
from drawlib.canvas import setup
from drawlib.smartarts import TreeNode
from drawlib.icons import phosphor
from drawlib.styles import Styles

setup(width=100, height=60)

# Register custom icons for folders and files
TreeNode.register_drawing_item(
    name="folder", location="before", padding_width=4.0, function=phosphor.folder,
    style=Styles.PrimaryFlat, args={"width": 3.0}
)
TreeNode.register_drawing_item(
    name="file", location="before", padding_width=4.0, function=phosphor.file_text,
    style=Styles.Dark, args={"width": 3.0}
)

root = TreeNode(
    "src/",
    text_style=Styles.DarkBold,
    line_style=Styles.DarkLight,
    line_horizontal_margin=3.0,
    line_horizontal_length=3.0,
    line_vertical_margin=6.0,
    children=[
        TreeNode("components/", children=[
            TreeNode("Button.py").set_drawing_item("file"),
            TreeNode("Modal.py").set_drawing_item("file"),
        ]).set_drawing_item("folder"),
        TreeNode("utils.py").set_drawing_item("file"),
    ]
).set_drawing_item("folder")

root.draw(xy=(10, 50))
```

---

## 2. Geometry & Coordinate Mechanics

- **Top-Left Anchor `(x, y)`**: The coordinate passed to `root.draw(xy=...)` represents the **top-left corner** of the root node text.
- **Downward & Rightward Flow**: Sub-directories and files branch downward and indent horizontally to the right.
- **Root Node Style & Margin Requirements**:  
  When instantiating the root `TreeNode`, both styles and all three layout spacing arguments must be configured (child nodes inherit them automatically via cascading):
  - `text_style`: Default text style for node labels.
  - `line_style`: Default line style for tree branch connectors.
  - `line_horizontal_margin`: Horizontal gap between parent label and vertical connector line.
  - `line_horizontal_length`: Length of the horizontal tick connecting to child nodes.
  - `line_vertical_margin`: Vertical row spacing between adjacent items.

---

## 3. Registering Icons (`register_drawing_item`)

You can attach vector icons or visual badges to tree items using `register_drawing_item`:

```python
TreeNode.register_drawing_item(
    name="custom_badge",
    location="before",  # "before" or "after" the label text
    padding_width=4.0,
    function=phosphor.file_code,
    style=Styles.AccentFlat,
    args={"width": 3.5},
)

# Apply to node
node = TreeNode("config.yaml").set_drawing_item("custom_badge")
```
