# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/drawing_icons/icon_phosphor/"


def test():
    icon_phosphor.google_logo(
        xy=(50, 50),
        width=20,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_style():
    icon_phosphor.google_logo(
        xy=(50, 50),
        width=20,
        style=IconStyle(
            style="fill",
            color=Colors.Red,
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_angle45():
    icon_phosphor.google_logo(
        xy=(50, 50),
        width=20,
        angle=45,
        style=IconStyle(
            style="thin",
            color=Colors.Red,
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_theme():
    icon_phosphor.google_logo(xy=(25, 25), width=20, style="blue")
    icon_phosphor.google_logo(xy=(25, 75), width=20, style="green")
    icon_phosphor.google_logo(xy=(75, 25), width=20, style="red")
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
