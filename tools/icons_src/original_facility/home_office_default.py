# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: home_office."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
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


# 1. Chimney on the right roof slope (PASTEL_BLUE_LIGHT, extended down behind roof)
rectangle(
    (71.5, 68.5),
    width=8.0,
    height=21.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.5),
)

# 2. Residential house pentagonal facade (WHITE)
house_pts = [
    (20.0, 15.0),
    (80.0, 15.0),
    (80.0, 54.0),
    (50.0, 79.0),
    (20.0, 54.0),
]
polygon(house_pts, style=no_border_fill(WHITE))
draw_round_polyline(house_pts, width_units=w_outer, color=DARK, closed=True)

# 3. Overhanging pitched roof band (PASTEL_BLUE)
roof_pts = [
    (12.0, 52.0),
    (50.0, 84.0),
    (88.0, 52.0),
    (83.5, 47.0),
    (50.0, 75.5),
    (16.5, 47.0),
]
polygon(roof_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(roof_pts, width_units=w_outer, color=DARK, closed=True)

# 4. Laptop inside the house (PASTEL_BLUE_LIGHT screen + PASTEL_BLUE base)
rectangle(
    (50.0, 34.5),
    width=28.0,
    height=17.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=2.2),
)
rectangle(
    (50.0, 23.5),
    width=36.0,
    height=4.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_inner, shape_r=2.0),
)

# 5. PASTEL_GREEN Wi-Fi transmitter dot & curved arc above laptop
wifi_cx, wifi_cy = 50.0, 49.0
circle(
    (wifi_cx, wifi_cy),
    radius=3.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner),
)

arc_pts = _arc_band_pts(wifi_cx, wifi_cy, 7.8, 12.2, 42.0, 138.0)
polygon(arc_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(arc_pts, width_units=w_inner, color=DARK, closed=True)

# 6. Ground baseline
draw_round_segment((14.0, 15.0), (86.0, 15.0), width_units=w_outer, color=DARK)

save()
