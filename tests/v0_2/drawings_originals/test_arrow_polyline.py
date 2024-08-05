# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_originals/arrow_polyline/"


def test():
    arrow_polyline(
        xys=[(10, 10), (10, 50), (50, 50), (50, 10)],
        tail_width=2,
        head_length=3,
        head_width=5,
        head="->",
        r=5,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test2():
    arrow_polyline(
        xys=[(10, 10), (10, 50), (50, 50), (50, 10)],
        tail_width=2,
        head_length=3,
        head_width=5,
        head="<-",
        r=5,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test3():
    arrow_polyline(
        xys=[(10, 10), (10, 50), (50, 50), (50, 10)],
        tail_width=2,
        head_length=3,
        head_width=5,
        head="<->",
        r=5,
    )
    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
