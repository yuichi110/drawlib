# SmartArts Overview

Drawing structured diagrams (such as process flows, comparison tables, directory trees, or mindmaps) using raw shapes and lines often requires calculating hundreds of manual coordinates. 
The `drawlib.smartarts` module eliminates this boilerplate by providing **high-level, declarative layout components**.

---

## 1. What SmartArts Can Do



<figure class="drawlib-image" style="text-align: center;">
  <img src="overview_images/smartarts_showcase.png" alt="overview_1" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">SmartArts High-Level Component Showcase</figcaption>
</figure>



---

## 2. Component Catalog Matrix

| Component | Primary Use Case | Anchor System | Key Methods |
| :--- | :--- | :--- | :--- |
| **`ChevronProcess`** | Phased pipelines, CI/CD stages, migration roadmaps | Bottom-Left `(x, y)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`Cycle`** | PDCA devops loops, circular lifecycles, state loops | Center `(cx, cy)` | `add(..., show=True)`, `set_center()`, `draw(..., scale=1.0)` |
| **`Table`** | Service SLAs, specification matrices, DB schemas | Top-Left `(x, y)` | `set_style_cell_*()`, `draw(xy, w, h, data, scale=1.0)` |
| **`TreeNode`** | Directory hierarchies, org charts, taxonomy trees | Top-Left `(x, y)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`MindMapNode`** | Brainstorming nodes, radial feature maps | Center `(cx, cy)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`GridLayout`** | Layered architectures, dashboard card grids | Bottom-Left `(x, y)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`Pyramid`** | Testing pyramids, tiered memory/cache hierarchies | Bottom-Left `(x, y)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`BoxList`** | Linear horizontal or vertical card sequences | Directional `(x, y)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`BulletPoints`** | Architectural takeaways, RFC key points | Top-Left `(x, y)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`SourceCode`** | Syntax-highlighted code blocks in diagrams | Top-Left `(x, y)` | `add(..., show=True)`, `draw(..., scale=1.0)` |
| **`GeoMap`** | Geographical maps (`GeoMap.World.*`, `GeoMap.Countries.*`, `GeoMap.Cities.*`) | Bottom-Left `(x, y)` | `get_areas()`, `set_area_styles()`, `draw()`, `get_area_xy()`, `lonlat_to_xy()` |

---

## 3. Coordinate Anchor Conventions

Understanding anchor points is essential when combining SmartArts with other elements:
- **Top-Left Anchored (`Table`, `TreeNode`, `BulletPoints`, `SourceCode`)**:  
  You specify the top-left coordinate `(x, y)`. Content flows horizontally to the right and vertically downward (`y` decreases).
- **Bottom-Left Anchored (`ChevronProcess`, `GridLayout`, `Pyramid`, `GeoMap`)**:  
  You specify the bottom-left coordinate `(x, y)`. The bounding container extends rightward and upward (`y` increases).
- **Center Anchored (`Cycle`, `MindMapNode`)**:  
  You specify the center coordinate `(cx, cy)`. The diagram expands symmetrically or radially around the center.

---

## 4. Unified Component Lifecycle (`add()`, `show`, and `scale`)

All SmartArts components follow a consistent 3-step lifecycle:
1. **Configure (`__init__`)**: Instantiate the component with default styles, spacing, and layout parameters.
2. **Register Content (`add(..., show: bool = True)`)**: Populate stages, rows, cards, or child nodes.
   - Setting `show=False` hides that specific item during rendering while **preserving the full geometry and layout slots of all sibling items** (preventing layout shifts when revealing items step-by-step).
3. **Render (`draw(xy=..., ..., scale: float = 1.0)`)**: Render the component onto the canvas at anchor `xy`.
   - Passing `scale` (e.g. `scale=0.8` or `scale=1.2`) proportionally scales all dimensions, spacing, line widths, and font sizes relative to the anchor `xy`.
