# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.v0_2.apis import *

OUTPUT_DIR = "../../../output_tests/v0_2/drawings_originals/arrow_arc/"


def test_circle():
    ellipse(xy=(25, 25), width=30, height=30, style="dashed")
    arrow_arc(
        xy=(25, 25),
        width=30,
        height=30,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
        from_angle=45,
        to_angle=135,
    )

    ellipse(xy=(25, 75), width=30, height=30, style="dashed")
    arrow_arc(
        xy=(25, 75),
        width=30,
        height=30,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<->",
        from_angle=0,
        to_angle=270,
    )

    ellipse(xy=(75, 25), width=30, height=30, style="dashed")
    arrow_arc(
        xy=(75, 25),
        width=30,
        height=30,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
        from_angle=270,
        to_angle=90,
    )

    ellipse(xy=(75, 75), width=30, height=30, style="dashed")
    arrow_arc(
        xy=(75, 75),
        width=30,
        height=30,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<-",
        from_angle=270,
        to_angle=180,
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ellipse():
    ellipse(xy=(25, 25), width=40, height=20, style="dashed")
    arrow_arc(
        xy=(25, 25),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
        from_angle=45,
        to_angle=135,
    )

    ellipse(xy=(25, 75), width=40, height=20, style="dashed")
    arrow_arc(
        xy=(25, 75),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<-",
        from_angle=355,
        to_angle=180,
    )

    ellipse(xy=(75, 25), width=40, height=20, style="dashed")
    arrow_arc(
        xy=(75, 25),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
        from_angle=270,
        to_angle=90,
    )

    ellipse(xy=(75, 75), width=40, height=20, style="dashed")
    arrow_arc(
        xy=(75, 75),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<-",
        from_angle=270,
        to_angle=180,
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")


def test_ellipse_angle45():
    ellipse(xy=(25, 25), width=40, height=20, style="dashed", angle=45)
    arrow_arc(
        xy=(25, 25),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
        from_angle=45,
        to_angle=135,
        angle=45,
    )

    ellipse(xy=(25, 75), width=40, height=20, style="dashed", angle=45)
    arrow_arc(
        xy=(25, 75),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<-",
        from_angle=355,
        to_angle=180,
        angle=45,
    )

    ellipse(xy=(75, 25), width=40, height=20, style="dashed", angle=45)
    arrow_arc(
        xy=(75, 25),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="->",
        from_angle=270,
        to_angle=90,
        angle=45,
    )

    ellipse(xy=(75, 75), width=40, height=20, style="dashed", angle=45)
    arrow_arc(
        xy=(75, 75),
        width=40,
        height=20,
        tail_width=5,
        head_angle=20,
        head_width=10,
        head="<-",
        from_angle=270,
        to_angle=180,
        angle=45,
    )

    save(f"{OUTPUT_DIR}{dutil_script.get_function_name()}.png")
