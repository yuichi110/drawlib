# Official Preset Styles: google


The `google` preset styles collection provides a modern palette based on Google Sheets and Material design standards.
It features rich, harmonious tints across multiple hues and full first-class support for semantic roles.


# Colors


The `google` preset styles provide neutral greys, 10 primary hue families with light and dark steps, and semantic mappings:

```drawlib 650px center caption:"Preset styles google color chart"
from drawlib.canvas import setup
from drawlib.preset_colors import GoogleColors
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style
from drawlib.styles import styles

setup(width=120, height=50)

semantic_items = [
    (12, "primary", GoogleColors.Primary),
    (31, "secondary", GoogleColors.Secondary),
    (50, "accent", GoogleColors.Accent),
    (69, "muted", GoogleColors.Muted),
    (88, "danger", GoogleColors.Danger),
    (107, "success", GoogleColors.Success),
]

for x, label, color in semantic_items:
    rectangle(
        (x, 32),
        width=16,
        height=14,
        style=Style(shape_fill_color=color, shape_line_width=1, shape_line_color=GoogleColors.DarkGray4),
    )
    text((x, 18), label, style=styles.bold)
    text((x, 10), str(color[:3]), style=styles.primary.patch(text_size=9))
```


# Semantic Roles

Drawlib maps the `google` theme colors to the 6 core semantic roles:

| Role | Theme Color | Intended Usage |
| :--- | :--- | :--- |
| **`primary`** | `CornflowerBlue` | Main services, application logic, core actions |
| **`secondary`** | `DarkCyan2` | Data stores, databases, caches, queues |
| **`accent`** | `Orange` | Clients, users, gateways, focal callouts |
| **`muted`** | `DarkGray3` | Group boundaries, VPC/subnets, containers |
| **`danger`** | `Red` | Alerts, errors, security risks, failures |
| **`success`** | `Green` | Completed milestones, verified status, healthy state |

Each role provides 10 orthogonal variants:
`bordered` (default), `flat`, `outline`, `dashed`, `bold`, `light`, `outline_bold`, `outline_light`, `dashed_bold`, and `dashed_light`.

```drawlib 650px center caption:"Semantic Roles in Action"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.preset_styles import google_styles
from drawlib.shapes import circle
from drawlib.text import text

setup(width=120, height=45)
line_y = 36
text_y = 9

items = [
    (12, "primary", google_styles.primary),
    (31, "secondary", google_styles.secondary),
    (50, "accent", google_styles.accent),
    (69, "muted", google_styles.muted),
    (88, "danger", google_styles.danger),
    (107, "success", google_styles.success),
]

for x, label, st in items:
    line((x - 7, line_y), (x + 7, line_y), style=st)
    circle((x, 23), radius=7, style=st)
    text((x, text_y), text=label, style=st, size=9)
```
