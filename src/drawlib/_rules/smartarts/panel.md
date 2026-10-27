# Drawlib Panel SmartArt Guidelines (`lib-smartarts-panel`)

`Panel` renders a titled container box with a header band (`header_variant="filled" | "underline" | "floating" | "window"`) and provides `get_content_box(...)` to automatically compute the inner drawable `(inner_xy, inner_width, inner_height)` for nesting other SmartArts, Charts, or Diagrams inside the panel.

---

## 1. Header Variants & Explicit Style Validation

Every displayed element on a `Panel` requires an explicit `Style` (passing `description` without `description_style`, `icon` without `icon_style`, or `header_variant="window"` without `dot_styles` raises a `ValueError`):

1. **`header_variant="filled"` *(default)***: Draws a solid filled top header band (`header_style`) with rounded top corners and a clean horizontal separator line.
2. **`header_variant="underline"`**: Draws the outer body frame (`style`) and places the title/icon/description above a horizontal divider line (`header_style`) inset from the side borders.
3. **`header_variant="floating"`**: Draws a stadium/pill badge (`header_style`) straddling the top border of the body frame.
4. **`header_variant="window"`**: Draws a filled top header bar (`header_style`) with 3 macOS/browser-style window control dots on the left (`dot_styles` required: pass either a single `Style` or a 3-tuple `(close_style, minimize_style, zoom_style)`).

---

## 2. Constructor & Methods (`draw`, `get_content_box`)

```python
from drawlib.smartarts import Panel

p = Panel(
    text: str,
    description: str = "",
    *,
    style: Style,
    header_style: Style,
    text_style: Style,
    description_style: Style | None = None,
    icon: Callable[..., Any] | None = None,
    icon_style: Style | None = None,
    dot_styles: tuple[Style, Style, Style] | Style | None = None,
    header_variant: Literal["filled", "underline", "floating", "window"] = "filled",
    header_height: float = 8.0,
    header_align: Literal["left", "center"] = "left",
    show: bool = True,
)
```

### Rendering & Inner Content Box Calculation

- **`draw(xy, width=80.0, height=50.0, *, align="bottom_left", scale=1.0)`** *(default signature `width: float = 100.0, height: float = 60.0`)*:
  ```python
  p.draw(
      xy: tuple[float, float],
      width: float = 100.0,
      height: float = 60.0,
      *,
      align: Literal["bottom_left", "center"] = "bottom_left",
      scale: float = 1.0,
  ) -> Self
  ```
  Renders the outer panel body and header at `xy` (`"bottom_left"` or `"center"`), returning `self`.

- **`get_content_box(xy, width=80.0, height=50.0, *, padding=(4.0, 3.0), align="bottom_left", scale=1.0)`** *(also supports `content_align: Literal["bottom_left", "center"] | None = None`)*:
  ```python
  inner_xy, inner_w, inner_h = p.get_content_box(
      xy: tuple[float, float],
      width: float = 100.0,
      height: float = 60.0,
      *,
      padding: float | tuple[float, float] = (4.0, 3.0),
      align: Literal["bottom_left", "center"] = "bottom_left",
      content_align: Literal["bottom_left", "center"] | None = None,
      scale: float = 1.0,
  ) -> tuple[tuple[float, float], float, float]
  ```
  Subtracts `header_height` from the top of the panel and insets all four sides by `padding` (a single float or `(pad_x, pad_y)` tuple), returning `(inner_xy, inner_width, inner_height)`. When `content_align=None` (default), `inner_xy` uses the same anchor mode as `align`.

---

## 3. Production Example: Side-by-Side Comparison Framed with `Panel`

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles

setup(width=144, height=58)

# Left Panel: Filled Header Variant
left_panel = Panel(
    "Before: Legacy GUI Workflow",
    "Manual Export",
    style=Styles.Neutral,
    header_style=Styles.SecondaryNeutral.patch(shape_line_width=1.2),
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    icon=phosphor.warning_circle,
    icon_style=Styles.DarkBold,
    header_variant="filled",
    header_height=8.5,
)
left_panel.draw((5.0, 5.0), width=64.0, height=48.0, align="bottom_left", scale=1.0)
l_xy, l_w, l_h = left_panel.get_content_box(
    (5.0, 5.0),
    width=64.0,
    height=48.0,
    padding=(3.5, 3.0),
    align="bottom_left",
    scale=1.0,
)

legacy_list = CardList(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=9.5),
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    spacing=2.0,
)
legacy_list.add("External GUI Tool", "Binary blobs outside Git control", badge_text="1")
legacy_list.add("Manual PNG Copy-Paste", "Screenshots drift from real code", badge_text="2")
legacy_list.add("Broken Font Sizing", "Tiny unreadable labels when scaled", badge_text="3")
legacy_list.draw(l_xy, width=l_w, height=l_h)

# Right Panel: Window Chrome Header Variant
right_panel = Panel(
    "After: Illustrated Docs as Code",
    "Git SoT + AI Loop",
    style=Styles.PrimaryNeutral,
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    description_style=Styles.White.patch(text_size=9.5),
    icon=phosphor.sparkle,
    icon_style=Styles.White,
    dot_styles=(
        Styles.DangerFlat.patch(shape_line_width=0),
        Styles.WarningFlat.patch(shape_line_width=0),
        Styles.SuccessFlat.patch(shape_line_width=0),
    ),
    header_variant="window",
    header_height=8.5,
)
right_panel.draw((75.0, 5.0), width=64.0, height=48.0, align="bottom_left", scale=1.0)
r_xy, r_w, r_h = right_panel.get_content_box(
    (75.0, 5.0),
    width=64.0,
    height=48.0,
    padding=(3.5, 3.0),
    align="bottom_left",
    scale=1.0,
)

modern_list = CardList(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=9.5),
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
    spacing=2.0,
)
modern_list.add("Declarative Python API", "Version-controlled in Git alongside code", badge_text="1")
modern_list.add("Headless CLI Build", "Incremental SQLite cache & link check", badge_text="2")
modern_list.add("Autonomous Grid Review", "AI self-corrects geometry with -g", badge_text="3")
modern_list.draw(r_xy, width=r_w, height=r_h)

save()
```
