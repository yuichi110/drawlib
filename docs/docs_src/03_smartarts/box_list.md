# BoxList

The `BoxList` component renders contiguous linear sequences of rectangular cards along a horizontal or vertical axis. Custom-styled items are automatically rendered in a second pass so their borders cleanly overlay adjacent default boxes—making `BoxList` ideal for memory/packet layouts, stage sequences, and vertical feature stacks.

---

## 1. Horizontal Sequence with Highlighted Focal Stage (`align="left"`)

When `align="left"` (the default), boxes flow horizontally to the right (`+x`) starting from `xy=(x, y)`. You can combine multiple `BoxList` instances with arrows or labels to illustrate pipelines and packet structures.

```drawlib show-code 650px center file:smartarts_boxlist_horizontal.png caption:"Horizontal Pipeline Sequence and Packet Header Layout with BoxList"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.smartarts import BoxList
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=52)

# 1. Top: Data Processing Pipeline Sequence
text((10, 44), "Request Processing Stages", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))

pipeline = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.5),
)
pipeline.add("1. Ingress")
pipeline.add("2. AuthN / AuthZ", style=Styles.PrimaryNeutral)
pipeline.add(
    "3. Rate Limiter",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
pipeline.add("4. Router", style=Styles.SecondaryNeutral)
pipeline.add("5. Upstream")
pipeline.draw(xy=(10, 27), box_width=20.0, box_height=11.0, align="left")

# 2. Bottom: Contiguous Binary Frame / Memory Layout
text((10, 19), "Frame Wire Layout (Bytes)", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))

packet = BoxList(
    style=Styles.NeutralFlat,
    text_style=Styles.Dark.patch(text_size=9.0),
)
packet.add("Magic (2B)")
packet.add("Version (1B)")
packet.add("Flags (1B)")
packet.add("Payload Length (4B)", style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=9.0))
packet.add("CRC32 Checksum (4B)")
packet.draw(xy=(10, 6), box_width=20.0, box_height=8.5, align="left")

line((60, 26), (60, 16), arrow_head="->", style=Styles.MutedDashed)
save()
```

---

## 2. Vertical Feature & Layer Stack (`align="bottom"` / `align="top"`)

Using `align="bottom"` stacks boxes vertically upward (`+y`) from `xy`, while `align="top"` stacks boxes downward (`-y`) from `xy`. Patching `shape_r` on the box style creates rounded feature cards.

```drawlib show-code 600px center file:smartarts_boxlist_vertical_stack.png caption:"Vertical Platform Layer Stacks with BoxList"
from drawlib.canvas import save, setup
from drawlib.smartarts import BoxList
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=62)

# Left Stack: Bottom-up OS / Runtime Stack (align="bottom")
text((30, 55), "Runtime Stack (Bottom-Up)", style=Styles.DarkBold.patch(text_size=10.5))

runtime_stack = BoxList(
    style=Styles.Neutral.patch(shape_r=1.2),
    text_style=Styles.DarkBold.patch(text_size=9.5),
)
runtime_stack.add("Linux Kernel & cgroups v2", style=Styles.Neutral.patch(shape_r=1.2))
runtime_stack.add("Containerd Runtime", style=Styles.SecondaryNeutral.patch(shape_r=1.2))
runtime_stack.add("Service Mesh Sidecar (Envoy)", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
runtime_stack.add(
    "Application Workload Pod",
    style=Styles.PrimaryFlat.patch(shape_r=1.2),
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
runtime_stack.draw(xy=(10, 8), box_width=42.0, box_height=10.5, align="bottom")

# Right Stack: Top-down Priority Tiers (align="top")
text((85, 55), "SLA Priority Tiers (Top-Down)", style=Styles.DarkBold.patch(text_size=10.5))

sla_tiers = BoxList(
    style=Styles.Neutral.patch(shape_r=1.2),
    text_style=Styles.DarkBold.patch(text_size=9.5),
)
sla_tiers.add(
    "Tier 0: Mission Critical (99.99%)",
    style=Styles.PrimaryFlat.patch(shape_r=1.2),
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
sla_tiers.add("Tier 1: Core Business (99.9%)", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
sla_tiers.add("Tier 2: Internal Tools (99.5%)", style=Styles.SecondaryNeutral.patch(shape_r=1.2))
sla_tiers.add("Tier 3: Batch & Best-Effort", style=Styles.Neutral.patch(shape_r=1.2))
sla_tiers.draw(xy=(64, 50), box_width=42.0, box_height=10.5, align="top")
save()
```

---

## 3. Directional Alignment & Two-Pass Z-Order

- **Directional Alignment (`align`)**:
  - `"left"` *(default)*: Boxes sequence rightward (`+x`) from `xy=(x, y)` (where `x` is the left edge and `y` is the bottom edge of the row).
  - `"right"`: Boxes sequence leftward (`-x`) from `xy=(x, y)` (where `x` is the right edge and `y` is the bottom edge of the row).
  - `"bottom"`: Boxes stack upward (`+y`) from `xy=(x, y)` (where `x` is the left edge and `y` is the bottom edge of the first box).
  - `"top"`: Boxes stack downward (`-y`) from `xy=(x, y)` (where `x` is the left edge and `y` is the top edge of the first box).
- **Two-Pass Highlight Z-Order**: `BoxList.draw()` automatically renders default-styled boxes first and custom-styled boxes second so highlighted borders are never occluded by adjacent neutral boxes.

```drawlib fold-code 650px center file:smartarts_boxlist_alignment_geometry.png caption:"BoxList Directional Alignments (left, right, bottom, top) and Anchor Points"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.smartarts import BoxList
from drawlib.styles import Styles
from drawlib.text import text

setup(width=145, height=54)

bl = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
bl.add("1. First", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=8.0))
bl.add("2. Second", style=Styles.PrimaryNeutral)
bl.add("3. Third", style=Styles.SecondaryNeutral)

# 1. Top-Left Panel: align="left" (flows +x from bottom-left xy)
text((8.0, 47.5), "align='left' (Flows +x from xy)", style=Styles.BlackBold.patch(text_size=8.5, halign="left"))
bl.draw(xy=(8.0, 34.0), box_width=18.0, box_height=9.0, align="left")
line((8.0, 31.0), (58.0, 31.0), arrow_head="->", style=Styles.PrimaryBold)
circle((8.0, 34.0), radius=1.1, style=Styles.DangerFlat)
text((8.0, 28.0), "xy=(8, 34)", style=Styles.DangerBold.patch(text_size=7.5, halign="left"))

# 2. Bottom-Left Panel: align="right" (flows -x from bottom-right xy)
text((8.0, 21.5), "align='right' (Flows -x from xy)", style=Styles.BlackBold.patch(text_size=8.5, halign="left"))
bl.draw(xy=(62.0, 8.0), box_width=18.0, box_height=9.0, align="right")
line((62.0, 5.0), (12.0, 5.0), arrow_head="->", style=Styles.PrimaryBold)
circle((62.0, 8.0), radius=1.1, style=Styles.DangerFlat)
text((62.0, 2.2), "xy=(62, 8)", style=Styles.DangerBold.patch(text_size=7.5, halign="right"))

# 3. Middle Panel: align="bottom" (stacks +y upward from bottom-left xy)
text((85.0, 47.5), "align='bottom'\n(Stacks +y Up)", style=Styles.BlackBold.patch(text_size=8.5))
bl.draw(xy=(73.0, 8.0), box_width=24.0, box_height=9.5, align="bottom")
line((100.0, 8.0), (100.0, 35.0), arrow_head="->", style=Styles.PrimaryBold)
circle((73.0, 8.0), radius=1.1, style=Styles.DangerFlat)
text((73.0, 3.5), "xy=(73, 8)", style=Styles.DangerBold.patch(text_size=7.5, halign="left"))

# 4. Right Panel: align="top" (stacks -y downward from top-left xy)
text((123.0, 47.5), "align='top'\n(Stacks -y Down)", style=Styles.BlackBold.patch(text_size=8.5))
bl.draw(xy=(111.0, 36.5), box_width=24.0, box_height=9.5, align="top")
line((138.0, 36.5), (138.0, 9.5), arrow_head="->", style=Styles.PrimaryBold)
circle((111.0, 36.5), radius=1.1, style=Styles.DangerFlat)
text((111.0, 39.8), "xy=(111, 36.5)", style=Styles.DangerBold.patch(text_size=7.5, halign="left"))

save()
```

---

## 4. API Reference

### Constructor
```python
BoxList(
    *,
    style: Style,
    text_style: Style,
)
```

### Methods & Properties
- **`add(text: str, *, style: Style | None = None, text_style: Style | None = None, show: bool = True) -> BoxListItem`**:
  Appends a box item to the sequence and returns a mutable `BoxListItem` (`text`, `style`, `text_style`, `show`). Setting `show=False` hides that box while keeping the positions of all following boxes unchanged.
- **`boxlist.items -> list[BoxListItem]`**:
  Returns the list of all registered `BoxListItem` instances (`text: str`, `style: Style`, `text_style: Style`, `show: bool`), allowing deferred mutation before or between `draw()` calls.
- **`draw(xy: tuple[float, float], box_width: float, box_height: float, align: Literal["left", "right", "bottom", "top"] = "left", scale: float = 1.0) -> None`**:
  Renders the sequence of boxes anchored at `xy`, with optional proportional scaling via `scale`.

