# 4. Preset Styles & Themes

Instead of manually configuring RGB tuples or custom `Style(...)` models for every shape, Drawlib includes a comprehensive **Preset Styles** system accessed via `from drawlib.styles import Styles`. Every drawing function accepts a preset style such as `style=Styles.Primary` or `style=Styles.DangerFlat`.

## Official Style Themes

Drawlib ships with three curated preset themes:
- **`"default"`**: Balanced, clean palette designed for architectural blueprints and engineering diagrams.
- **`"google"`**: Modern, vibrant palette adhering to Google Cloud / Material design standards.
- **`"monochrome"`**: Crisp grayscale palette tailored for print books and academic publications.

## Semantic Roles & Style Matrix

Drawlib defines 6 core semantic roles across all themes:
- **`primary`**: Main application logic, core services, and primary actions.
- **`secondary`**: Data stores, caches, queues, and auxiliary services.
- **`accent`**: Entry points, clients, gateways, and focal callouts.
- **`muted`**: Group containers, boundaries, subnets, and structural lines.
- **`danger`**: Errors, alerts, security vulnerabilities, and failures.
- **`success`**: Healthy status, completed milestones, and verified checks.

Each semantic role (and color) provides 10 orthogonal variants:
`bordered` (default), `flat`, `outline`, `dashed`, `bold`, `light`, `outline_bold`, `outline_light`, `dashed_bold`, and `dashed_light`.

```python
from drawlib.styles import Styles

circle((20, 25), radius=10, style=Styles.Primary)        # Primary bordered
circle((45, 25), radius=10, style=Styles.SecondaryFlat) # Secondary flat
circle((70, 25), radius=10, style=Styles.DangerOutline) # Danger outline
```

```drawlib 620px center caption:"Figure 4.1: Core Semantic Styles Applied to Lines, Shapes, and Text"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=45)
line_y = 36
text_y = 9

items = [
    (12, "primary", Styles.Primary),
    (31, "secondary", Styles.Secondary),
    (50, "accent", Styles.Accent),
    (69, "muted", Styles.Muted),
    (88, "danger", Styles.Danger),
    (107, "success", Styles.Success),
]

for x, label, st in items:
    line((x - 7, line_y), (x + 7, line_y), style=st)
    circle((x, 23), radius=7, style=st)
    text((x, text_y), text=label, style=st, size=9)
```

## Typography & Custom Fonts

Drawlib includes universal CJK/Latin fonts (`Font`), sans-serif typography (`FontRoboto`), and code fonts (`FontMonoSpace`) via `drawlib.fonts`. You can also load custom font files using `FontFile`:

```drawlib 620px center caption:"Figure 4.2: Typography and Custom Font Files"
from drawlib.canvas import setup
from drawlib.fonts import Font, FontFile, FontMonoSpace, FontRoboto
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=45)

font_items = [
    (18, Font.SANSSERIF_REGULAR, "Default Font", "Font.SANSSERIF", Styles.PrimaryOutline, "Universal"),
    (46, FontRoboto.ROBOTO_REGULAR, "Roboto Sans", "FontRoboto", Styles.SecondaryOutline, "Clean Sans"),
    (74, FontMonoSpace.ROBOTO_MONO_REGULAR, "Monospace", "FontMonoSpace", Styles.AccentOutline, "Code / Logs"),
    (102, FontFile("_assets/avenger/regular.ttf"), "AVENGER", "FontFile", Styles.DangerOutline, "Custom Font"),
]

for x, font_obj, title, sub, st, desc in font_items:
    rectangle(xy=(x, 26), width=24, height=22, r=2, style=st)
    text(xy=(x, 28), text=title, style=Styles.Primary.patch(text_font=font_obj, text_size=10))
    text(xy=(x, 19), text=sub, style=Styles.Muted, size=8)
    text(xy=(x, 9), text=desc, style=Styles.Primary, size=9)
```

