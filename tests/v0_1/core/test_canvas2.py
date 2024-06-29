# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_1.apis import *

OUTPUT_DIR = "../../../output_tests/v0_1/core/canvas2/"


def test_serial_save():
    clear()
    circle((25, 25), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_1.png")
    circle((25, 75), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_2.png")
    circle((75, 25), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_3.png")
    circle((75, 75), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_4.png")


def test_serial_save_grid():
    clear()
    config(grid=True)
    circle((25, 25), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_1.png")
    circle((25, 75), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_2.png")
    circle((75, 25), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_3.png")
    circle((75, 75), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_4.png")


def test_serial_save_gridonly():
    circle((25, 25), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_1.png")
    circle((25, 75), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_2.png")
    circle((75, 25), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_3.png")
    circle((75, 75), radius=10)
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}_4.png")
