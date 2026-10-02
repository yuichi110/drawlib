# MindMap Component

The `MindMapNode` component renders multi-directional, radial mindmaps and hierarchical feature maps centered around a central root topic. 
Branches can project to the left, right, top, or bottom, with automatic elbow connector routing.

---

## 1. Quick Example: Architecture Topology Map



<figure class="drawlib-image" style="text-align: center;">
  <img src="mindmap_images/mindmap_system_breakdown.png" alt="mindmap_1" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">System Architecture Breakdown with MindMap</figcaption>
</figure>



---

## 2. Geometry & Branching Directions

- **Center Anchor `(cx, cy)`**: The coordinate passed to `root.draw(xy=...)` anchors the **exact center** of the central root node.
- **Directional Branching (`branch`)**:
  - `"right"` *(default)*: Sub-branches extend to the right (`+x`).
  - `"left"`: Sub-branches extend to the left (`-x`).
  - `"top"`: Sub-branches extend upward (`+y`).
  - `"bottom"`: Sub-branches extend downward (`-y`).
- **Node Shapes**:
  - `"oval"`: Pill / ellipse container.
  - `"rectangle"`: Rectangular box with optional corner rounding (`r`).
  - `"none"`: Clean text label without border or background fill.

---

## 3. Node Class API

```python
MindMapNode(
    text: str,
    *,
    branch: Literal["left", "right", "top", "bottom"] | None = None,
    shape: Literal["oval", "rectangle", "none"] | None = None,
    size: tuple[float, float] | None = None,
    style: Style | None = None,
    r: float | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: float | None = None,
    vertical_margin: float | None = None,
    line_length: float | None = None,
    xy_shift: tuple[float, float] | None = None,
    children: list[MindMapNode] | None = None,
)
```
