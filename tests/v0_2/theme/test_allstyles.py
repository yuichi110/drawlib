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
OUTPUT_DIR = "../../../output_tests/v0_2/theme/allstyles/"


def test_list():
    styles = dtheme.allstyles.list()
    # print(styles)
    assert styles == [
        "",
        "light",
        "bold",
        "flat",
        "solid",
        "solid_light",
        "solid_bold",
        "dashed",
        "dashed_light",
        "dashed_bold",
        "red",
        "red_light",
        "red_bold",
        "red_flat",
        "red_solid",
        "red_solid_light",
        "red_solid_bold",
        "red_dashed",
        "red_dashed_light",
        "red_dashed_bold",
        "green",
        "green_light",
        "green_bold",
        "green_flat",
        "green_solid",
        "green_solid_light",
        "green_solid_bold",
        "green_dashed",
        "green_dashed_light",
        "green_dashed_bold",
        "blue",
        "blue_light",
        "blue_bold",
        "blue_flat",
        "blue_solid",
        "blue_solid_light",
        "blue_solid_bold",
        "blue_dashed",
        "blue_dashed_light",
        "blue_dashed_bold",
        "black",
        "black_light",
        "black_bold",
        "black_flat",
        "black_solid",
        "black_solid_light",
        "black_solid_bold",
        "black_dashed",
        "black_dashed_light",
        "black_dashed_bold",
        "white",
        "white_light",
        "white_bold",
        "white_flat",
        "white_solid",
        "white_solid_light",
        "white_solid_bold",
        "white_dashed",
        "white_dashed_light",
        "white_dashed_bold",
    ]


def test_copy():
    dtheme.allstyles.copy("blue", "1")
    circle((50, 50), 10, style="1")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


TABLE_COPY = """
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

+----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
| class \\ name   | red | red_light | red_bold | red_flat | red_solid | red_solid_light | red_solid_bold | red_dashed | red_dashed_light | red_dashed_bold |
+----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
| IconStyle      | x   | x         | x        | x        |           |                 |                |            |                  |                 |
| ImageStyle     | x   | x         | x        | x        | x         | x               | x              | x          | x                | x               |
| LineStyle      | x   | x         | x        |          | x         | x               | x              | x          | x                | x               |
| ShapeStyle     | x   | x         | x        | x        | x         | x               | x              | x          | x                | x               |
| ShapeTextStyle | x   | x         | x        |          |           |                 |                |            |                  |                 |
| TextStyle      | x   | x         | x        |          |           |                 |                |            |                  |                 |
+----------------+-----+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+

+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | green | green_light | green_bold | green_flat | green_solid | green_solid_light | green_solid_bold | green_dashed | green_dashed_light | green_dashed_bold |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
| ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
| ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
| TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | blue | blue_light | blue_bold | blue_flat | blue_solid | blue_solid_light | blue_solid_bold | blue_dashed | blue_dashed_light | blue_dashed_bold |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

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

+----------------+---+---+---+
| class \\ name   | 1 | 2 | 3 |
+----------------+---+---+---+
| IconStyle      | x | x | x |
| ImageStyle     | x | x | x |
| LineStyle      | x | x | x |
| ShapeStyle     | x | x | x |
| ShapeTextStyle | x | x | x |
| TextStyle      | x | x | x |
+----------------+---+---+---+
""".strip()


def test_copy_style_print():
    dtheme.allstyles.copy("blue", "1")
    dtheme.allstyles.copy("green", "2")
    dtheme.allstyles.copy("red", "3")
    # print()
    # dtheme.print_style_table()
    assert dtheme._get_style_table() == TABLE_COPY


TABLE_RENAME = """
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

+----------------+---+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
| class \\ name   | 1 | red_light | red_bold | red_flat | red_solid | red_solid_light | red_solid_bold | red_dashed | red_dashed_light | red_dashed_bold |
+----------------+---+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+
| IconStyle      | x | x         | x        | x        |           |                 |                |            |                  |                 |
| ImageStyle     | x | x         | x        | x        | x         | x               | x              | x          | x                | x               |
| LineStyle      | x | x         | x        |          | x         | x               | x              | x          | x                | x               |
| ShapeStyle     | x | x         | x        | x        | x         | x               | x              | x          | x                | x               |
| ShapeTextStyle | x | x         | x        |          |           |                 |                |            |                  |                 |
| TextStyle      | x | x         | x        |          |           |                 |                |            |                  |                 |
+----------------+---+-----------+----------+----------+-----------+-----------------+----------------+------------+------------------+-----------------+

+----------------+---+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | 2 | green_light | green_bold | green_flat | green_solid | green_solid_light | green_solid_bold | green_dashed | green_dashed_light | green_dashed_bold |
+----------------+---+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| IconStyle      | x | x           | x          | x          |             |                   |                  |              |                    |                   |
| ImageStyle     | x | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| LineStyle      | x | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
| ShapeStyle     | x | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| ShapeTextStyle | x | x           | x          |            |             |                   |                  |              |                    |                   |
| TextStyle      | x | x           | x          |            |             |                   |                  |              |                    |                   |
+----------------+---+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

+----------------+---+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | 3 | blue_light | blue_bold | blue_flat | blue_solid | blue_solid_light | blue_solid_bold | blue_dashed | blue_dashed_light | blue_dashed_bold |
+----------------+---+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+---+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

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


def test_rename():
    dtheme.allstyles.rename("red", "1")
    dtheme.allstyles.rename("green", "2")
    dtheme.allstyles.rename("blue", "3")
    # print()
    # dtheme.print_style_table()
    table = dtheme._get_style_table()

    assert table == TABLE_RENAME


def test_merge():
    theme_styles = dtheme.ThemeStyles(
        iconstyle=IconStyle(style="fill", color=Colors.Red),
        imagestyle=ImageStyle(lwidth=2, lcolor=Colors.Red),
        linestyle=LineStyle(style="dashed", width=5),
        shapestyle=ShapeStyle(lwidth=5, lcolor=Colors.Red),
        shapetextstyle=ShapeTextStyle(color=Colors.White, size=24),
        textstyle=TextStyle(size=24, font=FontSansSerif.RALEWAYS_REGULAR),
    )
    dtheme.allstyles.merge(theme_styles)

    icon_phosphor.google_logo((25, 25), width=30)
    image(xy=(25, 75), width=30, image=IMAGE_FILE)
    line((10, 50), (90, 50))
    line((50, 10), (50, 90), arrowhead="->")
    circle((75, 25), radius=20)
    circle((75, 75), radius=20, text="Hello")
    text((50, 50), "Hello Drawlib", angle=45)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
