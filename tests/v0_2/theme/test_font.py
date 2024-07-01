# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


from drawlib.apis import *

IMAGE_FILE = "../../assets/image.png"
OUTPUT_DIR = "../../../output_tests/v0_2/theme/font/"

FONT_MPLUS1P_LIGHT = "../../assets/mplus1p/light.ttf"
FONT_MPLUS1P_REGULAR = "../../assets/mplus1p/regular.ttf"
FONT_MPLUS1P_BOLD = "../../assets/mplus1p/bold.ttf"


def test_change_default_fonts():
    dtheme.change_default_fonts(
        light_font=FontSansSerif.RALEWAYS_LIGHT,
        regular_font=FontSansSerif.RALEWAYS_REGULAR,
        bold_font=FontSansSerif.RALEWAYS_BOLD,
    )

    text((25, 25), "Hello Drawlib", style="light")
    text((25, 50), "Hello Drawlib")
    text((25, 75), "Hello Drawlib", style="bold")
    text((75, 25), "Hello Drawlib", style="red_light")
    text((75, 50), "Hello Drawlib", style="red")
    text((75, 75), "Hello Drawlib", style="red_bold")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_change_default_fonts_file():
    dtheme.change_default_fonts(
        light_font=FontFile(FONT_MPLUS1P_LIGHT),
        regular_font=FontFile(FONT_MPLUS1P_REGULAR),
        bold_font=FontFile(FONT_MPLUS1P_BOLD),
    )

    text((25, 25), "こんにちは Drawlib", style="light")
    text((25, 50), "こんにちは Drawlib")
    text((25, 75), "こんにちは Drawlib", style="bold")
    text((75, 25), "こんにちは Drawlib", style="red_light")
    text((75, 50), "こんにちは Drawlib", style="red")
    text((75, 75), "こんにちは Drawlib", style="red_bold")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_change_default_font_size():
    dtheme.change_default_font_size(28)

    text((25, 25), "Hello Drawlib", style="light")
    text((25, 50), "Hello Drawlib")
    text((25, 75), "Hello Drawlib", style="bold")
    text((75, 25), "Hello Drawlib", style="red_light")
    text((75, 50), "Hello Drawlib", style="red")
    text((75, 75), "Hello Drawlib", style="red_bold")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
