# Drawlib BulletPoints SmartArt Guidelines (`lib-smartarts-bullet-points`)

`BulletPoints` renders nested bulleted lists with customizable indentation levels, custom bullet marker shapes or vector icons, and uniform vertical line spacing.

---

## 1. Coordinate & Indent Mechanics

- **Anchor**: Fixed Top-Left coordinate `xy=(x, y)`. The first item is rendered at `y`, and subsequent items step downward (`y - vertical_margin`) regardless of `item.show` so line positions never jump across animation frames.
- **Indentation Levels (`level: int`)**:
  - `level = 0`: Section headers or root items (no bullet marker drawn by default; text starts at `x`).
  - `level = 1`: Primary bullet items (defaults to a filled circle marker of `radius=0.5` matching `text_color`).
  - `level = 2`: Secondary nested items (defaults to an open outline circle marker of `radius=0.5` matching `text_color`).
  - `level >= 3`: Custom indent levels (configure marker via `set_bullet_style(level, ...)`).
- **Horizontal Positions**:
  - Text X coordinate: `x_text = x + indent_width * indent`
  - Bullet Marker X coordinate: `x_marker = x + indent_width * (indent - 0.5)`

---

## 2. Constructor, `BulletPointItem` & Methods

```python
from drawlib.smartarts import BulletPointItem, BulletPoints

bp = BulletPoints(
    *,
    text_style: Style,
    vertical_margin: float,
    indent_width: float,
)
```

### Item Model (`BulletPointItem`) & `.items` Property

- `bp.items -> list[BulletPointItem]`: Returns the list of registered `BulletPointItem` instances.
- `BulletPointItem` attributes (mutable before or between `draw()` calls):
  - `indent: int`: Indentation level captured when `add()` was called.
  - `text: str`: Bullet text string.
  - `text_style: Style`: Text style for this item (`item.style` is also provided as a property alias for `item.text_style`).
  - `show: bool = True`: Visibility flag. Setting `item.show = False` skips drawing the text and bullet marker while preserving its vertical row slot (`vertical_margin`).

### Methods

```python
bp.set_indent(level: int) -> None

bp.set_bullet_style(
    indent_level: int,
    function: Callable[..., Any],
    style: Style,
    args: dict[str, Any],
) -> None

item = bp.add(
    text: str,
    *,
    text_style: Style | None = None,
    show: bool = True,
) -> BulletPointItem

bp.draw(
    xy: tuple[float, float],
    scale: float = 1.0,
) -> Self
```

- `set_indent(level: int)`: Sets the active indentation level (`0`, `1`, `2`, ...) for all subsequent `add()` calls.
- `set_bullet_style(indent_level, function, style, args)`: Overrides the bullet marker drawing function (e.g. `circle`, `rectangle`, `phosphor.check_circle`) for `indent_level`. `style` is automatically patched with `halign="center", valign="center"`.
- `add(text, *, text_style=None, show=True) -> BulletPointItem`: Appends a bullet item at the current indent level and returns the public `BulletPointItem` instance.
- `draw(xy, scale=1.0) -> Self`: Renders all visible bullet points starting from top-left `xy` with optional proportional `scale`, returning `self`.

---

## 3. Production Example: Architecture Decision RFC Summary

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.preset_colors import CssColors
from drawlib.shapes import rectangle
from drawlib.smartarts import BulletPoints
from drawlib.styles import Colors, Styles

setup(width=115, height=65)

bp = BulletPoints(
    text_style=Styles.Primary.patch(text_size=10.0, text_color=Colors.Dark),
    vertical_margin=5.0,
    indent_width=5.0,
)
bp.set_bullet_style(
    indent_level=1,
    function=rectangle,
    style=Styles.Primary.patch(shape_fill_color=Colors.Primary, shape_line_width=0),
    args={"width": 1.2, "height": 1.2},
)
bp.set_bullet_style(
    indent_level=2,
    function=phosphor.check_circle,
    style=Styles.Primary.patch(icon_color=CssColors.ForestGreen),
    args={"width": 2.2},
)

bp.set_indent(0)
bp.add("RFC 402: Event-Driven Order Processing", text_style=Styles.PrimaryBold.patch(text_size=11.0))

bp.set_indent(1)
bp.add("Core Architectural Guarantees:", text_style=Styles.DarkBold.patch(text_size=10.0))
bp.set_indent(2)
bp.add("At-least-once message delivery via Apache Kafka partitioned topics")
bp.add("Idempotent event consumers using Redis deduplication filters")
bp.add("Dead-letter queue (DLQ) with automatic retry backoff")

bp.set_indent(1)
bp.add("Migration & Rollout Plan:", text_style=Styles.DarkBold.patch(text_size=10.0))
bp.set_indent(2)
bp.add("Phase 1: Shadow write events to Kafka cluster")
bp.add("Phase 2: Gradual 10% canary traffic migration")

bp.draw(xy=(10, 56))
save()
```
