# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: binary_executable."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

b = 2.0
w_line = 2.0

# 3 short DARK pins on each of the 4 sides
for p in (34.0, 50.0, 66.0):
    draw_round_segment((p, 82.0), (p, 88.5), width_units=w_line, color=DARK)
    draw_round_segment((p, 11.5), (p, 18.0), width_units=w_line, color=DARK)
    draw_round_segment((11.5, p), (18.0, p), width_units=w_line, color=DARK)
    draw_round_segment((82.0, p), (88.5, p), width_units=w_line, color=DARK)

# Square PASTEL_BLUE chip/module plate
rectangle(
    (50.0, 50.0),
    width=64.0,
    height=64.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b, shape_r=6.0),
)

# Inner WHITE panel
rectangle(
    (50.0, 50.0),
    width=48.0,
    height=48.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=3.0),
)


def _draw_zero(cx: float, cy: float) -> None:
    rectangle(
        (cx, cy),
        width=11.0,
        height=15.0,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=b, shape_r=5.5),
    )
    rectangle(
        (cx, cy),
        width=4.6,
        height=8.6,
        style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=2.3),
    )


def _draw_one(cx: float, cy: float) -> None:
    rectangle(
        (cx, cy),
        width=5.6,
        height=15.0,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b, shape_r=2.0),
    )


# 2x2 grid: '0 1' top, '1 0' bottom
_draw_zero(40.0, 60.0)
_draw_one(60.0, 60.0)
_draw_one(40.0, 40.0)
_draw_zero(60.0, 40.0)

save()
