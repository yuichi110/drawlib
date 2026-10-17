# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: qr_code."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Outer QR plate (WHITE)
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=10.0),
)


def _draw_finder(cx: float, cy: float, color: str) -> None:
    rectangle(
        (cx, cy),
        width=21.0,
        height=21.0,
        style=fill_style(color, border_color=DARK, border_units=2.2, shape_r=3.5),
    )
    rectangle(
        (cx, cy),
        width=11.5,
        height=11.5,
        style=fill_style(WHITE, border_color=DARK, border_units=1.8, shape_r=1.8),
    )
    rectangle(
        (cx, cy),
        width=5.0,
        height=5.0,
        style=fill_style(DARK, shape_r=0.8),
    )


# 2. Three corner finder squares in PASTEL_BLUE and PASTEL_GREEN
_draw_finder(31.0, 69.0, PASTEL_BLUE)
_draw_finder(31.0, 31.0, PASTEL_BLUE)
_draw_finder(69.0, 69.0, PASTEL_GREEN)

# 3. QR data modules (DARK) in center timing lanes and bottom-right quadrant
module_coords = [
    (50.0, 74.0),
    (50.0, 64.0),
    (50.0, 50.0),
    (26.0, 50.0),
    (36.0, 50.0),
    (60.0, 50.0),
    (74.0, 50.0),
    (50.0, 38.0),
    (60.0, 38.0),
    (69.0, 38.0),
    (78.0, 38.0),
    (50.0, 29.0),
    (69.0, 29.0),
    (50.0, 21.0),
    (60.0, 21.0),
    (76.0, 21.0),
]

for mx, my in module_coords:
    rectangle(
        (mx, my),
        width=5.4,
        height=5.4,
        style=fill_style(DARK, shape_r=1.0),
    )

save()
