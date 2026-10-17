# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: shared_office."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6


def _arc_band_pts(
    cx: float,
    cy: float,
    r_in: float,
    r_out: float,
    deg_start: float,
    deg_end: float,
    steps: int = 20,
) -> list[tuple[float, float]]:
    outer = [
        (
            cx + r_out * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r_out * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]
    inner = [
        (
            cx + r_in * math.cos(math.radians(deg_end - (deg_end - deg_start) * (i / steps))),
            cy + r_in * math.sin(math.radians(deg_end - (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]
    return [*outer, *inner]


# 1. Open office floor room container (WHITE + PASTEL_BLUE_LIGHT floor strip)
# x=13..87, y=15..83
rectangle(
    (50.0, 49.0),
    width=74.0,
    height=68.0,
    style=no_border_fill(WHITE, shape_r=6.0),
)
draw_rounded_corner_block(
    13.0,
    15.0,
    87.0,
    25.0,
    r=6.0,
    round_bl=True,
    round_br=True,
    color=PASTEL_BLUE_LIGHT,
)
draw_round_segment((13.0, 25.0), (87.0, 25.0), width_units=w_inner, color=DARK)
rectangle(
    (50.0, 49.0),
    width=74.0,
    height=68.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w_outer, shape_r=6.0),
)

# 2. Shared coworking bench desk (PASTEL_BLUE tabletop + sturdy legs)
for leg_x in (27.0, 73.0):
    draw_round_segment((leg_x, 25.0), (leg_x, 38.0), width_units=w_outer, color=DARK)

rectangle(
    (50.0, 40.5),
    width=56.0,
    height=5.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_inner, shape_r=2.0),
)

# 3. Two laptops/monitors side by side on the shared desk (PASTEL_BLUE_LIGHT)
for lx in (35.0, 65.0):
    draw_round_segment((lx, 43.2), (lx, 46.5), width_units=w_inner, color=DARK)
    rectangle(
        (lx, 52.5),
        width=16.0,
        height=11.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=2.0),
    )

# 4. PASTEL_GREEN Wi-Fi transmitter dot & curved arc above the shared desk
wifi_cx, wifi_cy = 50.0, 62.5
circle(
    (wifi_cx, wifi_cy),
    radius=3.4,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner),
)

arc_pts = _arc_band_pts(wifi_cx, wifi_cy, 8.2, 13.0, 40.0, 140.0)
polygon(arc_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(arc_pts, width_units=w_inner, color=DARK, closed=True)

save()
