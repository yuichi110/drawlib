=================================

# Official Theme: monochrome


Theme `monochrome` has colors between black and white.
There are many possibility that printed documents and published books has only black color.
This theme is useful for those kind of situation.

The styling rules are the same as those for the `default` theme. 
If you are unfamiliar with these rules, please refer to the documentation for the default theme first, as this document does not provide detailed styling information.


# Colors


Theme `monochrome` posses 7 colors between black and white.


```python 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors, ColorsThemeMonochrome
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import ShapeStyle, TextStyle

config(width=100, height=50)
start_x = 10
pad_x = 13
rect_y = 30
text1_y = 15
text2_y = 10

colors = [
    ("black", ColorsThemeMonochrome.Black),
    ("charcoal", ColorsThemeMonochrome.Charcoal),
    ("graphite", ColorsThemeMonochrome.Graphite),
    ("gray", ColorsThemeMonochrome.Gray),
    ("silver", ColorsThemeMonochrome.Silver),
    ("snow", ColorsThemeMonochrome.Snow),
    ("white", ColorsThemeMonochrome.White),
]

for i, (color_name, color) in enumerate(colors):
    x = start_x + pad_x * i
    lwidth = 0 if color_name != "white" else 1
    rectangle(
        (x, rect_y),
        width=10,
        height=10,
        style=ShapeStyle(fill_color=color, line_width=lwidth, line_color=Colors.Black),
    )
    text((x, text1_y), color_name, style=TextStyle(text_size=14))
    text((x, text2_y), str(color[:3]), style=TextStyle(text_size=12))

save()
```


    Theme `monochrome` color chart

Here is a list of the colors. 
You can use `ColorsThemeMonochrome` to retrieve RGB codes by their names.

- `black`: RGB(0, 0, 0)
- `charcoal`: RGB(39, 39, 39)
- `graphite`: RGB(63, 63, 63)
- `gray`: RGB(127, 127, 127)
- `silver`: RGB(191, 191, 191)
- `snow`: RGB(239, 239, 239)
- `white`: RGB(255, 255, 255)



# Style Names


Here is a list of style names.




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

# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | class \ name   | charcoal | charcoal_light | charcoal_bold | charcoal_flat | charcoal_solid | charcoal_solid_light | charcoal_solid_bold | charcoal_dashed | charcoal_dashed_light | charcoal_dashed_bold |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | IconStyle      | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
# | ImageStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | LineStyle      | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
# | ShapeStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | ShapeTextStyle | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# | TextStyle      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | class \ name   | graphite | graphite_light | graphite_bold | graphite_flat | graphite_solid | graphite_solid_light | graphite_solid_bold | graphite_dashed | graphite_dashed_light | graphite_dashed_bold |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
# | IconStyle      | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
# | ImageStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | LineStyle      | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
# | ShapeStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
# | ShapeTextStyle | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# | TextStyle      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
# +----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | class \ name   | gray | gray_light | gray_bold | gray_flat | gray_solid | gray_solid_light | gray_solid_bold | gray_dashed | gray_dashed_light | gray_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | class \ name   | silver | silver_light | silver_bold | silver_flat | silver_solid | silver_solid_light | silver_solid_bold | silver_dashed | silver_dashed_light | silver_dashed_bold |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
# | IconStyle      | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
# | ImageStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | LineStyle      | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
# | ShapeStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
# | ShapeTextStyle | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# | TextStyle      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
# +----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | class \ name   | snow | snow_light | snow_bold | snow_flat | snow_solid | snow_solid_light | snow_solid_bold | snow_dashed | snow_dashed_light | snow_dashed_bold |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
# | IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
# | ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
# | ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
# | ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# | TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
# +----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

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

![official_monochrome_1](official_monochrome_images/1.png)




## Color: default



![image_style_black.png](image_style_black.png)


    Theme Style default


## Color: ``black``



![image_style_black.png](image_style_black.png)


    Theme Style black


## Color: ``charcoal``



![image_style_charcoal.png](image_style_charcoal.png)


    Theme Style charcoal


## Color: ``graphite``



![image_style_graphite.png](image_style_graphite.png)


    Theme Style graphite


## Color: ``gray``



![image_style_gray.png](image_style_gray.png)


    Theme Style gray


## Color: ``silver``



![image_style_silver.png](image_style_silver.png)


    Theme Style silver


## Color: ``snow``



![image_style_snow.png](image_style_snow.png)


    Theme Style snow


## Color: ``white``



![image_style_white.png](image_style_white.png)


    Theme Style white