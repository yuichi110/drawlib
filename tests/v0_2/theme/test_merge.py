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
OUTPUT_DIR = "../../../output_tests/v0_2/theme/merge/"


def test_iconstyle():
    dtheme.iconstyles.merge(IconStyle(style="fill", color=Colors.Red))
    icon_phosphor.google_logo((50, 50), width=30)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_imagestyle():
    dtheme.imagestyles.merge(ImageStyle(lwidth=2, lcolor=Colors.Red))
    image(xy=(50, 50), width=30, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_linestyle():
    dtheme.linestyles.merge(LineStyle(style="dashed", width=5))
    line((10, 10), (90, 90))
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_shapestyle():
    dtheme.shapestyles.merge(ShapeStyle(lwidth=5, lcolor=Colors.Red))
    circle((50, 50), radius=20)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_shapetextstyle():
    dtheme.shapetextstyles.merge(ShapeTextStyle(color=Colors.White, size=24))
    circle((50, 50), radius=20, text="Hello")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_textstyle():
    dtheme.textstyles.merge(TextStyle(size=24, font=FontSansSerif.RALEWAYS_REGULAR))
    text((50, 50), "Hello Drawlib")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_allstyle():
    dtheme.allstyles.merge(
        dtheme.ThemeStyles(textstyle=TextStyle(font=FontSansSerif.RALEWAYS_LIGHT)),
        targets=["light", "red_light", "blue_light", "green_light", "black_light", "white_light"],
    )
    dtheme.allstyles.merge(
        dtheme.ThemeStyles(textstyle=TextStyle(font=FontSansSerif.RALEWAYS_REGULAR)),
        targets=["", "red", "blue", "green", "black", "white"],
    )
    dtheme.allstyles.merge(
        dtheme.ThemeStyles(textstyle=TextStyle(font=FontSansSerif.RALEWAYS_BOLD)),
        targets=["bold", "red_bold", "blue_bold", "green_bold", "black_bold", "white_bold"],
    )

    text((25, 25), "Hello Drawlib", style="light")
    text((25, 50), "Hello Drawlib")
    text((25, 75), "Hello Drawlib", style="bold")
    text((75, 25), "Hello Drawlib", style="red_light")
    text((75, 50), "Hello Drawlib", style="red")
    text((75, 75), "Hello Drawlib", style="red_bold")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
