# Drawlib Pyramid SmartArt Guidelines (`lib-smartarts-pyramid`)

`Pyramid` renders tiered, hierarchical trapezoids crowned by an apex triangle (`PyramidItem`). It is ideal for visualizing defense-in-depth security layers, testing pyramids, storage/memory hierarchies, and organizational governance.

---

## 1. Architecture & Geometry

- **Anchor (`align`)**: Bottom-Left coordinate `xy=(x, y)` (`align="bottom_left"`, default) or center coordinate (`align="center"`) of the bounding box.
- **Apex & Trapezoid Slices**: The vertex tier is drawn as a triangle; all other tiers are drawn as trapezoids widening progressively toward the base.
- **Orientations (`direction`)**:
  - `"bottom"` *(default)*: Base at the bottom, apex pointing upward (`+y`).
  - `"top"`: Inverted funnel—base at the top, apex pointing downward (`-y`).
  - `"left"`: Base on the left, apex pointing rightward (`+x`).
  - `"right"`: Base on the right, apex pointing leftward (`-x`).
- **Tier Ordering (`order`)**:
  - `"vertex_to_base"` *(default)*: First added item (`items[0]`) is placed at the apex/vertex; subsequent items progress toward the wide base.
  - `"base_to_vertex"`: First added item (`items[0]`) is placed at the wide base; subsequent items progress toward the apex/vertex.

---

## 2. Constructor, `PyramidItem` & Methods

```python
from drawlib.smartarts import Pyramid, PyramidItem

pyramid = Pyramid(
    *,
    style: Style,
    text_style: Style,
)
```

### Item Model (`PyramidItem`) & `.items` Property

- `pyramid.items -> list[PyramidItem]`: Returns the list of registered `PyramidItem` instances.
- `PyramidItem` attributes (mutable before or between `draw()` calls):
  - `text: str`
  - `style: Style`
  - `text_style: Style`
  - `show: bool = True`

### Adding Tiers & Drawing Modes

```python
tier = pyramid.add(
    text: str,
    *,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> PyramidItem

pyramid.draw(
    xy: tuple[float, float],
    width: float,
    height: float,
    margin: float,
    direction: Literal["bottom", "top", "left", "right"] = "bottom",
    order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self

pyramid.draw_flexible(
    xy: tuple[float, float],
    width: float,
    item_heights: list[float],
    margins: list[float],
    direction: Literal["bottom", "top", "left", "right"] = "bottom",
    order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

- `draw(...) -> Self`: Computes uniform tier heights across `N` items:
  $$\text{tier\_height} = \frac{\text{height} - (N - 1) \cdot \text{margin}}{N}$$
- `draw_flexible(...) -> Self`: Uses explicit `item_heights` (length `N`) and `margins` (length `N - 1`), ordered from base to vertex according to the rendered tier stack.

---

## 3. Production Example: Software Testing Pyramid

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.smartarts import Pyramid
from drawlib.styles import Styles

setup(width=100, height=65)

test_pyramid = Pyramid(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
test_pyramid.add("Manual (1%)", style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=9.5))
test_pyramid.add("End-to-End UI Tests (9%)", style=Styles.PrimaryNeutral)
test_pyramid.add("Integration & Contract Tests (20%)", style=Styles.SecondaryNeutral)
test_pyramid.add(
    "Unit Tests (70%)",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

test_pyramid.draw(
    xy=(15, 10),
    width=70,
    height=45,
    margin=1.5,
    direction="bottom",
    order="vertex_to_base",
)
save()
```
