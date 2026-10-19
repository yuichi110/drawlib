# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: school."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Side classroom wings (WHITE, x=15..85, y=18..54)
rectangle(
    (50.0, 36.0),
    width=70.0,
    height=36.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer),
)

# Side wing sloped roofs (PASTEL_BLUE)
side_roof_pts = [
    (12.0, 54.0),
    (28.0, 61.0),
    (72.0, 61.0),
    (88.0, 54.0),
]
polygon(side_roof_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(side_roof_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Central classical pavilion (WHITE, x=30..70, y=18..61)
rectangle(
    (50.0, 39.5),
    width=40.0,
    height=43.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer),
)

# 3. Classical triangular pediment (PASTEL_BLUE)
pediment_outer = [
    (25.0, 61.0),
    (50.0, 81.0),
    (75.0, 61.0),
]
polygon(pediment_outer, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(pediment_outer, width_units=w_outer, color=Icon.DARK, closed=True)

# Flagpole & PASTEL_GREEN pennant on top of pediment
Icon.draw_round_segment((50.0, 81.0), (50.0, 88.5), width_units=w_outer, color=Icon.DARK)
flag_pts = [(50.0, 88.5), (60.0, 85.5), (50.0, 82.5)]
polygon(flag_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(flag_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 4. PASTEL_GREEN campus clock inside pediment at (50.0, 68.5)
cx, cy = 50.0, 68.5
circle(
    (cx, cy),
    radius=6.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer),
)
Icon.draw_round_segment((cx, cy), (cx, cy + 3.8), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((cx, cy), (cx + 3.2, cy), width_units=w_inner, color=Icon.DARK)

# 5. Side wing windows (PASTEL_BLUE_LIGHT)
for wx in (22.5, 77.5):
    for wy in (44.0, 30.0):
        rectangle(
            (wx, wy),
            width=7.5,
            height=9.0,
            style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.0),
        )

# Central pavilion upper side windows
for wx in (36.5, 63.5):
    rectangle(
        (wx, 48.0),
        width=6.5,
        height=9.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.0),
    )

# 6. Central arched double door (PASTEL_BLUE, x=43..57, y=18..40)
door_pts: list[tuple[float, float]] = [(43.0, 18.0), (57.0, 18.0), (57.0, 33.0)]
steps = 12
for i in range(steps + 1):
    ang = math.radians(180.0 * (i / steps))
    door_pts.append((50.0 + 7.0 * math.cos(ang), 33.0 + 7.0 * math.sin(ang)))
polygon(door_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(door_pts, width_units=w_outer, color=Icon.DARK, closed=True)
Icon.draw_round_segment((50.0, 18.0), (50.0, 40.0), width_units=w_inner, color=Icon.DARK)

# 7. Stepped ground foundation
rectangle(
    (50.0, 16.5),
    width=74.0,
    height=3.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=1.0),
)
rectangle(
    (50.0, 13.5),
    width=80.0,
    height=3.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=1.0),
)

save()
