=================================

# Official Theme: default


The `default` theme is the standard Drawlib theme.
We will explain style naming rule at this document.


# Colors


The `default` theme includes 5 colors.


```python 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors, ColorsThemeDefault
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import ShapeStyle, TextStyle

config(width=100, height=50)
start_x = 15
pad_x = 18
rect_y = 30
text1_y = 15
text2_y = 10

colors = [
    ("red", ColorsThemeDefault.Red),
    ("green", ColorsThemeDefault.Green),
    ("blue", ColorsThemeDefault.Blue),
    ("black", ColorsThemeDefault.Black),
    ("white", ColorsThemeDefault.White),
]

for i, (color_name, color) in enumerate(colors):
    x = start_x + pad_x * i
    lwidth = 0 if color_name != "white" else 1
    rectangle(
        (x, rect_y),
        width=12,
        height=12,
        style=ShapeStyle(fill_color=color, line_width=lwidth, line_color=Colors.Black),
    )
    text((x, text1_y), color_name)
    text((x, text2_y), str(color[:3]), style=TextStyle(text_size=14))

save()
```


    Theme `default` color chart

Here is a list of the colors. 
You can use `ColorsThemeDefault` to retrieve RGB codes by their names.

- `red`: RGB(239, 95, 95)
- `green`: RGB(79, 191, 79)
- `blue`: RGB(111, 111, 239)
- `black`: RGB(0, 0, 0)
- `white`: RGB(255, 255, 255)

Here is a color chart:




# Style Types


The default theme possesses these style types for all colors:

- default: Has both border and fill color
- `flat`: No border (actually has a white color)
- `solid`: Shape has an outline but no fill
- `dashed`: Dashed line, dashed outline

Each style type has variations of weight (line width, font weight) except for `flat`, which doesn't have a line:

- `light`: Half of default's line width. Font light.
- `default`: Font regular.
- `bold`: Double the default's line width. Font bold.

Remember, the style names follow this syntax: `<color>_<type>_<weight>`. 
If the color, type, and weight are default, they may not appear in the style name.

Let's take a look at a matrix with the blue color as an example:


```python 600px center
from drawlib.canvas import save
from drawlib.icons import icon_phosphor
from drawlib.lines import line
from drawlib.preset_styles import get_style
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import TextStyle

xs = [28, 48, 68, 88]
ys = [80, 50, 20]


def draw_header():
    x0 = 10
    y0 = 92

    text((x0, y0), "width \\ type", style="red")
    text((xs[0], y0), "(default)", style="red")
    text((xs[1], y0), "flat", style="red")
    text((xs[2], y0), "solid", style="red")
    text((xs[3], y0), "dashed", style="red")
    text((x0, ys[0]), "light", style="red")
    text((x0, ys[1]), "(default)", style="red")
    text((x0, ys[2]), "bold", style="red")


def draw_content():
    ts16 = get_style()
    ts16.text_size = 16

    for i, style_type in enumerate(["", "flat", "solid", "dashed"]):
        for j, style_width in enumerate(["light", "", "bold"]):
            if style_type == "flat":
                if style_width in ["light", "bold"]:
                    continue

            x = xs[i]
            y = ys[j]
            st = f"_{style_type}" if style_type != "" else ""
            sw = f"_{style_width}" if style_width != "" else ""
            style = f"blue{st}{sw}"

            if style_type in ["", "flat"]:
                circle((x - 4, y), 4, style=style)
                icon_phosphor.heart((x + 4.5, y - 0.5), width=8, style=style)
            else:
                circle((x, y), 4, style=style)

            if style_type != "flat":
                line((x - 7.5, y - 8), (x + 7.5, y - 8), style=style)
            if style_type == "":
                text((x, y - 12), style, style=style)
            else:
                text((x, y - 12), style, style=ts16)


draw_header()
draw_content()

save()
```


    Style type and width

As you can see, each style has these effects:

- `ShapeStyle`: Both style and width work.
- `IconStyle`: Line width can be controlled with width; flat style makes it fill.
- `LineStyle`: Width has an effect; flat style doesn't support line.
- `TextStyle`: Only the default type is supported; width affects font (light/regular/bold).

Although not shown in the example, other styles have these effects:

- `ImageStyle`: Similar to ShapeStyle, but the default has no line and fill.
- `ShapeTextStyle`: Similar to TextStyle.

You can check which style supports which style class in the style capability table below. 

Let's take a look at the blue example:



```text
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
 | class \ name   | blue | blue_light | blue_bold | blue_flat | blue_solid | blue_solid_light | blue_solid_bold | blue_dashed | blue_dashed_light | blue_dashed_bold |
 +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
 | IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
 | ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
 | LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
 | ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
 | ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
 | TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
 +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
```


As you can see, `flat` doesn't have a weight(light, bold). 
It can be used for only `IconStyle`, `ImageStyle`, and `ShapeStyle`. 

Here is a tip for remembering the rule:

- default type supports all classes.
- flat supports styles that can be filled.
- solid and dashed support styles that have a line.

Please remember, this naming rule is common in other official themes as well.



# Style Names


Here is a list of style names:




```python
from drawlib.types import IconStyle, ImageStyle, LineStyle, ShapeStyle, ShapeTextStyle, TextStyle



# +----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+
# | class \ name   |   | light | bold | flat | solid | solid_light | solid_bold | dashed | dashed_light | dashed_bold |
# +----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+
# | IconStyle      | x | x     | x    | x    |       |             |            |        |              |             |
# | ImageStyle     | x | x     | x    | x    | x     | x           | x          | x      | x            | x           |
# | LineStyle      | x | x     | x    |      | x     | x           | x          | x      | x            | x           |
# | ShapeStyle     | x | x     | x    | x    | x     | x           | x          | x      | x            | x           |
# | ShapeTextStyle | x | x     | x    |      |       |             |            |        |              |             |
# | TextStyle      | x | x     | x    |      |       |             |            |        |              |             |
# +----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+

# +----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
# | class \ name   | red | red_light | red_bold | red_flat | red_solid | red_solid_light | red_solid_bold | red_dashed | red_dashed_light | red_dashed_bold |
# +----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
# | IconStyle      | x   | x         | x        | x        |           |                 |                |            |                  |                 |
# | ImageStyle     | x   | x         | x        | x        | x         | x               | x              | x          | x                | x               |
# | LineStyle      | x   | x         | x        |          | x         | x               | x              | x          | x                | x               |
# | ShapeStyle     | x   | x         | x        | x        | x         | x               | x              | x          | x                | x               |
# | ShapeTextStyle | x   | x         | x        |          |           |                 |                |            |                  |                 |
# | TextStyle      | x   | x         | x        |          |           |                 |                |            |                  |                 |
# +----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | class \ name   | green | green_light | green_bold | green_flat | green_solid | green_solid_light | green_solid_bold | green_dashed | green_dashed_light | green_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | class \ name   | blue | blue_light | blue_bold | blue_flat | blue_solid | blue_solid_light | blue_solid_bold | blue_dashed | blue_dashed_light | blue_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | class \ name   | black | black_light | black_bold | black_flat | black_solid | black_solid_light | black_solid_bold | black_dashed | black_dashed_light | black_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | class \ name   | white | white_light | white_bold | white_flat | white_solid | white_solid_light | white_solid_bold | white_dashed | white_dashed_light | white_dashed_bold |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
# | IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
# | ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
# | ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
# | ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# | TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
# +----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
```

![official_default_1](official_default_images/1.png)





## color: default



![image_style.png](image_style.png)



## color: ``red``.



![image_style_red.png](image_style_red.png)



## color: ``green``.



![image_style_green.png](image_style_green.png)



## color: ``blue``.



![image_style_blue.png](image_style_blue.png)



## color: ``black``.



![image_style_black.png](image_style_black.png)



## color: ``white``.



![image_style_white.png](image_style_white.png)

