# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: E501

from drawlib.apis import *

IMAGE_FILE = "../../assets/image.png"
OUTPUT_DIR = "../../../output_tests/v0_1/theme/monochrome/"


def test_icon_text_lightbold():
    dtheme.apply_official_theme("monochrome")

    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80

    # default
    icon_phosphor.airplane((x1, y1), width=20, style="light")
    icon_phosphor.airplane((x2, y1), width=20)
    icon_phosphor.airplane((x3, y1), width=20, style="bold")

    text((x1, y2), "Hello Drawlib1", style="light")
    text((x2, y2), "Hello Drawlib1")
    text((x3, y2), "Hello Drawlib1", style="bold")

    icon_phosphor.airplane((x1, y3), width=20, style="flat")
    icon_phosphor.airplane((x2, y3), width=20, style="black_flat")
    icon_phosphor.airplane((x3, y3), width=20, style="gray_flat")

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    # recover to default theme


def test_shape_lightbold():
    dtheme.apply_official_theme("monochrome")

    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80
    radius = 10

    # default
    circle((x1, y1), radius, style="light", text="drawlib", textstyle="light")
    circle((x2, y1), radius, text="drawlib")
    circle((x3, y1), radius, style="bold", text="drawlib", textstyle="bold")

    # solid
    circle((x1, y2), radius, style="solid_light", text="drawlib", textstyle="light")
    circle((x2, y2), radius, style="solid", text="drawlib")
    circle((x3, y2), radius, style="solid_bold", text="drawlib", textstyle="bold")

    # dashed
    circle((x1, y3), radius, style="dashed_light", text="drawlib", textstyle="light")
    circle((x2, y3), radius, style="dashed", text="drawlib")
    circle((x3, y3), radius, style="dashed_bold", text="drawlib", textstyle="bold")

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    # recover to default theme


def test_line_lightbold():
    dtheme.apply_official_theme("monochrome")

    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80

    # default
    line((x1 - 5, y1), (x1 + 5, y1), style="light")
    line((x2 - 5, y1), (x2 + 5, y1))
    line((x3 - 5, y1), (x3 + 5, y1), style="bold")

    # solid
    line((x1 - 5, y2), (x1 + 5, y2), style="solid_light")
    line((x2 - 5, y2), (x2 + 5, y2), style="solid")
    line((x3 - 5, y2), (x3 + 5, y2), style="solid_bold")

    # dashed
    line((x1 - 5, y3), (x1 + 5, y3), style="dashed_light")
    line((x2 - 5, y3), (x2 + 5, y3), style="dashed")
    line((x3 - 5, y3), (x3 + 5, y3), style="dashed_bold")

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    # recover to default theme


def test_image_lightbold():
    dtheme.apply_official_theme("monochrome")

    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80
    width = 10

    # default
    image((x1, y1), width=width, image=IMAGE_FILE, style="light")
    image((x2, y1), width=width, image=IMAGE_FILE)
    image((x3, y1), width=width, image=IMAGE_FILE, style="bold")

    # solid
    image((x1, y2), width=width, image=IMAGE_FILE, style="solid_light")
    image((x2, y2), width=width, image=IMAGE_FILE, style="solid")
    image((x3, y2), width=width, image=IMAGE_FILE, style="solid_bold")

    # dashed
    image((x1, y3), width=width, image=IMAGE_FILE, style="dashed_light")
    image((x2, y3), width=width, image=IMAGE_FILE, style="dashed")
    image((x3, y3), width=width, image=IMAGE_FILE, style="dashed_bold")

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")

    # recover to default theme


def draw(styles: list[str]):
    xs = [20, 50, 80]
    ys = [20, 50, 80]

    for i, style in enumerate(styles):
        x = xs[int(i % 3)]
        y = ys[int(i / 3)]
        circle((x, y), 10, text=style, style=style)


def test_fill():
    dtheme.apply_official_theme("monochrome")
    styles = [""] + dtheme.colors.list()
    draw(styles)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_flat():
    dtheme.apply_official_theme("monochrome")
    styles = ["flat"] + [f"{name}_flat" for name in dtheme.colors.list()]
    draw(styles)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_solid():
    dtheme.apply_official_theme("monochrome")
    styles = ["solid"] + [f"{name}_solid" for name in dtheme.colors.list()]
    draw(styles)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_dashed():
    dtheme.apply_official_theme("monochrome")
    styles = ["dashed"] + [f"{name}_dashed" for name in dtheme.colors.list()]
    draw(styles)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


TABLE = """
+----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+
| class \\ name   |   | light | bold | flat | solid | solid_light | solid_bold | dashed | dashed_light | dashed_bold |
+----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+
| IconStyle      | x | x     | x    | x    |       |             |            |        |              |             |
| ImageStyle     | x | x     | x    | x    | x     | x           | x          | x      | x            | x           |
| LineStyle      | x | x     | x    |      | x     | x           | x          | x      | x            | x           |
| ShapeStyle     | x | x     | x    | x    | x     | x           | x          | x      | x            | x           |
| ShapeTextStyle | x | x     | x    |      |       |             |            |        |              |             |
| TextStyle      | x | x     | x    |      |       |             |            |        |              |             |
+----------------+---+-------+------+------+-------+-------------+------------+--------+--------------+-------------+

+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | black | black_light | black_bold | black_flat | black_solid | black_solid_light | black_solid_bold | black_dashed | black_dashed_light | black_dashed_bold |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
| ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
| ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
| TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
| class \\ name   | charcoal | charcoal_light | charcoal_bold | charcoal_flat | charcoal_solid | charcoal_solid_light | charcoal_solid_bold | charcoal_dashed | charcoal_dashed_light | charcoal_dashed_bold |
+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
| IconStyle      | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
| ImageStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
| LineStyle      | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
| ShapeStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
| ShapeTextStyle | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
| TextStyle      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
| class \\ name   | graphite | graphite_light | graphite_bold | graphite_flat | graphite_solid | graphite_solid_light | graphite_solid_bold | graphite_dashed | graphite_dashed_light | graphite_dashed_bold |
+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
| IconStyle      | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
| ImageStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
| LineStyle      | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
| ShapeStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
| ShapeTextStyle | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
| TextStyle      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | gray | gray_light | gray_bold | gray_flat | gray_solid | gray_solid_light | gray_solid_bold | gray_dashed | gray_dashed_light | gray_dashed_bold |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| class \\ name   | silver | silver_light | silver_bold | silver_flat | silver_solid | silver_solid_light | silver_solid_bold | silver_dashed | silver_dashed_light | silver_dashed_bold |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| IconStyle      | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
| ImageStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| LineStyle      | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
| ShapeStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| ShapeTextStyle | x      | x            | x           |             |              |                    |                   |               |                     |                    |
| TextStyle      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | snow | snow_light | snow_bold | snow_flat | snow_solid | snow_solid_light | snow_solid_bold | snow_dashed | snow_dashed_light | snow_dashed_bold |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | white | white_light | white_bold | white_flat | white_solid | white_solid_light | white_solid_bold | white_dashed | white_dashed_light | white_dashed_bold |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
| ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
| ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
| TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
""".strip()


def test_style_print():
    dtheme.apply_official_theme("monochrome")
    # print()
    # dtheme.print_style_table()
    assert dtheme._get_style_table() == TABLE


COLORS_OUTPUT = """
black   : (  0,   0,   0, 1.0)
charcoal: ( 39,  39,  39, 1.0)
graphite: ( 63,  63,  63, 1.0)
gray    : (127, 127, 127, 1.0)
silver  : (191, 191, 191, 1.0)
snow    : (239, 239, 239, 1.0)
white   : (255, 255, 255, 1.0)
""".strip()


def test_theme_colors_print():
    dtheme.apply_official_theme("monochrome")
    # print()
    # dtheme.print_theme_colors()
    assert dtheme._get_theme_colors() == COLORS_OUTPUT
