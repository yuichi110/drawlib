# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: beam."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9

# Outer geometric 'B' frame coordinates
x_left = 18.0
y_bot = 12.0
y_top = 88.0

# 1. Outer 'B' silhouette (Colors.Orange3)
# Bottom loop: center (55.0, 31.0), rx=25.0, ry=19.0 (from -90 deg to +49.5 deg -> meets waist (71.2, 45.4))
# Wait: let both loops meet cleanly at waist point (64.5, 50.0)
b_outer: list[tuple[float, float]] = [
    (x_left, y_bot),
    (55.0, y_bot),
]
steps_loop = 24
# Bottom loop from -90 deg to +90 deg, where +90 deg is at y=50.0, wait:
# Let bottom loop center be (55.0, 31.0), ry=19.0, rx=25.0.
# At ang = +49.0 deg: y = 31.0 + 19.0 * sin(49) = 45.3, x = 55.0 + 25.0 * cos(49) = 71.4.
# Even cleaner: let bottom loop go from -90 deg to +67.6 deg where y = 31.0 + 19.0 * sin(67.6) = 48.6,
# and let both loops share exact waist vertex (64.5, 50.0)!
for i in range(1, steps_loop + 1):
    ang = math.radians(-90.0 + 157.6 * (i / steps_loop))
    b_outer.append((55.0 + 25.0 * math.cos(ang), 31.0 + 19.0 * math.sin(ang)))

# Exact shared waist vertex on right side of 'B'
b_outer.append((64.5, 50.0))

# Top loop: center (54.0, 68.5), rx=24.5, ry=19.5 (from -64.6 deg to +90 deg)
# At -64.6 deg: x = 54.0 + 24.5 * cos(-64.6) = 64.5, y = 68.5 + 19.5 * sin(-64.6) = 50.9!
for i in range(1, steps_loop + 1):
    ang = math.radians(-64.6 + 154.6 * (i / steps_loop))
    b_outer.append((54.0 + 24.5 * math.cos(ang), 68.5 + 19.5 * math.sin(ang)))

b_outer.append((x_left, y_top))

polygon(b_outer, style=no_border_fill(Colors.Orange3))

# 2. Inner converging double-wedge field (Colors.Amber1)
x_inner_wall = 63.0
p_notch = (41.0, 50.0)

wedge_pts: list[tuple[float, float]] = [
    (x_left, 84.5),
    (x_inner_wall, 74.0),
    (x_inner_wall, 63.0),
    p_notch,
    (x_inner_wall, 37.0),
    (x_inner_wall, 26.0),
    (x_left, 15.5),
]
polygon(wedge_pts, style=no_border_fill(Colors.Amber1))

# 3. Two converging horizontal light beams (Colors.Amber3)
top_beam: list[tuple[float, float]] = [
    (x_left, 71.8),
    (x_inner_wall, 74.0),
    (x_inner_wall, 63.0),
    (x_left, 65.2),
]
bot_beam: list[tuple[float, float]] = [
    (x_left, 34.8),
    (x_inner_wall, 37.0),
    (x_inner_wall, 26.0),
    (x_left, 28.2),
]
polygon(top_beam, style=no_border_fill(Colors.Amber3))
polygon(bot_beam, style=no_border_fill(Colors.Amber3))

# 4. Two white semicircular focal lenses on the right end of each beam
for yc_lens in (68.5, 31.5):
    lens_pts: list[tuple[float, float]] = []
    for i in range(17):
        ang = math.radians(90.0 + 180.0 * (i / 16))
        lens_pts.append((x_inner_wall + 5.2 * math.cos(ang), yc_lens + 5.2 * math.sin(ang)))
    polygon(lens_pts, style=no_border_fill(WHITE))
    draw_round_polyline(lens_pts, width_units=1.6, color=DARK, closed=True)

# 5. Crisp dark internal divider lines and outer 'B' outline
draw_round_polyline(top_beam, width_units=1.6, color=DARK, closed=True)
draw_round_polyline(bot_beam, width_units=1.6, color=DARK, closed=True)
draw_round_segment((x_left, 84.5), (x_inner_wall, 74.0), width_units=1.7, color=DARK)
draw_round_segment((x_inner_wall, 63.0), p_notch, width_units=1.7, color=DARK)
draw_round_segment(p_notch, (x_inner_wall, 37.0), width_units=1.7, color=DARK)
draw_round_segment((x_inner_wall, 26.0), (x_left, 15.5), width_units=1.7, color=DARK)

draw_round_polyline(b_outer, width_units=w, color=DARK, closed=True)

save()
