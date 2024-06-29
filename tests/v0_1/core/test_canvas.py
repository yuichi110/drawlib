# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/core/canvas/"


def test_save_without_filename():
    circle((50, 50), 30)
    # file name should be "<module-name-who-call-save>.png"
    # save to module file directory
    # in this case, ./test_canvas.png
    save()


def test_save_with_format():
    circle((50, 50), 30)
    # file name should be "<module-name-who-call-save>.webp"
    # save to module file directory
    # in this case, ./test_canvas.webp
    save(format="webp")


def test_size():
    config(width=192, height=108, grid_only=True)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_grid_pitch():
    config(width=200, height=100, grid_only=True, grid_xpitch=10, grid_ypitch=50)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_dpi():
    config(grid_only=True, dpi=200)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_background():
    config(
        background_color=Colors140.Orange,
        background_alpha=0.2,
        grid_only=True,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_grid():
    config(
        grid_only=True,
        grid_style=LineStyle(
            width=1,
            color=Colors.Red,
            style="dashed",
        ),
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_nogrid():
    clear()
    config()
    circle((50, 50), 30)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_both():
    clear()
    config(grid=True)
    circle((50, 50), 30)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
