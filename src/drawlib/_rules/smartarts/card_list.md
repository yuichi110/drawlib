# Drawlib CardList SmartArt Guidelines (`lib-smartarts-card-list`)

`CardList` renders vertical stacks (`direction="vertical"`) or horizontal step sequences (`direction="horizontal"`) of rich cards (`CardListItem`) equipped with circular or rounded-rectangle badges (`badge_shape="rounded_rect" | "circle" | "none"`), vector icons (`icon`), numbered/labeled badges (`badge_text`), multi-line descriptions (`description`), and optional inter-card connecting arrows (`show_arrows=True`).

---

## 1. Orientation & Badge Mechanics

- **Anchor (`align`)**: `CardList.draw(xy, width=90.0, height=50.0, *, align="bottom_left", scale=1.0)` anchors the `"bottom_left"` corner (default) or `"center"` of the bounding box at `xy`.
- **Orientation Modes (`direction`)**:
  - `"vertical"` *(default)*: Cards stack **top-to-bottom** inside the `(width, height)` bounding box. Each card places its badge/icon on the left and left-aligns `text` and `description` on the right.
  - `"horizontal"`: Cards sequence **left-to-right**. Each card centers its badge/icon in the upper zone with `text` and `description` centered below.
- **Connecting Arrows (`show_arrows=True`)**: Draws `"->"` arrows between adjacent visible cards across the `spacing` gap (`arrow_style` is required when `show_arrows=True`).
- **Badge Shapes & Content (`badge_shape`)**:
  - `"rounded_rect"` *(default)* or `"circle"`: Draws the badge background shape using `badge_style`.
  - `"none"`: Renders `icon` and/or `badge_text` directly without a background badge container.
  - When both `icon` and `badge_text` are provided on an item, the icon is rendered in the upper portion of the badge and `badge_text` is rendered below it inside the same badge.

---

## 2. Constructor, `CardListItem` & Methods

```python
from drawlib.smartarts import CardList, CardListItem

cl = CardList(
    *,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    badge_shape: Literal["circle", "rounded_rect", "none"] = "rounded_rect",
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    icon_style: Style | None = None,
    direction: Literal["vertical", "horizontal"] = "vertical",
    spacing: float = 2.5,
    show_arrows: bool = False,
    arrow_style: Style | None = None,
)
```

### Item Model (`CardListItem`) & `.items` Property

- `cl.items -> list[CardListItem]`: Returns the list of registered `CardListItem` instances.
- `CardListItem` attributes (mutable before or between `draw()` calls):
  - `text: str`: Primary card title text.
  - `description: str = ""`: Supporting description text (single-line or multi-line).
  - `badge_text: str | None = None`: Optional short badge label (e.g. `"1"`, `"L1"`, `"P0"`).
  - `icon: Callable[..., Any] | None = None`: Optional icon drawing callable (e.g. `phosphor.shield_check`).
  - `style: Style`: Card background rectangle style.
  - `text_style: Style`: Text style for `text`.
  - `description_style: Style | None = None`: Text style for `description` (required when `description` is non-empty).
  - `badge_style: Style | None = None`: Style for the badge background shape (required when `badge_shape != "none"` and `icon` or `badge_text` is present).
  - `badge_text_style: Style | None = None`: Text style for `badge_text` (required when `badge_text` is non-empty).
  - `icon_style: Style | None = None`: Style passed to `icon` (required when `icon` is provided).
  - `show: bool = True`: Visibility flag. Setting `item.show = False` hides that card (and any connecting arrow to/from it) while preserving the exact coordinates of all sibling cards.

### Per-Item Overrides (`add`) & Rendering (`draw`)

```python
item = cl.add(
    text: str,
    description: str = "",
    *,
    badge_text: str | None = None,
    icon: Callable[..., Any] | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    icon_style: Style | None = None,
    show: bool = True,
) -> CardListItem

cl.draw(
    xy: tuple[float, float],
    width: float = 90.0,
    height: float = 50.0,
    *,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

---

## 3. Production Example: Vertical Defense Cards & Horizontal Workflow Steps

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList
from drawlib.styles import Styles

setup(width=185, height=70)

# 1. Left: Vertical Feature Stack with Icon + Text Badges
cl_v = CardList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=3.0,
)
cl_v.add(
    "Edge Anycast Scrubbing",
    "Drop volumetric UDP/SYN floods at POPs",
    badge_text="L1",
    icon=phosphor.shield_check,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
    icon_style=Styles.WhiteBold,
)
cl_v.add(
    "Cloud Armor Rate Limiting",
    "Throttle suspicious ASN & JA3 fingerprints",
    badge_text="L2",
    icon=phosphor.funnel,
)
cl_v.add(
    "Origin Zero-Trust mTLS",
    "Verify cryptographic workload identity",
    badge_text="L3",
    icon=phosphor.lock_key,
)
cl_v.draw(xy=(6.0, 7.0), width=83.0, height=56.0, align="bottom_left", scale=1.0)

# 2. Right: Horizontal Step Sequence with Connecting Arrows
cl_h = CardList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    badge_shape="circle",
    badge_style=Styles.PrimaryNeutral,
    icon_style=Styles.PrimaryBold,
    direction="horizontal",
    show_arrows=True,
    arrow_style=Styles.Dark,
    spacing=4.5,
)
cl_h.add("1. Write Code", "Python API\nin Markdown", icon=phosphor.code)
cl_h.add("2. Build Docs", "Headless SVG\n& HTML build", icon=phosphor.gear)
cl_h.add(
    "3. AI Review",
    "Grid check &\nself-healing",
    icon=phosphor.eye,
    badge_style=Styles.PrimaryFlat,
    icon_style=Styles.WhiteBold,
)
cl_h.draw(xy=(96.0, 12.0), width=83.0, height=46.0, align="bottom_left", scale=1.0)

save()
```
