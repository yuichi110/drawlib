# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: gps_tracker."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
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

w = ORIG_STROKE

# 1. Top GPS antenna stub (PASTEL_BLUE_LIGHT)
rectangle(
    (67.0, 74.0),
    width=10.0,
    height=9.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2, shape_r=3.0),
)

# 2. Portable GPS map device housing (PASTEL_BLUE)
rectangle(
    (50.0, 42.5),
    width=66.0,
    height=55.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=10.0),
)

# 3. Map display screen background (WHITE)
rectangle(
    (50.0, 42.5),
    width=52.0,
    height=40.0,
    style=no_border_fill(WHITE, shape_r=5.0),
)

# Crisp map road lines inside screen
draw_round_segment((24.8, 35.0), (75.2, 43.0), width_units=2.0, color=DARK)
draw_round_segment((39.0, 23.0), (45.0, 62.0), width_units=2.0, color=DARK)

# Map screen border drawn over line ends
rectangle(
    (50.0, 42.5),
    width=52.0,
    height=40.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=2.2, shape_r=5.0),
)

# 4. Location pin drop (PASTEL_GREEN) with tangent circular head
pin_cx, pin_cy = 50.0, 61.5
pin_tip = (50.0, 35.0)
pin_r = 15.0
dist = pin_cy - pin_tip[1]
alpha_deg = math.degrees(math.asin(pin_r / dist))
ang_start = -alpha_deg
ang_end = 180.0 + alpha_deg

steps = 36
pin_pts: list[tuple[float, float]] = [pin_tip]
for i in range(steps + 1):
    ang = math.radians(ang_start + (ang_end - ang_start) * (i / steps))
    pin_pts.append((pin_cx + pin_r * math.cos(ang), pin_cy + pin_r * math.sin(ang)))

polygon(pin_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(pin_pts, width_units=w, color=DARK, closed=True)

# 5. Center dot inside location pin (WHITE)
circle(
    (pin_cx, pin_cy),
    radius=5.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)

save()
