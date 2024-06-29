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
OUTPUT_DIR = "../../../output_tests/v0_1/theme/essentials/"


def test_colors():
    dtheme.apply_official_theme("essentials")

    x_start = 10
    x_pad = 20
    y_start = 10
    y_pad = 20
    for i, color in enumerate(dtheme.colors.list()):
        row = int(i / 5)
        col = i % 5
        if color in {"navy", "charcoal", "graphite", "black"}:
            ts = "white"
        else:
            ts = ""
        rectangle(
            (x_start + x_pad * col, y_start + y_pad * row),
            width=15,
            height=10,
            text=color,
            style=color,
            textstyle=ts,
        )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_difficult_to_see_colors():
    dtheme.apply_official_theme("essentials")
    config(width=100, height=50, grid_only=False, grid=False)
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 10
    y2 = 25
    y3 = 40

    for x, name in [(x1, "yellow"), (x2, "ivory"), (x3, "snow")]:
        line((x - 10, y1), (x + 10, y1), style=f"{name}_bold")
        circle((x, y2), radius=10, style=name)
        text((x, y3), "Hello Drawlib!", style=f"{name}_bold")

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_fill():
    dtheme.apply_official_theme("essentials")
    circle((25, 25), 10, text="drawlib")
    circle((25, 50), 10, style="blue", text="drawlib")
    circle((25, 75), 10, style="green", text="drawlib")
    circle((75, 25), 10, style="red", text="drawlib")
    circle((75, 50), 10, style="black", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white", text="drawlib")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style_images():
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, style="blue", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="blue_solid", image=IMAGE_FILE)
    image((50, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_fill_images():
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, image=IMAGE_FILE)
    image((25, 50), 20, style="blue", image=IMAGE_FILE)
    image((25, 75), 20, style="green", image=IMAGE_FILE)
    image((75, 25), 20, style="red", image=IMAGE_FILE)
    image((75, 50), 20, style="black", image=IMAGE_FILE)
    image((75, 75), 20, style="white", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_flat_images():
    dtheme.apply_official_theme("essentials")
    config(background_color=Colors.Gray)
    image((25, 25), 20, style="flat", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="green_flat", image=IMAGE_FILE)
    image((75, 25), 20, style="red_flat", image=IMAGE_FILE)
    image((75, 50), 20, style="black_flat", image=IMAGE_FILE)
    image((75, 75), 20, style="white_flat", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_solid_images():
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, style="solid", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_solid", image=IMAGE_FILE)
    image((25, 75), 20, style="green_solid", image=IMAGE_FILE)
    image((75, 25), 20, style="red_solid", image=IMAGE_FILE)
    image((75, 50), 20, style="black_solid", image=IMAGE_FILE)
    image((75, 75), 20, style="white_solid", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_dashed_images():
    dtheme.apply_official_theme("essentials")
    image((25, 25), 20, style="dashed", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    image((25, 75), 20, style="green_dashed", image=IMAGE_FILE)
    image((75, 25), 20, style="red_dashed", image=IMAGE_FILE)
    image((75, 50), 20, style="black_dashed", image=IMAGE_FILE)
    image((75, 75), 20, style="white_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_flat():
    dtheme.apply_official_theme("essentials")
    circle((25, 25), 10, style="flat", text="drawlib")
    circle((25, 50), 10, style="blue_flat", text="drawlib")
    circle((25, 75), 10, style="green_flat", text="drawlib")
    circle((75, 25), 10, style="red_flat", text="drawlib")
    circle((75, 50), 10, style="black_flat", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_flat", text="drawlib")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_solid():
    dtheme.apply_official_theme("essentials")
    circle((25, 25), 10, style="solid", text="drawlib")
    circle((25, 50), 10, style="blue_solid", text="drawlib")
    circle((25, 75), 10, style="green_solid", text="drawlib")
    circle((75, 25), 10, style="red_solid", text="drawlib")
    circle((75, 50), 10, style="black_solid", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_solid", text="drawlib")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_dashed():
    dtheme.apply_official_theme("essentials")
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

+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
| class \\ name   | lightred | lightred_light | lightred_bold | lightred_flat | lightred_solid | lightred_solid_light | lightred_solid_bold | lightred_dashed | lightred_dashed_light | lightred_dashed_bold |
+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+
| IconStyle      | x        | x              | x             | x             |                |                      |                     |                 |                       |                      |
| ImageStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
| LineStyle      | x        | x              | x             |               | x              | x                    | x                   | x               | x                     | x                    |
| ShapeStyle     | x        | x              | x             | x             | x              | x                    | x                   | x               | x                     | x                    |
| ShapeTextStyle | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
| TextStyle      | x        | x              | x             |               |                |                      |                     |                 |                       |                      |
+----------------+----------+----------------+---------------+---------------+----------------+----------------------+---------------------+-----------------+-----------------------+----------------------+

+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | pink | pink_light | pink_bold | pink_flat | pink_solid | pink_solid_light | pink_solid_bold | pink_dashed | pink_dashed_light | pink_dashed_bold |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | brown | brown_light | brown_bold | brown_flat | brown_solid | brown_solid_light | brown_solid_bold | brown_dashed | brown_dashed_light | brown_dashed_bold |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
| ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
| ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
| TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| class \\ name   | orange | orange_light | orange_bold | orange_flat | orange_solid | orange_solid_light | orange_solid_bold | orange_dashed | orange_dashed_light | orange_dashed_bold |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| IconStyle      | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
| ImageStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| LineStyle      | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
| ShapeStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| ShapeTextStyle | x      | x            | x           |             |              |                    |                   |               |                     |                    |
| TextStyle      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

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

+----------------+------------+------------------+-----------------+-----------------+------------------+------------------------+-----------------------+-------------------+-------------------------+------------------------+
| class \\ name   | lightgreen | lightgreen_light | lightgreen_bold | lightgreen_flat | lightgreen_solid | lightgreen_solid_light | lightgreen_solid_bold | lightgreen_dashed | lightgreen_dashed_light | lightgreen_dashed_bold |
+----------------+------------+------------------+-----------------+-----------------+------------------+------------------------+-----------------------+-------------------+-------------------------+------------------------+
| IconStyle      | x          | x                | x               | x               |                  |                        |                       |                   |                         |                        |
| ImageStyle     | x          | x                | x               | x               | x                | x                      | x                     | x                 | x                       | x                      |
| LineStyle      | x          | x                | x               |                 | x                | x                      | x                     | x                 | x                       | x                      |
| ShapeStyle     | x          | x                | x               | x               | x                | x                      | x                     | x                 | x                       | x                      |
| ShapeTextStyle | x          | x                | x               |                 |                  |                        |                       |                   |                         |                        |
| TextStyle      | x          | x                | x               |                 |                  |                        |                       |                   |                         |                        |
+----------------+------------+------------------+-----------------+-----------------+------------------+------------------------+-----------------------+-------------------+-------------------------+------------------------+

+----------------+-------------+-------------------+------------------+------------------+-------------------+-------------------------+------------------------+--------------------+--------------------------+-------------------------+
| class \\ name   | greenyellow | greenyellow_light | greenyellow_bold | greenyellow_flat | greenyellow_solid | greenyellow_solid_light | greenyellow_solid_bold | greenyellow_dashed | greenyellow_dashed_light | greenyellow_dashed_bold |
+----------------+-------------+-------------------+------------------+------------------+-------------------+-------------------------+------------------------+--------------------+--------------------------+-------------------------+
| IconStyle      | x           | x                 | x                | x                |                   |                         |                        |                    |                          |                         |
| ImageStyle     | x           | x                 | x                | x                | x                 | x                       | x                      | x                  | x                        | x                       |
| LineStyle      | x           | x                 | x                |                  | x                 | x                       | x                      | x                  | x                        | x                       |
| ShapeStyle     | x           | x                 | x                | x                | x                 | x                       | x                      | x                  | x                        | x                       |
| ShapeTextStyle | x           | x                 | x                |                  |                   |                         |                        |                    |                          |                         |
| TextStyle      | x           | x                 | x                |                  |                   |                         |                        |                    |                          |                         |
+----------------+-------------+-------------------+------------------+------------------+-------------------+-------------------------+------------------------+--------------------+--------------------------+-------------------------+

+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | teal | teal_light | teal_bold | teal_flat | teal_solid | teal_solid_light | teal_solid_bold | teal_dashed | teal_dashed_light | teal_dashed_bold |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | olive | olive_light | olive_bold | olive_flat | olive_solid | olive_solid_light | olive_solid_bold | olive_dashed | olive_dashed_light | olive_dashed_bold |
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

+----------------+-----------+-----------------+----------------+----------------+-----------------+-----------------------+----------------------+------------------+------------------------+-----------------------+
| class \\ name   | lightblue | lightblue_light | lightblue_bold | lightblue_flat | lightblue_solid | lightblue_solid_light | lightblue_solid_bold | lightblue_dashed | lightblue_dashed_light | lightblue_dashed_bold |
+----------------+-----------+-----------------+----------------+----------------+-----------------+-----------------------+----------------------+------------------+------------------------+-----------------------+
| IconStyle      | x         | x               | x              | x              |                 |                       |                      |                  |                        |                       |
| ImageStyle     | x         | x               | x              | x              | x               | x                     | x                    | x                | x                      | x                     |
| LineStyle      | x         | x               | x              |                | x               | x                     | x                    | x                | x                      | x                     |
| ShapeStyle     | x         | x               | x              | x              | x               | x                     | x                    | x                | x                      | x                     |
| ShapeTextStyle | x         | x               | x              |                |                 |                       |                      |                  |                        |                       |
| TextStyle      | x         | x               | x              |                |                 |                       |                      |                  |                        |                       |
+----------------+-----------+-----------------+----------------+----------------+-----------------+-----------------------+----------------------+------------------+------------------------+-----------------------+

+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | aqua | aqua_light | aqua_bold | aqua_flat | aqua_solid | aqua_solid_light | aqua_solid_bold | aqua_dashed | aqua_dashed_light | aqua_dashed_bold |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| class \\ name   | navy | navy_light | navy_bold | navy_flat | navy_solid | navy_solid_light | navy_solid_bold | navy_dashed | navy_dashed_light | navy_dashed_bold |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+
| IconStyle      | x    | x          | x         | x         |            |                  |                 |             |                   |                  |
| ImageStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| LineStyle      | x    | x          | x         |           | x          | x                | x               | x           | x                 | x                |
| ShapeStyle     | x    | x          | x         | x         | x          | x                | x               | x           | x                 | x                |
| ShapeTextStyle | x    | x          | x         |           |            |                  |                 |             |                   |                  |
| TextStyle      | x    | x          | x         |           |            |                  |                 |             |                   |                  |
+----------------+------+------------+-----------+-----------+------------+------------------+-----------------+-------------+-------------------+------------------+

+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | steel | steel_light | steel_bold | steel_flat | steel_solid | steel_solid_light | steel_solid_bold | steel_dashed | steel_dashed_light | steel_dashed_bold |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
| ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
| ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
| TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| class \\ name   | yellow | yellow_light | yellow_bold | yellow_flat | yellow_solid | yellow_solid_light | yellow_solid_bold | yellow_dashed | yellow_dashed_light | yellow_dashed_bold |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| IconStyle      | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
| ImageStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| LineStyle      | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
| ShapeStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| ShapeTextStyle | x      | x            | x           |             |              |                    |                   |               |                     |                    |
| TextStyle      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| class \\ name   | purple | purple_light | purple_bold | purple_flat | purple_solid | purple_solid_light | purple_solid_bold | purple_dashed | purple_dashed_light | purple_dashed_bold |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+
| IconStyle      | x      | x            | x           | x           |              |                    |                   |               |                     |                    |
| ImageStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| LineStyle      | x      | x            | x           |             | x            | x                  | x                 | x             | x                   | x                  |
| ShapeStyle     | x      | x            | x           | x           | x            | x                  | x                 | x             | x                   | x                  |
| ShapeTextStyle | x      | x            | x           |             |              |                    |                   |               |                     |                    |
| TextStyle      | x      | x            | x           |             |              |                    |                   |               |                     |                    |
+----------------+--------+--------------+-------------+-------------+--------------+--------------------+-------------------+---------------+---------------------+--------------------+

+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| class \\ name   | ivory | ivory_light | ivory_bold | ivory_flat | ivory_solid | ivory_solid_light | ivory_solid_bold | ivory_dashed | ivory_dashed_light | ivory_dashed_bold |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+
| IconStyle      | x     | x           | x          | x          |             |                   |                  |              |                    |                   |
| ImageStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| LineStyle      | x     | x           | x          |            | x           | x                 | x                | x            | x                  | x                 |
| ShapeStyle     | x     | x           | x          | x          | x           | x                 | x                | x            | x                  | x                 |
| ShapeTextStyle | x     | x           | x          |            |             |                   |                  |              |                    |                   |
| TextStyle      | x     | x           | x          |            |             |                   |                  |              |                    |                   |
+----------------+-------+-------------+------------+------------+-------------+-------------------+------------------+--------------+--------------------+-------------------+

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
    dtheme.apply_official_theme("essentials")
    # print()
    # dtheme.print_style_table()
    assert dtheme._get_style_table() == TABLE


COLORS_OUTPUT = """
red        : (255,  23,  23, 1.0)
lightred   : (239,  95,  95, 1.0)
pink       : (239,  63, 239, 1.0)
brown      : (159,  31,  31, 1.0)
orange     : (255,  95,  31, 1.0)
green      : ( 15, 127,  15, 1.0)
lightgreen : ( 79, 191,  79, 1.0)
greenyellow: (127, 207,  31, 1.0)
teal       : ( 15, 127, 127, 1.0)
olive      : (127, 127,  31, 1.0)
blue       : ( 31,  31, 255, 1.0)
lightblue  : (111, 111, 239, 1.0)
aqua       : ( 47, 239, 239, 1.0)
navy       : ( 15,  15, 127, 1.0)
steel      : ( 96,  96, 143, 1.0)
yellow     : (239, 239,  31, 1.0)
purple     : (127,  31, 127, 1.0)
ivory      : (239, 239, 207, 1.0)
black      : (  0,   0,   0, 1.0)
charcoal   : ( 39,  39,  39, 1.0)
graphite   : ( 63,  63,  63, 1.0)
gray       : (127, 127, 127, 1.0)
silver     : (191, 191, 191, 1.0)
snow       : (239, 239, 239, 1.0)
white      : (255, 255, 255, 1.0)
""".strip()


def test_theme_colors_print():
    dtheme.apply_official_theme("essentials")
    # print()
    # dtheme.print_theme_colors()
    assert dtheme._get_theme_colors() == COLORS_OUTPUT
