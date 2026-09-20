=============================

# Official Theme: essentials


The `essentials` theme comprises 25 basic colors. 
We recommend this theme for advanced users as it includes all aspects of the `default` and `monochrome` themes. 
If you are looking to customize our themes extensively, essentials serves as an excellent base.

The styling rules are the same as those for the `default` theme. 
If you are unfamiliar with these rules, please refer to the documentation for the default theme first, as this document does not provide detailed styling information.


# Colors


The `essentials` theme includes 25 colors, encompassing all other themes' colors.


```python 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors, ColorsThemeEssentials
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=100)
start_x = 12
pad_x = 19


def draw_horizon(colors: list[tuple[str, tuple[int, int, int]]], y):
    rect_y = y
    text1_y = y - 6
    text2_y = y - 9

    for i, (color_name, color) in enumerate(colors):
        x = start_x + pad_x * i
        lwidth = 0 if color_name not in ["white", "ivory"] else 1
        rectangle(
            (x, rect_y),
            width=12,
            height=6,
            style=Style(fill_color=color, line_width=lwidth, line_color=Colors.Black),
        )
        text((x, text1_y), color_name)
        text((x, text2_y), str(color[:3]), style=Style(text_size=14))


draw_horizon([
    ("red", ColorsThemeEssentials.Red),
    ("lightred", ColorsThemeEssentials.LightRed),
    ("pink", ColorsThemeEssentials.Pink),
    ("brown", ColorsThemeEssentials.Brown),
    ("orange", ColorsThemeEssentials.Orange),
], 90)
draw_horizon([
    ("green", ColorsThemeEssentials.Green),
    ("lightgreen", ColorsThemeEssentials.LightGreen),
    ("greenyellow", ColorsThemeEssentials.GreenYellow),
    ("teal", ColorsThemeEssentials.Teal),
    ("olive", ColorsThemeEssentials.Olive),
], 70)
draw_horizon([
    ("blue", ColorsThemeEssentials.Blue),
    ("lightblue", ColorsThemeEssentials.LightBlue),
    ("aqua", ColorsThemeEssentials.Aqua),
    ("navy", ColorsThemeEssentials.Navy),
    ("steel", ColorsThemeEssentials.Steel),
], 50)
draw_horizon([
    ("yellow", ColorsThemeEssentials.Yellow),
    ("purple", ColorsThemeEssentials.Purple),
    ("ivory", ColorsThemeEssentials.Ivory),
    ("black", ColorsThemeEssentials.Black),
    ("charcoal", ColorsThemeEssentials.Charcoal),
], 32.5)
draw_horizon([
    ("graphite", ColorsThemeEssentials.Graphite),
    ("gray", ColorsThemeEssentials.Gray),
    ("silver", ColorsThemeEssentials.Silver),
    ("snow", ColorsThemeEssentials.Snow),
    ("white", ColorsThemeEssentials.White),
], 15)
save()
```


    Theme `essentials` color chart

Here is a list of the colors. 
You can use `ColorsThemeEssentials` to retrieve RGB codes by their names.

- `red`: RGB(255, 23, 23)
- `lightred`: RGB(239, 95, 95). Same to `red` of default theme.
- `pink`: RGB(239, 63, 239)
- `brown`: RGB(159, 31, 31)
- `orange`: RGB(255, 95, 31)
- `green`: RGB(15, 127, 15)
- `lightgreen`: RGB(79, 191, 79). Same to `green` of default theme.
- `greenyellow`: RGB(127, 207, 31)
- `teal`: RGB(15, 127, 127)
- `olive`: RGB(127, 127, 31)
- `blue`: RGB(31, 31, 255)
- `lightblue`: RGB(111, 111, 239). Default color of shape fill. Same to `blue` of default theme.
- `aqua`: RGB(47, 239, 239)
- `navy`: RGB(15, 15, 127)
- `steel`: RGB(96, 96, 143)
- `yellow`: RGB(239, 239, 31)
- `purple`: RGB(127, 31, 127)
- `ivory`: RGB(239, 239, 207)
- `black`: RGB(0, 0, 0)
- `charcoal`: RGB(39, 39, 39). Default color of line and test
- `graphite`: RGB(63, 63, 63)
- `gray`: RGB(127, 127, 127)
- `silver`: RGB(191, 191, 191)
- `snow`: RGB(239, 239, 239)
- `white`: RGB(255, 255, 255)


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

# +----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
# | Item \ Name    | red | red_light | red_bold | red_flat | red_solid | red_solid_light | red_solid_bold | red_dashed | red_dashed_light | red_dashed_bold |
# +----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
# | Icon           | x   | x         | x        | x        |           |                 |                |            |                  |                 |
# | Image          | x   | x         | x        | x        | x         | x               | x              | x          | x                | x               |
# | Line           | x   | x         | x        |          | x         | x               | x              | x          | x                | x               |
# | Shape          | x   | x         | x        | x        | x         | x               | x              | x          | x                | x               |
# | ShapeText      | x   | x         | x        |          |           |                 |                |            |                  |                 |
# | Text           | x   | x         | x        |          |           |                 |                |            |                  |                 |
# +----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+

# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | Item \ Name    | lightred | lightred_light | lightred_bold | lightred_flat | lightred_solid | lightred_solid_light | lightred_solid_bold | lightred_dashed | lightred_dashed_light | lightred_dashed_bold |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | Icon           | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
# | Image          | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | Line           | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
# | Shape          | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | ShapeText      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# | Text           | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Item \ Name    | pink | pink_light | pink_bold | pink_flat | pink_solid | pink_solid_light | pink_solid_bold | pink_dashed | pink_dashed_light | pink_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Icon           | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | Image          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | Line           | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | Shape          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeText      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | Text           | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | brown | brown_light | brown_bold | brown_flat | brown_solid | brown_solid_light | brown_solid_bold | brown_dashed | brown_dashed_light | brown_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Item \ Name    | orange | orange_light | orange_bold | orange_flat | orange_solid | orange_solid_light | orange_solid_bold | orange_dashed | orange_dashed_light | orange_dashed_bold |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Icon           | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
# | Image          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | Line           | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
# | Shape          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | ShapeText      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# | Text           | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | green | green_light | green_bold | green_flat | green_solid | green_solid_light | green_solid_bold | green_dashed | green_dashed_light | green_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+------------+------------------+-----------------+-----------------+------------------+------------------------+-----------------------+-------------------+-------------------------+------------------------+
# | Item \ Name    | lightgreen | lightgreen_light | lightgreen_bold | lightgreen_flat | lightgreen_solid | lightgreen_solid_light | lightgreen_solid_bold | lightgreen_dashed | lightgreen_dashed_light | lightgreen_dashed_bold |
# +----------------+------------+------------------+-----------------+-----------------+------------------+------------------------+-----------------------+-------------------+-------------------------+------------------------+
# | Icon           | x          | x                | x               | x               |                  |                        |                       |                   |                         |                        |
# | Image          | x          | x                | x               | x               | x                | x                      | x                     | x                 | x                       | x                      |
# | Line           | x          | x                | x               |                 | x                | x                      | x                     | x                 | x                       | x                      |
# | Shape          | x          | x                | x               | x               | x                | x                      | x                     | x                 | x                       | x                      |
# | ShapeText      | x          | x                | x               |                 |                  |                        |                       |                   |                         |                        |
# | Text           | x          | x                | x               |                 |                  |                        |                       |                   |                         |                        |
# +----------------+------------+------------------+-----------------+-----------------+------------------+------------------------+-----------------------+-------------------+-------------------------+------------------------+

# +----------------+-------------+-------------------+------------------+------------------+-------------------+-------------------------+------------------------+--------------------+--------------------------+-------------------------+
# | Item \ Name    | greenyellow | greenyellow_light | greenyellow_bold | greenyellow_flat | greenyellow_solid | greenyellow_solid_light | greenyellow_solid_bold | greenyellow_dashed | greenyellow_dashed_light | greenyellow_dashed_bold |
# +----------------+-------------+-------------------+------------------+------------------+-------------------+-------------------------+------------------------+--------------------+--------------------------+-------------------------+
# | Icon           | x           | x                 | x                | x                |                   |                         |                        |                    |                          |                         |
# | Image          | x           | x                 | x                | x                | x                 | x                       | x                      | x                  | x                        | x                       |
# | Line           | x           | x                 | x                |                  | x                 | x                       | x                      | x                  | x                        | x                       |
# | Shape          | x           | x                 | x                | x                | x                 | x                       | x                      | x                  | x                        | x                       |
# | ShapeText      | x           | x                 | x                |                  |                   |                         |                        |                    |                          |                         |
# | Text           | x           | x                 | x                |                  |                   |                         |                        |                    |                          |                         |
# +----------------+-------------+-------------------+------------------+------------------+-------------------+-------------------------+------------------------+--------------------+--------------------------+-------------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Item \ Name    | teal | teal_light | teal_bold | teal_flat | teal_solid | teal_solid_light | teal_solid_bold | teal_dashed | teal_dashed_light | teal_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Icon           | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | Image          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | Line           | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | Shape          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeText      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | Text           | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | olive | olive_light | olive_bold | olive_flat | olive_solid | olive_solid_light | olive_solid_bold | olive_dashed | olive_dashed_light | olive_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Item \ Name    | blue | blue_light | blue_bold | blue_flat | blue_solid | blue_solid_light | blue_solid_bold | blue_dashed | blue_dashed_light | blue_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Icon           | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | Image          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | Line           | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | Shape          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeText      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | Text           | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+-----------+-----------------+----------------+----------------+-----------------+-----------------------+----------------------+------------------+------------------------+-----------------------+
# | Item \ Name    | lightblue | lightblue_light | lightblue_bold | lightblue_flat | lightblue_solid | lightblue_solid_light | lightblue_solid_bold | lightblue_dashed | lightblue_dashed_light | lightblue_dashed_bold |
# +----------------+-----------+-----------------+----------------+----------------+-----------------+-----------------------+----------------------+------------------+------------------------+-----------------------+
# | Icon           | x         | x               | x              | x              |                 |                       |                      |                  |                        |                       |
# | Image          | x         | x               | x              | x              | x               | x                     | x                    | x                | x                      | x                     |
# | Line           | x         | x               | x              |                | x               | x                     | x                    | x                | x                      | x                     |
# | Shape          | x         | x               | x              | x              | x               | x                     | x                    | x                | x                      | x                     |
# | ShapeText      | x         | x               | x              |                |                 |                       |                      |                  |                        |                       |
# | Text           | x         | x               | x              |                |                 |                       |                      |                  |                        |                       |
# +----------------+-----------+-----------------+----------------+----------------+-----------------+-----------------------+----------------------+------------------+------------------------+-----------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Item \ Name    | aqua | aqua_light | aqua_bold | aqua_flat | aqua_solid | aqua_solid_light | aqua_solid_bold | aqua_dashed | aqua_dashed_light | aqua_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Icon           | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | Image          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | Line           | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | Shape          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeText      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | Text           | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Item \ Name    | navy | navy_light | navy_bold | navy_flat | navy_solid | navy_solid_light | navy_solid_bold | navy_dashed | navy_dashed_light | navy_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Icon           | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | Image          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | Line           | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | Shape          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeText      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | Text           | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | steel | steel_light | steel_bold | steel_flat | steel_solid | steel_solid_light | steel_solid_bold | steel_dashed | steel_dashed_light | steel_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Item \ Name    | yellow | yellow_light | yellow_bold | yellow_flat | yellow_solid | yellow_solid_light | yellow_solid_bold | yellow_dashed | yellow_dashed_light | yellow_dashed_bold |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Icon           | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
# | Image          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | Line           | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
# | Shape          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | ShapeText      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# | Text           | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Item \ Name    | purple | purple_light | purple_bold | purple_flat | purple_solid | purple_solid_light | purple_solid_bold | purple_dashed | purple_dashed_light | purple_dashed_bold |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Icon           | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
# | Image          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | Line           | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
# | Shape          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | ShapeText      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# | Text           | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Item \ Name    | ivory | ivory_light | ivory_bold | ivory_flat | ivory_solid | ivory_solid_light | ivory_solid_bold | ivory_dashed | ivory_dashed_light | ivory_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | Icon           | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | Image          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | Line           | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | Shape          | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeText      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | Text           | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

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

# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | Item \ Name    | charcoal | charcoal_light | charcoal_bold | charcoal_flat | charcoal_solid | charcoal_solid_light | charcoal_solid_bold | charcoal_dashed | charcoal_dashed_light | charcoal_dashed_bold |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | Icon           | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
# | Image          | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | Line           | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
# | Shape          | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | ShapeText      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# | Text           | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | Item \ Name    | graphite | graphite_light | graphite_bold | graphite_flat | graphite_solid | graphite_solid_light | graphite_solid_bold | graphite_dashed | graphite_dashed_light | graphite_dashed_bold |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | Icon           | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
# | Image          | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | Line           | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
# | Shape          | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | ShapeText      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# | Text           | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Item \ Name    | gray | gray_light | gray_bold | gray_flat | gray_solid | gray_solid_light | gray_solid_bold | gray_dashed | gray_dashed_light | gray_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Icon           | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | Image          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | Line           | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | Shape          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeText      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | Text           | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Item \ Name    | silver | silver_light | silver_bold | silver_flat | silver_solid | silver_solid_light | silver_solid_bold | silver_dashed | silver_dashed_light | silver_dashed_bold |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | Icon           | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
# | Image          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | Line           | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
# | Shape          | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | ShapeText      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# | Text           | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Item \ Name    | snow | snow_light | snow_bold | snow_flat | snow_solid | snow_solid_light | snow_solid_bold | snow_dashed | snow_dashed_light | snow_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | Icon           | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | Image          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | Line           | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | Shape          | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeText      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | Text           | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

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

![official_essentials_1](official_essentials_images/1.png)



---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
