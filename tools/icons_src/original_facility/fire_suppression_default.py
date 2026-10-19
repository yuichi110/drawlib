# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: fire_suppression."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Clean-agent gas cylinder body (x=18..48, y=14..68)
cyl_cx = 33.0
# Dome top + straight tank + flat foot
cyl_pts: list[tuple[float, float]] = [(18.0, 14.0), (48.0, 14.0), (48.0, 54.0)]
steps = 16
for i in range(steps + 1):
    ang = math.radians(180.0 * (i / steps))
    cyl_pts.append((cyl_cx + 15.0 * math.cos(ang), 54.0 + 14.0 * math.sin(ang)))
polygon(cyl_pts, style=Icon.no_border_fill(Icon.WHITE))

# Cylinder top shoulder fill (PASTEL_BLUE, y=54..68)
dome_pts: list[tuple[float, float]] = [(18.0, 54.0), (48.0, 54.0)]
for i in range(steps + 1):
    ang = math.radians(180.0 * (i / steps))
    dome_pts.append((cyl_cx + 15.0 * math.cos(ang), 54.0 + 14.0 * math.sin(ang)))
polygon(dome_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_segment((18.0, 54.0), (48.0, 54.0), width_units=w_inner, color=Icon.DARK)

# Cylinder middle label band (PASTEL_BLUE_LIGHT, y=32..44)
rectangle(
    (cyl_cx, 38.0),
    width=30.0,
    height=12.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
)

# Cylinder bottom foot band (PASTEL_BLUE, y=14..21)
rectangle(
    (cyl_cx, 17.5),
    width=30.0,
    height=7.0,
    style=Icon.no_border_fill(Icon.PASTEL_BLUE),
)
Icon.draw_round_segment((18.0, 21.0), (48.0, 21.0), width_units=w_inner, color=Icon.DARK)

# Cylinder outer contour
Icon.draw_round_polyline(cyl_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Valve neck, operating handle, and pressure gauge
rectangle(
    (cyl_cx, 72.5),
    width=11.0,
    height=9.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=1.0),
)
# Squeeze handle levers pointing left
Icon.draw_round_polyline([(27.5, 76.0), (17.5, 82.0)], width_units=w_outer, color=Icon.DARK)
Icon.draw_round_polyline([(27.5, 73.0), (16.5, 75.0)], width_units=w_outer, color=Icon.DARK)

# Discharge pipe & flared nozzle pointing right/down-right
Icon.draw_round_polyline([(38.5, 74.0), (54.0, 74.0), (58.0, 70.0)], width_units=w_outer, color=Icon.DARK)
nozzle_pts = [
    (55.0, 72.0),
    (66.0, 75.0),
    (69.0, 66.0),
    (58.0, 67.0),
]
polygon(nozzle_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(nozzle_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# Pressure gauge circle at valve center
circle(
    (cyl_cx, 72.5),
    radius=3.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
)
Icon.draw_round_segment((cyl_cx, 72.5), (cyl_cx + 1.8, 74.3), width_units=1.4, color=Icon.DARK)

# 3. Clean-agent spray mist lines from nozzle toward shield
Icon.draw_round_segment((63.0, 64.0), (64.5, 59.5), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((67.5, 64.0), (70.0, 59.5), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((71.5, 66.5), (75.5, 62.5), width_units=w_inner, color=Icon.DARK)

# 4. Foreground PASTEL_GREEN suppression shield at (67.0, 14..58)
sx = 67.0
y_bot, y_top = 14.0, 56.0
half_w = 18.0
left_pts = Icon.build_shield_half_points(sx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(sx, y_bot, y_top, half_w, side="right")
shield_pts = left_pts + list(reversed(right_pts[1:-1]))

polygon(shield_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(shield_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# Inner WHITE clean-agent droplet inside shield
drop_r = 6.5
drop_cy = 32.5
drop_pts: list[tuple[float, float]] = [(sx, 45.5)]
for i in range(steps + 1):
    ang = math.radians(150.0 + 240.0 * (i / steps))
    drop_pts.append((sx + drop_r * math.cos(ang), drop_cy + drop_r * math.sin(ang)))
polygon(drop_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(drop_pts, width_units=w_inner, color=Icon.DARK, closed=True)

save()
