# Tree Component

The `TreeNode` component renders hierarchical tree structures, such as codebase directory trees, organizational hierarchy charts, and taxonomy categorizations. 
It automates vertical branch alignment, indentation levels, and tree connector lines.

---

## 1. Quick Example: Project Directory Hierarchy



<figure class="drawlib-image" style="text-align: center;">
  <img src="tree_images/tree_project_structure.png" alt="tree_1" style="width: 600px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Project File Structure with TreeNode</figcaption>
</figure>



---

## 2. Geometry, Lifecycle & Coordinate Mechanics

- **Top-Left Anchor `(x, y)`**: The coordinate passed to `root.draw(xy=..., *, scale: float = 1.0)` represents the **top-left corner** of the root node text. Passing `scale` proportionally scales indentation, vertical spacing, icons, and text sizes relative to `xy`.
- **Downward & Rightward Flow**: Sub-directories and files branch downward and indent horizontally to the right.
- **Visibility (`show: bool = True`)**:
  - Both `TreeNode(text, ..., show: bool = True)` and `node.add(child, *, show: bool = True)` control node visibility.
  - Setting `show=False` hides the node, its incoming branch line, and its subtree while **preserving the exact vertical Y-coordinates of all subsequent sibling nodes**.
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
