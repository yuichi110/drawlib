# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: datacenter."""

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


def _top_rounded_box(x0: float, y0: float, x1: float, y1: float, r: float) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = [(x0, y0), (x1, y0)]
    steps = 10
    for i in range(steps + 1):
        ang = math.radians(0.0 + 90.0 * (i / steps))
        pts.append((x1 - r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    for i in range(steps + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps))
        pts.append((x0 + r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    return pts


# 1. Left and right windowless fortress buttress wings
for x0, x1 in ((14.0, 28.0), (72.0, 86.0)):
    wing_pts = _top_rounded_box(x0, 14.0, x1, 68.0, 3.5)
    polygon(wing_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
    draw_round_polyline(wing_pts, width_units=w_outer, color=DARK, closed=True)
    for y_louver in (60.0, 54.5):
        draw_round_segment((x0 + 3.5, y_louver), (x1 - 3.5, y_louver), width_units=w_inner, color=DARK)

# 2. Upper roof HVAC / security crown
crown_pts = _top_rounded_box(32.0, 76.0, 68.0, 85.0, 3.0)
polygon(crown_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(crown_pts, width_units=w_outer, color=DARK, closed=True)

# 3. Main central windowless fortress building
main_pts = _top_rounded_box(25.0, 14.0, 75.0, 78.0, 4.0)
polygon(main_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(main_pts, width_units=w_outer, color=DARK, closed=True)

# 4. Central WHITE server rack bay inside fortress
rectangle(
    (50.0, 41.0),
    width=36.0,
    height=46.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=3.5),
)

# 5. Three stacked server blade units with PASTEL_GREEN status LEDs
for cy in (55.0, 42.0, 29.0):
    rectangle(
        (50.0, cy),
        width=28.0,
        height=8.5,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=2.0),
    )
    draw_round_segment((40.0, cy), (50.0, cy), width_units=w_inner, color=DARK)
    circle(
        (59.0, cy),
        radius=2.3,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner),
    )

# 6. Top security crest indicator bar in PASTEL_GREEN
rectangle(
    (50.0, 70.5),
    width=18.0,
    height=4.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner, shape_r=2.0),
)

# 7. Ground foundation line
draw_round_segment((11.5, 14.0), (88.5, 14.0), width_units=w_outer, color=DARK)

save()
