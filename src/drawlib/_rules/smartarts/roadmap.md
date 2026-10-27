# Drawlib Roadmap SmartArt Guidelines (`lib-smartarts-roadmap`)

`Roadmap` renders chronological milestone timelines, release roadmaps, migration phases, or incident chronicles along a straight or curved Bezier spine (`direction="vertical" | "horizontal"`), pairing spine badges (`badge_text`) with rounded-rectangle or pill cards (`card_shape="rounded_rect" | "pill"`) containing titles (`text`), descriptions/subtitles (`description`), and optional vector icons (`icon`).

---

## 1. Spine Modes & Coordinate Geometry

- **Anchor (`align`)**: `Roadmap.draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` anchors the `"bottom_left"` corner (default) or `"center"` of the overall bounding box at `xy`.
- **Vertical Spine Modes (`direction="vertical"`)**:
  - `curve_bend = 0.0` *(default)*: Draws a straight vertical spine on the left with a downward arrowhead (`"->"`) at the bottom, circular or pill badges on the spine (wide pill badges automatically activate when any `len(badge_text) >= 3`), and horizontal connector ticks into each milestone card.
  - `curve_bend != 0.0` (must be between `-0.5` and `0.5`): Draws a quadratic Bezier arc spine (`line_bezier1`) and shifts each milestone badge and card horizontally along the parametric Bezier curve.
- **Horizontal Spine Modes (`direction="horizontal"`)**:
  - `alternating = False` *(default)*: Draws a horizontal rightward arrow spine near the bottom and places all milestone cards in a single row above the spine.
  - `alternating = True`: Draws the horizontal spine along the vertical midline (`y0 + height / 2`) and alternates milestone cards above (`0, 2, 4, ...`) and below (`1, 3, 5, ...`) the spine.
- **Auto-Numbered `badge_text`**: When `badge_text=None` in `roadmap.add(...)`, `Roadmap` automatically assigns sequential 1-based numbers (`"1"`, `"2"`, `"3"`, ...).

---

## 2. Constructor, `RoadmapItem` & Methods

```python
from drawlib.smartarts import Roadmap, RoadmapItem

rm = Roadmap(
    *,
    style: Style,
    text_style: Style,
    spine_style: Style,
    badge_style: Style,
    badge_text_style: Style,
    description_style: Style | None = None,
    icon_style: Style | None = None,
    direction: Literal["vertical", "horizontal"] = "vertical",
    curve_bend: float = 0.0,
    card_shape: Literal["pill", "rounded_rect"] = "rounded_rect",
    alternating: bool = False,
    spacing: float = 2.5,
)
```

### Item Model (`RoadmapItem`) & `.items` Property

- `rm.items -> list[RoadmapItem]`: Returns the list of registered `RoadmapItem` instances.
- `RoadmapItem` attributes (mutable before or between `draw()` calls):
  - `text: str`: Primary milestone or phase title text.
  - `description: str = ""`: Supporting description or subtitle text.
  - `badge_text: str | None = None`: Short label displayed on the spine badge (auto-populated as `"1"`, `"2"`, ... when omitted in `add()`).
  - `icon: Callable[..., Any] | None = None`: Optional icon drawing callable displayed inside the milestone card.
  - `style: Style`: Style for the milestone card container.
  - `text_style: Style`: Text style for `text`.
  - `description_style: Style | None = None`: Text style for `description` (required when `description` is non-empty).
  - `badge_style: Style`: Style for the spine badge.
  - `badge_text_style: Style`: Text style for `badge_text`.
  - `icon_style: Style | None = None`: Style passed to `icon` (required when `icon` is provided).
  - `show: bool = True`: Visibility flag. Setting `item.show = False` hides that milestone's badge, connector, and card while keeping the spine and all remaining milestones at their exact positions.

### Per-Item Overrides (`add`) & Rendering (`draw`)

```python
item = rm.add(
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
) -> RoadmapItem

rm.draw(
    xy: tuple[float, float],
    width: float = 100.0,
    height: float = 60.0,
    *,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

---

## 3. Production Example: Vertical Roadmaps & Horizontal Alternating Timeline

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import Roadmap
from drawlib.styles import Styles

setup(width=185, height=110)

# 1. Top-Left: Vertical Straight Spine
rm_v1 = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.0,
    card_shape="rounded_rect",
    spacing=2.5,
)
rm_v1.add(
    "Foundation & Core Engine",
    "Pure-Python vector canvas & themes",
    badge_text="Q1",
    icon=phosphor.cube,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rm_v1.add("AI Agent Rules & CLI", "Headless HTML/PDF build & grid review", badge_text="Q2", icon=phosphor.robot)
rm_v1.add("Enterprise Cloud & GeoMap", "GCP diagrams & 215 country maps", badge_text="Q3", icon=phosphor.globe_hemisphere_east)
rm_v1.draw(xy=(6.0, 48.0), width=84.0, height=56.0, align="bottom_left", scale=1.0)

# 2. Top-Right: Vertical Curved Spine (Pill Cards, auto-numbered badge_text=None)
rm_v2 = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.22,
    card_shape="pill",
    spacing=2.5,
)
rm_v2.add(
    "1. Edge Anomaly Detected",
    "SYN/UDP flood hits 180 Gbps at Tokyo POP",
    icon=phosphor.warning,
    badge_style=Styles.AccentFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
    icon_style=Styles.AccentBold,
)
rm_v2.add("2. Anycast Scrubbing Active", "Malicious ASN traffic diverted to scrubbing", icon=phosphor.shield_check)
rm_v2.add(
    "3. Service Fully Restored",
    "Origin P99 latency stabilized at 11.4ms",
    icon=phosphor.check_circle,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rm_v2.draw(xy=(96.0, 48.0), width=83.0, height=56.0, align="bottom_left", scale=1.0)

# 3. Bottom: Horizontal Alternating Timeline
rm_h = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="horizontal",
    alternating=True,
    spacing=2.5,
)
rm_h.add("Audit & Discovery", "Map legacy Visio diagrams", badge_text="P1", icon=phosphor.magnifying_glass)
rm_h.add("Scaffold Repo", "Run drawlib init site", badge_text="P2", icon=phosphor.folder_open)
rm_h.add("CI/CD Pipeline", "Automate build & checks", badge_text="P3", icon=phosphor.git_branch)
rm_h.add(
    "Production Launch",
    "Publish HTML & A4 PDF",
    badge_text="P4",
    icon=phosphor.rocket_launch,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rm_h.draw(xy=(6.0, 5.0), width=173.0, height=38.0, align="bottom_left", scale=1.0)

save()
```
