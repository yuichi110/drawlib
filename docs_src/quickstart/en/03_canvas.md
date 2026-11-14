# 3. Cartesian Canvas & Coordinate Anchors

Every Drawlib illustration is composed on a deterministic **2D Cartesian coordinate plane** where the origin `(0, 0)` sits strictly at the **bottom-left corner**, `X` increases horizontally to the right (`0 -> width`), and `Y` increases vertically upward (`0 -> height`).

Mastering three foundational rules—**bottom-left Cartesian axes**, the **`720pt` typography formula**, and **component coordinate anchors**—lets engineers and AI coding agents place shapes, icons, charts, and SmartArts with single-shot precision and zero visual collisions.

```drawlib align=center code=fold file=cartesian_canvas.png caption="Figure 3.1: Drawlib Bottom-Left (0, 0) Cartesian Canvas, Safe Margin Zone, and Plotted Coordinates"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=148, height=72)

# Illustrated virtual canvas frame [26..126] x [16..64] and 6-unit inset safe margin zone
rectangle((76.0, 40.0), width=100.0, height=48.0, style=Styles.Neutral.patch(shape_line_width=1.2))
rectangle(
    (76.0, 40.0),
    width=88.0,
    height=36.0,
    style=Styles.PrimaryDashed.patch(shape_fill_color=Colors.White, shape_r=1.4),
)
text(
    (34.5, 55.2),
    "Safe Margin Zone (>= 4–6u inset)",
    style=Styles.MutedBold.patch(text_size=10.2, halign="left", valign="top"),
)

# Subtle center crosshair guides (drawn behind center badge)
line((32.0, 40.0), (120.0, 40.0), style=Styles.MutedDotted)
line((76.0, 22.0), (76.0, 50.5), style=Styles.MutedDotted)

# Cartesian X-axis (rightward) and Y-axis (upward)
line((26.0, 16.0), (136.0, 16.0), arrow_head="->", style=Styles.DarkBold)
text((138.0, 16.0), "+X", style=Styles.DarkBold.patch(text_size=11.5, halign="left", valign="center"))
text((76.0, 7.2), "X-Axis: Increases Rightward (0 -> width)", style=Styles.DarkBold.patch(text_size=11.0))

line((26.0, 16.0), (26.0, 67.5), arrow_head="->", style=Styles.DarkBold)
text((23.2, 66.8), "+Y", style=Styles.DarkBold.patch(text_size=11.5, halign="right", valign="center"))
text(
    (9.5, 40.0),
    "Y-Axis: Increases Upward (0 -> height)",
    style=Styles.DarkBold.patch(text_size=11.0, angle=90),
)

# Corner markers with offset labels (zero overlap with axes or borders)
circle((26.0, 16.0), radius=1.25, style=Styles.PrimaryFlat)
text((24.0, 12.2), "Origin (0, 0)", style=Styles.DarkBold.patch(text_size=10.8, halign="right", valign="top"))

circle((126.0, 16.0), radius=0.95, style=Styles.DarkFlat)
text((126.0, 12.2), "(W, 0)", style=Styles.DarkBold.patch(text_size=10.5, halign="center", valign="top"))

circle((26.0, 64.0), radius=0.95, style=Styles.DarkFlat)
text((29.2, 64.8), "(0, H)", style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="bottom"))

circle((126.0, 64.0), radius=0.95, style=Styles.DarkFlat)
text((128.5, 64.0), "(W, H)", style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="center"))

# Focal center anchor badge and two sample plotted points
rectangle(
    (76.0, 40.0),
    width=34.0,
    height=9.8,
    style=Styles.PrimaryFlat.patch(shape_r=2.0),
    text="Center (W/2, H/2)",
    text_style=Styles.WhiteBold.patch(text_size=10.8),
)

circle((45.0, 28.0), radius=1.05, style=Styles.DarkFlat)
text((47.6, 28.0), "P1 (25, 20)", style=Styles.DarkBold.patch(text_size=10.4, halign="left", valign="center"))

circle((108.0, 50.5), radius=1.05, style=Styles.DarkFlat)
text((105.4, 50.5), "P2 (95, 48)", style=Styles.DarkBold.patch(text_size=10.4, halign="right", valign="center"))

save()
```

---

## 3.1 Cartesian Coordinates vs. Browser DOM / SVG

Frontend engineers accustomed to HTML5 `<canvas>`, CSS absolute positioning, or raw `<svg>` must note one crucial geometric distinction so `Y` coordinates are never inverted:

| Coordinate Property | **Drawlib Cartesian Canvas** | Browser DOM / HTML `<svg>` |
| :--- | :--- | :--- |
| **Origin `(0, 0)`** | **Bottom-Left corner** | Top-Left corner |
| **Horizontal `+X` Direction** | Left to Right (`0 -> width`) | Left to Right (`0 -> width`) |
| **Vertical `+Y` Direction** | **Bottom to Top (`0 -> height`)** | Top to Bottom (`0 -> height`) |
| **Top Title Placement** | High `Y` near `height - 6` | Small `Y` near `16px` |
| **Safe Outer Margin** | Keep content inside `[5, W - 5]` × `[5, H - 5]` | CSS padding / viewBox |

Because `+Y` points upward just like mathematical plots and architectural elevation drawings, **higher `Y` always means visually higher on the page**—page titles sit near `height - 6`, central architecture tiers sit around `height / 2`, and footnotes or legends sit near `y = 6..10`. Always maintain **`4–6` virtual units of clear outer margin** around all four canvas edges so borders, rounded corners, and drop shadows never clip.

---

## 3.2 Canvas Lifecycle: `setup()`, Drawing Calls, and `save()`

Every Drawlib script and embedded Markdown block follows a clean three-step execution lifecycle:

1. **`setup(width=..., height=..., dpi=..., background_color=..., grid=...)`**: Initializes canvas geometry in **abstract virtual units** (`width` and `height`, defaulting to `100 × 100`) and configures raster output density via `dpi` (default `100`). Because coordinates use resolution-independent virtual units, increasing `dpi=100` to `dpi=200` doubles output pixel dimensions (`1400 × 520 px` -> `2800 × 1040 px`) without changing a single `(x, y)` number. Project-wide theme palettes and fonts (`from drawlib.styles import Colors, Styles`) load automatically from `styles.py` (`style = "google"` in `drawlib.toml`).
2. **Declarative Drawing Calls**: Invoke Z-ordered primitives, icons, SmartArts, charts, or domain diagrams from back (containers and connector lines) to front (service cards and callouts).
3. **`save()`**: Commits and renders the canvas. Always end **every standalone `.py` script and every embedded ```` ```drawlib ```` Markdown block** with `save()`—in standalone scripts `save()` flushes the image file to disk (`<script_name>.png` or an explicit path), and in Markdown blocks ending with `save()` ensures every snippet is 100% self-contained and directly runnable outside the document builder. *(If a single `.py` script generates multiple sequential files, call `clear()` after each `save(...)` before the next `setup(...)`.)*

```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# 1. Abstract 136x50 virtual units at crisp 150 DPI (2040x750 output pixels)
setup(width=136, height=50, dpi=150)

# 2. Back-to-front drawing calls (neutral baseline + 1 focal PrimaryFlat node)
line((44, 25), (54, 25), arrow_head="->", style=Styles.DarkBold)
line((82, 25), (92, 25), arrow_head="->", style=Styles.DarkBold)

rectangle((26, 25), width=36, height=18, style=Styles.Neutral, text="Client App")
rectangle(
    (68, 25),
    width=28,
    height=18,
    style=Styles.PrimaryFlat,
    text="API Core",
    text_style=Styles.WhiteBold,
)
rectangle((110, 25), width=36, height=18, style=Styles.SecondaryNeutral, text="PostgreSQL")

# 3. Mandatory lifecycle commit
save()
```

---

## 3.3 The `720pt` Typography Formula & Canvas Sizing

Internally, Drawlib normalizes figure typography against a fixed **`720pt` reference width**. Regardless of `dpi`, the visual font size of any label when an image is displayed at `Display Width` pixels in HTML, PDF, or slides is governed by one exact formula:

```text
Rendered Font Size (px) = text_size × (Display Width (px) / 720)
```

Understanding this linear scaling relationship prevents microscopic, unreadable diagram labels:

- **Keep `text_size >= 10.0` Everywhere**: In HTML and A4 PDF documentation (`doc`, `site`, `catalog`), content columns typically span `~820px–900px` (`Display Width / 720 ≈ 1.15–1.25`). Setting **`text_size = 10.5–12.0`** for body/node labels and **`12.0–14.0`** for headers produces crisp `~12px–17px` lettering that matches surrounding `16px` HTML prose. Never drop below `text_size = 10.0` (with `9.5` strictly reserved as an absolute floor for minor chart ticks).
- **Ideal Embedded Figure Width (`width=120..150`)**: Calling `setup(width=140, height=60)` (or `width=120..150`) gives clean `10`-unit grid arithmetic for multi-column diagrams while keeping aspect ratios compact above the fold.
- **Never Cap Markdown Fences with Narrow Pixel Widths**: Never add `width=500px` or `width=600px` to ```` ```drawlib ```` fences—shrinking `Display Width` to `500px` reduces `Display Width / 720` to `0.69`, shrinking every label inside the figure by over `30%`.

| Target Context | Typical `setup(width, height)` | Display Width | Recommended `text_size` | Resulting Visual Size |
| :--- | :--- | :--- | :--- | :--- |
| **Doc / Site Hero & Flow** | `140 × 60` (`120..150` wide) | `~840px` | **`10.5–12.0`** (headers `12.0–14.0`) | **`~12.5px–16.5px`** (matches `16px` prose) |
| **Dense Multi-Tier Schema** | `148 × 72` | `~840px` | **`10.0–11.5`** (headers `12.0–13.5`) | **`~11.7px–15.8px`** |
| **16:9 Full-Width Slide** | `160 × 80` | `~1760px` | **`11.0–13.0`** (headers `14.0–16.0`) | **`~27px–39px`** (matches `26px` slide text) |

---

## 3.4 Text Alignment & Component Coordinate Anchors

When placing standalone labels with `text(xy, label, style=...)`, the anchor point `xy` is controlled via `.patch(halign=..., valign=...)` on preset `Styles.*` tokens (never construct raw `Style(...)` instances directly):

- **`halign="left" | "center" | "right"`**: Controls whether text extends rightward from `x` (`"left"`), centers around `x` (`"center"`, default), or ends flush against `x` (`"right"`).
- **`valign="bottom" | "center" | "top"`**: Controls whether text sits above `y` (`"bottom"`), centers vertically on `y` (`"center"`, default), or hangs downward from `y` (`"top"`).

Beyond `text()`, Drawlib components follow **three predictable coordinate anchor conventions** summarized below:

```drawlib align=center code=fold file=text_alignment_anchors.png caption="Figure 3.2: Text Alignment (halign / valign) and the Three Component Anchor Conventions"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=68)

# Left Panel: halign & valign anchor demonstration (zero dot-to-text overlap)
p_left = Panel(
    "Text Alignment (halign & valign)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    icon=phosphor.text_t,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p_left.draw((5.0, 5.0), width=66.0, height=58.0)

# Row 1: halign="left", valign="center"
rectangle((38.0, 45.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
line((13.0, 41.2), (13.0, 48.8), style=Styles.MutedDashed)
circle((13.0, 45.0), radius=1.05, style=Styles.PrimaryFlat)
text(
    (16.0, 45.0),
    'halign="left", valign="center"',
    style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="center"),
)

# Row 2: halign="center", valign="bottom"
rectangle((38.0, 30.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
line((16.0, 26.5), (60.0, 26.5), style=Styles.MutedDashed)
circle((38.0, 26.5), radius=1.05, style=Styles.PrimaryFlat)
text(
    (38.0, 28.5),
    'halign="center", valign="bottom"',
    style=Styles.DarkBold.patch(text_size=10.5, halign="center", valign="bottom"),
)

# Row 3: halign="right", valign="top"
rectangle((38.0, 15.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
line((22.0, 18.5), (63.0, 18.5), style=Styles.MutedDashed)
circle((63.0, 18.5), radius=1.05, style=Styles.PrimaryFlat)
text(
    (60.2, 16.5),
    'halign="right", valign="top"',
    style=Styles.DarkBold.patch(text_size=10.5, halign="right", valign="top"),
)

# Right Panel: Component Anchor Mental Model
p_right = Panel(
    "Component Anchor Mental Model",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    icon=phosphor.crosshair,
    icon_style=Styles.DarkBold,
    header_height=8.5,
)
p_right.draw((77.0, 5.0), width=66.0, height=58.0)

# Archetype 1: Center (cx, cy) — 1 Focal PrimaryFlat shape
rectangle((110.0, 45.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
rectangle((90.5, 45.0), width=14.5, height=7.8, style=Styles.PrimaryFlat.patch(shape_r=1.2))
circle((90.5, 45.0), radius=1.05, style=Styles.WhiteFlat)
text((100.8, 47.0), "Center (cx, cy)", style=Styles.DarkBold.patch(text_size=10.8, halign="left"))
text((100.8, 42.6), "Shapes, Icons, Images, text()", style=Styles.Dark.patch(text_size=10.0, halign="left"))

# Archetype 2: Bottom-Left (x0, y0)
rectangle((110.0, 30.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
rectangle((90.5, 30.0), width=14.5, height=7.8, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
circle((83.25, 26.1), radius=1.05, style=Styles.PrimaryFlat)
text((100.8, 32.0), "Bottom-Left (x0, y0)", style=Styles.DarkBold.patch(text_size=10.8, halign="left"))
text((100.8, 27.6), "Charts, Diagrams, SmartArts", style=Styles.Dark.patch(text_size=10.0, halign="left"))

# Archetype 3: Top-Left (x0, y_top)
rectangle((110.0, 15.0), width=59.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
rectangle((90.5, 15.0), width=14.5, height=7.8, style=Styles.SecondaryNeutral.patch(shape_r=1.2))
circle((83.25, 18.9), radius=1.05, style=Styles.PrimaryFlat)
text((100.8, 17.0), "Top-Left (x0, y_top)", style=Styles.DarkBold.patch(text_size=10.8, halign="left"))
text((100.8, 12.6), "Table, TreeNode, SourceCode", style=Styles.Dark.patch(text_size=10.0, halign="left"))

save()
```

Keep this anchor mental model handy whenever combining primitives with composite SmartArts or Charts:

- **Center `(cx, cy)`**: Used by all geometric primitives (`shapes.*`), `text()`, icons (`phosphor.*`, `gcp.*`, `aws.*`, `azure.*`), `images.image()`, `MindMapNode`, `Cycle`, and individual `Node` items added inside `ArchitectureDiagram`. The element spans `[cx - w/2, cx + w/2]` horizontally and `[cy - h/2, cy + h/2]` vertically.
- **Bottom-Left `(x0, y0)`**: Used by all `charts.*`, `diagrams.*` (`d.draw(xy=(x0, y0))` and `NodeGroup(..., xy=(x0, y0))`), and most `smartarts.*` (`Panel`, `CardList`, `ChevronProcess`, `GridLayout`, `KpiCards`, `BoxList`, `Pyramid`, `Roadmap`, `GeoMap`, `*Calendar`). To center a component of width `w` on a canvas of width `W`, pass `x0 = (W - w) / 2` (never `W / 2`).
- **Top-Left `(x0, y_top)`**: Used by top-down document SmartArts—`Table`, `TreeNode`, `BulletPoints`, and `SourceCode`—so multi-row tables, directory trees, and code listings naturally expand downward from a fixed header line `y_top`.
