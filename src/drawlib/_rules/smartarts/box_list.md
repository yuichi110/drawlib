# Drawlib BoxList SmartArt Guidelines (`lib-smartarts-box-list`)

`BoxList` draws contiguous linear sequences of rectangular boxes or cards with optional per-item highlight overrides (`BoxListItem`).

---

## 1. Architecture & Layout Direction

- **Anchor (`align`)**: Coordinate `xy=(x, y)` marks the `"bottom_left"` corner (default) or `"center"` of the overall bounding box across all 4 stacking directions.
- **Stacking Direction (`direction`)**:
  - `"left"` *(default)*: Boxes sequence from left to right (`+x`). Total bounding size is `(N * box_width, box_height)`.
  - `"right"`: Boxes sequence from right to left (`-x`).
  - `"bottom"`: Boxes stack from bottom to top (`+y`). Total bounding size is `(box_width, N * box_height)`.
  - `"top"`: Boxes stack from top to bottom (`-y`).
- **Z-Order Highlighting**: `BoxList.draw()` automatically renders default-styled boxes in Pass 1 and custom-styled (`style` or `text_style` overridden) boxes in Pass 2 so highlighted borders cleanly overlap adjacent default borders.

---

## 2. Constructor, `BoxListItem` & Methods

```python
from drawlib.smartarts import BoxList, BoxListItem

box_list = BoxList(
    *,
    style: Style,
    text_style: Style,
)
```

### Item Model (`BoxListItem`) & `.items` Property

- `box_list.items -> list[BoxListItem]`: Returns the list of registered `BoxListItem` instances.
- `BoxListItem` attributes (mutable before or between `draw()` calls):
  - `text: str`
  - `style: Style`
  - `text_style: Style`
  - `show: bool = True`

### Methods

```python
item = box_list.add(
    text: str,
    *,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> BoxListItem

box_list.draw(
    xy: tuple[float, float],
    box_width: float,
    box_height: float,
    direction: Literal["left", "right", "bottom", "top"] = "left",
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

- `add(...) -> BoxListItem`: Appends a box with optional custom `style` and `text_style` overrides and returns the public `BoxListItem` instance. Setting `item.show = False` hides that specific box while keeping all remaining boxes at their exact coordinates.
- `draw(...) -> Self`: Renders all visible boxes in the specified `direction` anchored at `xy` (`"bottom_left"` or `"center"`) with optional proportional `scale`, returning `self`.

---

## 3. Production Example: Horizontal Service Pipeline & Status Cards

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.smartarts import BoxList
from drawlib.styles import Styles

setup(width=110, height=50)

pipeline = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
pipeline.add("1. Ingestion")
pipeline.add("2. Validation")
# Highlighted hero step (returns BoxListItem)
hero_item = pipeline.add(
    "3. ML Inference",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)
pipeline.add("4. Persistence", style=Styles.SecondaryNeutral)
pipeline.add("5. Dispatch")
pipeline.draw(xy=(8, 30), box_width=18, box_height=10, direction="left")

status_list = BoxList(
    style=Styles.NeutralFlat,
    text_style=Styles.DarkBold.patch(text_size=9.5),
)
for label in ("Cluster A: OK", "Cluster B: OK", "Cluster C: SYNC"):
    status_list.add(label)
status_list.draw(xy=(8, 8), box_width=25, box_height=7, direction="left")
save()
```
