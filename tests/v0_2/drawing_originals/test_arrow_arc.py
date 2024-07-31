# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawing_originals/arrow_arc/"


def test():
    arrow_arc(
        xy=(25, 25),
        radius=15,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
    )

    arrow_arc(
        xy=(25, 75),
        radius=15,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<-",
    )

    arrow_arc(
        xy=(75, 25),
        radius=15,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
        from_angle=270,
        to_angle=90,
    )

    arrow_arc(
        xy=(75, 75),
        radius=15,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<-",
        from_angle=270,
        to_angle=90,
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
