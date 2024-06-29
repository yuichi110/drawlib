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
OUTPUT_DIR = "../../../output_tests/v0_1/theme/default/"


def test_fill():
    circle((25, 25), 10, text="drawlib")
    circle((25, 50), 10, style="blue", text="drawlib")
    circle((25, 75), 10, style="green", text="drawlib")
    circle((75, 25), 10, style="red", text="drawlib")
    circle((75, 50), 10, style="black", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white", text="drawlib")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style_images():
    image((25, 25), 20, style="blue", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="blue_solid", image=IMAGE_FILE)
    image((50, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_fill_images():
    image((25, 25), 20, image=IMAGE_FILE)
    image((25, 50), 20, style="blue", image=IMAGE_FILE)
    image((25, 75), 20, style="green", image=IMAGE_FILE)
    image((75, 25), 20, style="red", image=IMAGE_FILE)
    image((75, 50), 20, style="black", image=IMAGE_FILE)
    image((75, 75), 20, style="white", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_flat_images():
    config(grid_only=True, background_color=Colors.Gray)
    image((25, 25), 20, style="flat", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="green_flat", image=IMAGE_FILE)
    image((75, 25), 20, style="red_flat", image=IMAGE_FILE)
    image((75, 50), 20, style="black_flat", image=IMAGE_FILE)
    image((75, 75), 20, style="white_flat", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_solid_images():
    image((25, 25), 20, style="solid", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_solid", image=IMAGE_FILE)
    image((25, 75), 20, style="green_solid", image=IMAGE_FILE)
    image((75, 25), 20, style="red_solid", image=IMAGE_FILE)
    image((75, 50), 20, style="black_solid", image=IMAGE_FILE)
    image((75, 75), 20, style="white_solid", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_dashed_images():
    image((25, 25), 20, style="dashed", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    image((25, 75), 20, style="green_dashed", image=IMAGE_FILE)
    image((75, 25), 20, style="red_dashed", image=IMAGE_FILE)
    image((75, 50), 20, style="black_dashed", image=IMAGE_FILE)
    image((75, 75), 20, style="white_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_flat():
    circle((25, 25), 10, style="flat", text="drawlib")
    circle((25, 50), 10, style="blue_flat", text="drawlib")
    circle((25, 75), 10, style="green_flat", text="drawlib")
    circle((75, 25), 10, style="red_flat", text="drawlib")
    circle((75, 50), 10, style="black_flat", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_flat", text="drawlib")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_solid():
    circle((25, 25), 10, style="solid", text="drawlib")
    circle((25, 50), 10, style="blue_solid", text="drawlib")
    circle((25, 75), 10, style="green_solid", text="drawlib")
    circle((75, 25), 10, style="red_solid", text="drawlib")
    circle((75, 50), 10, style="black_solid", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_solid", text="drawlib")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_dashed():
    circle((25, 25), 10, style="dashed", text="drawlib")
    circle((25, 50), 10, style="blue_dashed", text="drawlib")
    circle((25, 75), 10, style="green_dashed", text="drawlib")
    circle((75, 25), 10, style="red_dashed", text="drawlib")
    circle((75, 50), 10, style="black_dashed", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_dashed", text="drawlib")
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
""".strip()


def test_style_print():
    # print()
    # dtheme.print_style_table()
    assert dtheme._get_style_table() == TABLE


COLORS_OUTPUT = """
red  : (239,  95,  95, 1.0)
green: ( 79, 191,  79, 1.0)
blue : (111, 111, 239, 1.0)
black: (  0,   0,   0, 1.0)
white: (255, 255, 255, 1.0)
""".strip()


def test_theme_colors_print():
    # print()
    # dtheme.print_theme_colors()
    assert dtheme._get_theme_colors() == COLORS_OUTPUT
