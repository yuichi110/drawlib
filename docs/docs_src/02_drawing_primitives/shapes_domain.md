# Cylinders, Faces & Callouts

Beyond standard geometric primitives, `drawlib.shapes` includes three expressive domain shapes for technical architecture and storytelling diagrams:
- **`cylinder`**: 3D shaded storage cylinders and multi-disk database stacks.
- **`face`**: Expressive user/actor personas and operational status faces.
- **`bubblespeech`**: Callout speech bubbles with directional pointer tails.

---

## 1. Overview: Combining Actors, Databases & Callouts

```drawlib fold-code 650px center file:shapes_domain_overview.png caption:"Combining Actor Faces, 3D Database Cylinders, and Speech Callouts"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import bubblespeech, cylinder, face
from drawlib.styles import Styles
from drawlib.text import text

setup(width=125, height=56)

# 1. User Actor Face
face((22, 26), radius=10, style=Styles.Neutral, mood="smile")
text((22, 11), "SRE Operator", style=Styles.DarkBold)

# 2. 3-Disk Primary Database Cylinder
cylinder(
    (64, 24),
    width=26,
    height=32,
    disks=3,
    style=Styles.PrimaryFlat,
    text="Primary\nCluster",
    text_style=Styles.WhiteBold,
)

# 3. Callout Speech Bubble pointing to the Database
bubblespeech(
    xy=(84, 26),
    width=35,
    height=18,
    tail_edge="left",
    tail_start_ratio=0.25,
    tail_end_ratio=0.55,
    tail_vertex_xy=(77, 28),
    style=Styles.SecondaryNeutral,
    text="3-disk replicated\nstorage volume",
)

line((34, 26), (49, 26), arrow_head="->", style=Styles.DarkBold)

save()
```

---

## 2. 3D Cylinders & Database Stacks (`cylinder`)

For relational databases, object storage buckets, disk arrays, and message queues, `cylinder` renders a 3D cylindrical container with an automatically lightened elliptical top cap:

```python
cylinder(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    style: Style,
    disks: int = 1,
    text: str = "",
    text_style: Style | None = None,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the cylinder. |
| `width` / `height` | `float` | *Required* | Total horizontal width and vertical height (`> 0`). |
| `disks` | `int` | `1` | Number of stacked disk tiers (`>= 1`). Values `2` or `3+` add curved divider seams. |
| `style` | `Style` | *Required* | Shape fill and stroke style. Set `style.patch(angle=-90)` for horizontal FIFO queues/pipes. |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | Centered text label and optional typography override. |

```drawlib show-code 620px center file:shapes_domain_cylinder.png caption:"Single Cylinder, 3-Disk Database Stack, and Horizontal Queue"
from drawlib.canvas import save, setup
from drawlib.shapes import cylinder
from drawlib.styles import Styles

setup(width=120, height=52)

# 1. Single-tier cache cylinder
cylinder((24, 26), width=26, height=34, style=Styles.Neutral, text="Cache")

# 2. 3-disk database stack (disks=3)
cylinder(
    (62, 26),
    width=28,
    height=36,
    disks=3,
    style=Styles.PrimaryFlat,
    text="Primary\nDB",
    text_style=Styles.WhiteBold,
)

# 3. Horizontal rotated cylinder (angle=-90 for message queue)
cylinder(
    (99, 26),
    width=20,
    height=32,
    style=Styles.SecondaryNeutral.patch(angle=-90),
    text="Queue",
)

save()
```

---

## 3. Expressive Actor & Status Faces (`face`)

For user personas, customer journey maps, and system health indicators, `face` renders a circular face with eyes, eyebrows, and five built-in facial expressions (`mood`):

```python
face(
    xy: tuple[float, float],
    radius: float,
    *,
    style: Style,
    mood: Literal["smile", "neutral", "sad", "angry", "surprised"] = "smile",
    text: str = "",
    text_style: Style | None = None,
)
```

- **`mood`**: Selects the mouth and eyebrow geometry (`"smile"`, `"neutral"`, `"sad"`, `"angry"`, or `"surprised"`).
- **Automatic Feature Contrast**: Eyes, eyebrows, and mouth automatically use `style.shape_line_color` on outlined cards, or high-contrast `text_color` / white on borderless flat styles (`Styles.PrimaryFlat`).

```drawlib show-code 640px center file:shapes_domain_face.png caption:"The Five Facial Moods in drawlib.shapes.face"
from drawlib.canvas import save, setup
from drawlib.shapes import face
from drawlib.styles import Styles
from drawlib.text import text

setup(width=125, height=46)

moods = [
    ("smile", Styles.PrimaryFlat),
    ("neutral", Styles.Neutral),
    ("surprised", Styles.SecondaryNeutral),
    ("sad", Styles.Neutral),
    ("angry", Styles.DangerNeutral),
]

for i, (mood_name, st) in enumerate(moods):
    cx = 17 + i * 22.5
    face((cx, 27), radius=9, style=st, mood=mood_name)
    text((cx, 11), f'"{mood_name}"', style=Styles.DarkBold.patch(text_size=9.5))

save()
```

---

## 4. Callout Speech Bubbles (`bubblespeech`)

`bubblespeech` draws a rectangular callout box with an integrated triangular pointer tail that originates from any of the four edges (`"left"`, `"top"`, `"right"`, `"bottom"`) and points to an exact target coordinate `tail_vertex_xy`:

```python
bubblespeech(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_edge: Literal["left", "top", "right", "bottom"],
    tail_start_ratio: float,
    tail_vertex_xy: tuple[float, float],
    tail_end_ratio: float,
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
)
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | **Bottom-left corner** `(x, y)` of the rectangular bubble body (always bottom-left anchored regardless of `style.halign`/`valign`). |
| `width` / `height` | `float` | Width and height of the rectangular bubble body (`> 0`). |
| `tail_edge` | `"left" \| "top" \| "right" \| "bottom"` | Which edge of the bubble body the pointer tail attaches to. |
| `tail_start_ratio` | `float` | Start position along `tail_edge` in `[0.0, 1.0]` (`< tail_end_ratio`). |
| `tail_end_ratio` | `float` | End position along `tail_edge` in `[0.0, 1.0]` (`> tail_start_ratio`). |
| `tail_vertex_xy` | `tuple[float, float]` | Absolute canvas coordinate `(x, y)` where the tip of the tail points. |
| `style` / `text` / `text_style` | `Style` / `str` / `Style \| None` | Bubble fill/stroke style and centered annotation text. Note: `bubblespeech` ignores `style.shape_r`, `style.angle`, and `style.halign`/`valign`. |

```drawlib show-code 640px center file:shapes_domain_bubblespeech.png caption:"Speech Bubble Callouts with Bottom-Left Anchor xy and Pointer Tail Vertex"
from drawlib.canvas import save, setup
from drawlib.shapes import bubblespeech, circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=56)

# Target nodes
circle((26, 14), radius=8.5, style=Styles.Neutral, text="Node A")
rectangle((102, 22), width=26, height=16, style=Styles.Neutral, text="Service B")

# 1. Callout with bottom tail pointing down to Node A
bubblespeech(
    xy=(8, 33),
    width=38,
    height=15,
    tail_edge="bottom",
    tail_start_ratio=0.35,
    tail_end_ratio=0.60,
    tail_vertex_xy=(26, 26),
    style=Styles.PrimaryFlat,
    text="Bottom Tail Callout\n(tail_edge='bottom')",
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)

# Coordinate indicators for bottom-left anchor xy and tail_vertex_xy
circle((8, 33), radius=1.1, style=Styles.DangerFlat)
text((4, 29.5), "xy=(8, 33)", style=Styles.DangerBold.patch(text_size=8.0, halign="left"))

circle((26, 26), radius=1.1, style=Styles.DangerFlat)
text((28.5, 26.5), "tail_vertex_xy=(26, 26)", style=Styles.DangerBold.patch(text_size=8.0, halign="left"))

# 2. Callout with right tail pointing to Service B
bubblespeech(
    xy=(64, 14),
    width=15,
    height=16,
    tail_edge="right",
    tail_start_ratio=0.30,
    tail_end_ratio=0.70,
    tail_vertex_xy=(88, 22),
    style=Styles.SecondaryNeutral,
    text="Note",
)

save()
```

> [!TIP]
> For embedding syntax-highlighted source code blocks alongside callouts, see **[SourceCode](../03_smartarts/source_code.md)**.
