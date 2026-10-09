# Pyramid

The `Pyramid` component renders tiered hierarchical trapezoids crowned by an apex triangle. It supports standard upright pyramids, inverted funnels, horizontal orientations, and custom per-tier heights—making it ideal for software testing pyramids, DIKW knowledge hierarchies, defense-in-depth tiers, and conversion funnels.

---

## 1. Upward Hierarchy Pyramid (`align="bottom"`)

By default (`align="bottom", order="vertex_to_base"`), the first added item is placed at the top apex triangle, and subsequent items form progressively wider trapezoidal tiers toward the base.

```drawlib show-code 600px center file:smartarts_pyramid_testing.png caption:"Software Testing Pyramid (Upright Hierarchy)"
from drawlib.canvas import save, setup
from drawlib.smartarts import Pyramid
from drawlib.styles import Styles

setup(width=110, height=65)

pyramid = Pyramid(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.5),
)

# Added from apex (top) to base (bottom) when order="vertex_to_base"
pyramid.add(
    "Manual\n(5%)",
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
pyramid.add(
    "End-to-End UI Tests (15%)",
    style=Styles.SecondaryNeutral,
)
pyramid.add(
    "Integration & Contract Tests (30%)",
    style=Styles.PrimaryNeutral,
)
pyramid.add(
    "Fast Automated Unit Tests (50%)",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

pyramid.draw(
    xy=(15, 8),
    width=80,
    height=48,
    margin=1.5,
    align="bottom",
    order="vertex_to_base",
)
save()
```

---

## 2. Inverted Conversion Funnel with Custom Tier Heights (`draw_flexible`)

Setting `align="top"` and `order="base_to_vertex"` inverts the pyramid into a top-down funnel where the first item is the wide top intake and the last item is the bottom apex. Using `draw_flexible(...)` lets you assign custom `item_heights` and `margins` to each stage.

```drawlib show-code 600px center file:smartarts_pyramid_funnel.png caption:"Telemetry Ingestion & Filtering Funnel (align='top' with draw_flexible)"
from drawlib.canvas import save, setup
from drawlib.smartarts import Pyramid
from drawlib.styles import Styles

setup(width=110, height=65)

funnel = Pyramid(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.5),
)

# Added from wide top base to bottom apex when align="top", order="base_to_vertex"
funnel.add("1. Raw Edge Telemetry (100k events/s)", style=Styles.Neutral)
funnel.add("2. Schema Validation & Deduplication (40k/s)", style=Styles.PrimaryNeutral)
funnel.add("3. Anomaly Correlation Window (2.5k/s)", style=Styles.SecondaryNeutral)
funnel.add(
    "4. Alerts",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)

funnel.draw_flexible(
    xy=(15, 8),
    width=80,
    item_heights=[9.5, 10.5, 11.0, 14.0],
    margins=[1.5, 1.5, 1.5],
    align="top",
    order="base_to_vertex",
)
save()
```

---

## 3. Geometry, Orientations & Ordering

- **Bottom-Left Anchor `(x, y)`**: The `xy` coordinate passed to `draw()` or `draw_flexible()` specifies the **bottom-left corner** of the pyramid's bounding box.
- **Alignment (`align`)**:
  - `"bottom"` *(default)*: Upright pyramid—wide base at the bottom, apex pointing up.
  - `"top"`: Inverted funnel—wide base at the top, apex pointing down.
  - `"left"`: Horizontal pyramid—wide base on the left, apex pointing right.
  - `"right"`: Horizontal pyramid—wide base on the right, apex pointing left.
- **Item Ordering (`order`)**:
  - `"vertex_to_base"` *(default)*: First added item is placed at the triangular apex; last added item is at the wide base.
  - `"base_to_vertex"`: First added item is placed at the wide base; last added item is at the triangular apex.

```drawlib fold-code 650px center file:smartarts_pyramid_orientations.png caption:"All Four Pyramid Alignments: bottom, top, left, and right"
from drawlib.canvas import save, setup
from drawlib.shapes import circle
from drawlib.smartarts import Pyramid
from drawlib.styles import Styles
from drawlib.text import text

setup(width=145, height=48)

p = Pyramid(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=7.5),
)
p.add("1", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=7.5))
p.add("2", style=Styles.PrimaryNeutral)
p.add("3", style=Styles.SecondaryNeutral)

panels = [
    ("bottom", (6.0, 9.0), "align='bottom'\n(Upright)"),
    ("top", (41.0, 9.0), "align='top'\n(Inverted Funnel)"),
    ("left", (76.0, 9.0), "align='left'\n(Apex Right)"),
    ("right", (111.0, 9.0), "align='right'\n(Apex Left)"),
]

for align_val, (px, py), label in panels:
    text((px + 14.0, 42.5), label, style=Styles.BlackBold.patch(text_size=8.2))
    p.draw(xy=(px, py), width=28.0, height=26.0, margin=1.0, align=align_val, order="vertex_to_base")
    circle((px, py), radius=1.0, style=Styles.DangerFlat)
    text((px + 2.0, py - 3.5), f"xy=({int(px)}, {int(py)})", style=Styles.DangerBold.patch(text_size=7.0, halign="left"))

save()
```

---

## 4. API Reference

### Constructor
```python
Pyramid(
    *,
    style: Style,
    text_style: Style,
)
```

### Methods & Properties
- **`add(text: str, *, style: Style | None = None, text_style: Style | None = None, show: bool = True) -> PyramidItem`**:
  Appends a tier to the pyramid and returns a mutable `PyramidItem` (`style`, `text`, `text_style`, `show`). Setting `show=False` hides that tier while preserving its slice geometry so sibling tiers never shift.
- **`pyramid.items -> list[PyramidItem]`**:
  Returns the list of all registered `PyramidItem` instances (`style: Style`, `text: str`, `text_style: Style`, `show: bool`), allowing deferred mutation before or between `draw()` calls.
- **`draw(xy: tuple[float, float], width: float, height: float, margin: float, align: Literal["bottom", "top", "left", "right"] = "bottom", order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base", scale: float = 1.0) -> None`**:
  Renders the pyramid with uniform tier heights separated by `margin`, with optional proportional scaling around `xy`.
- **`draw_flexible(xy: tuple[float, float], width: float, item_heights: list[float], margins: list[float], align: Literal["bottom", "top", "left", "right"] = "bottom", order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base", scale: float = 1.0) -> None`**:
  Renders the pyramid with explicit per-tier heights (`len(item_heights) == len(items)`) and inter-tier margins (`len(margins) == len(items) - 1`). Notice that `item_heights` are ordered from the base toward the vertex.

