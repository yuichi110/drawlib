# Official Preset Styles: monochrome


The `monochrome` preset styles has colors between black and white.
There are many possibility that printed documents and published books has only black color.
These preset styles are useful for those kinds of situations.

The styling rules are the same as those for the `default` preset styles. 
If you are unfamiliar with these rules, please refer to the documentation for the default preset styles first, as this document does not provide detailed styling information.


# Colors


The `monochrome` preset styles possess 8 colors between black and white.


```drawlib 600px center caption:"Preset styles monochrome color chart"
from drawlib.canvas import setup
from drawlib.preset_colors import MonochromeColors
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style
from drawlib.styles import Colors, Styles

setup(width=100, height=45)
start_x = 8.5
pad_x = 12
rect_y = 28
text1_y = 15
text2_y = 9

colors = [
    ("black", MonochromeColors.Black),
    ("gray6", MonochromeColors.Gray6),
    ("gray5", MonochromeColors.Gray5),
    ("gray4", MonochromeColors.Gray4),
    ("gray3", MonochromeColors.Gray3),
    ("gray2", MonochromeColors.Gray2),
    ("gray1", MonochromeColors.Gray1),
    ("white", MonochromeColors.White),
]

for i, (color_name, color) in enumerate(colors):
    x = start_x + pad_x * i
    lwidth = 0 if color_name != "white" else 1
    rectangle(
        (x, rect_y),
        width=10,
        height=10,
        style=Style(shape_fill_color=color, shape_line_width=lwidth, shape_line_color=(0, 0, 0)),
    )
    text((x, text1_y), color_name, style=Styles.Bold.patch(text_size=12))
    text((x, text2_y), str(color[:3]), style=Styles.Primary.patch(text_size=8))
```

Here is a list of the colors. 
You can use `MonochromeColors` to retrieve RGB codes by their names (all colors strictly have $R = G = B$ for true neutral grayscale).

- `black`: RGB(0, 0, 0)
- `gray6`: RGB(35, 35, 35)
- `gray5`: RGB(75, 75, 75)
- `gray4`: RGB(130, 130, 130)
- `gray3`: RGB(180, 180, 180)
- `gray2`: RGB(220, 220, 220)
- `gray1`: RGB(245, 245, 245)
- `white`: RGB(255, 255, 255)
# Semantic Roles

Because grayscale documents lack color cues, **MonochromeStyles focuses on 4 core semantic roles** (excluding `danger` and `success`):

| Role | Monochrome Tone | Intended Usage |
| :--- | :--- | :--- |
| **`primary`** | `White` fill / `Black` border | Core application logic, main components |
| **`secondary`** | `Gray2` fill / `Gray6` border | Secondary components, data stores, background workers |
| **`accent`** | `Black` fill / `White` text | High-contrast focal callouts, active triggers, key gateways |
| **`muted`** | `Gray1` fill / `Gray4` dashed | Grouping containers, boundaries, subnets |

> **Note on Danger & Success**: Grayscale has no universal neutral equivalents for red and green without confusing value hierarchies. Therefore, `MonochromeStyles.danger` and `MonochromeStyles.success` are omitted (`None`). For alerts in monochrome, use `accent` or `muted_dashed` with explicit text labels or icons.

Each role provides 10 orthogonal variants (`bordered`, `bold`, `light`, `flat`, `outline`, `outline_bold`, `outline_light`, `dashed`, `dashed_bold`, `dashed_light`).

```drawlib 650px center caption:"Monochrome Semantic Roles in Action"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.preset_styles import MonochromeStyles
from drawlib.shapes import circle
from drawlib.text import text

setup(width=100, height=45)
line_y = 36
text_y = 9

items = [
    (15, "primary", MonochromeStyles.Primary),
    (38, "secondary", MonochromeStyles.Secondary),
    (61, "accent", MonochromeStyles.Accent),
    (84, "muted", MonochromeStyles.Muted),
]

for x, label, st in items:
    line((x - 7, line_y), (x + 7, line_y), style=st)
    circle((x, 23), radius=7, style=st)
    text((x, text_y), text=label, style=MonochromeStyles.Primary, size=9)
```


# Style Names


Here is a list of style names.


```python
from drawlib.types import Style




# +----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+
# | Item \ Name    |   | light | bold | flat | solid | solid_light | solid_bold | dashed | dashed_light | dashed_bold |
# +----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+
# | Icon           | x | x     | x    | x    |       |             |            |        |              |             |
# | Image          | x | x     | x    | x    | x     | x           | x          | x      | x            | x           |
# | Line           | x | x     | x    |      | x     | x           | x          | x      | x            | x           |
# | Shape          | x | x     | x    | x    | x     | x           | x          | x      | x            | x           |
# | ShapeText      | x | x     | x    |      |       |             |            |        |              |             |
# | Text           | x | x     | x    |      |       |             |            |        |              |             |
# +----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | black | black_light | black_bold | black_flat | black_solid | black_solid_light | black_solid_bold | black_dashed | black_dashed_light | black_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | gray6 | gray6_light | gray6_bold | gray6_flat | gray6_solid | gray6_solid_light | gray6_solid_bold | gray6_dashed | gray6_dashed_light | gray6_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | gray5 | gray5_light | gray5_bold | gray5_flat | gray5_solid | gray5_solid_light | gray5_solid_bold | gray5_dashed | gray5_dashed_light | gray5_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | gray4 | gray4_light | gray4_bold | gray4_flat | gray4_solid | gray4_solid_light | gray4_solid_bold | gray4_dashed | gray4_dashed_light | gray4_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | gray3 | gray3_light | gray3_bold | gray3_flat | gray3_solid | gray3_solid_light | gray3_solid_bold | gray3_dashed | gray3_dashed_light | gray3_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | gray2 | gray2_light | gray2_bold | gray2_flat | gray2_solid | gray2_solid_light | gray2_solid_bold | gray2_dashed | gray2_dashed_light | gray2_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | gray1 | gray1_light | gray1_bold | gray1_flat | gray1_solid | gray1_solid_light | gray1_solid_bold | gray1_dashed | gray1_dashed_light | gray1_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | white | white_light | white_bold | white_flat | white_solid | white_solid_light | white_solid_bold | white_dashed | white_dashed_light | white_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
