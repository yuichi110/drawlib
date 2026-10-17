# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: firewall."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 1.8
w_line = 2.7
mortar_w = 2.2

# 1. Background brick wall base fill (x=12..80, y=25..83)
wall_cx, wall_cy = 46.0, 54.0
wall_w, wall_h = 68.0, 58.0
wall_r = 6.0

rectangle(
    (wall_cx, wall_cy),
    width=wall_w,
    height=wall_h,
    style=no_border_fill(PASTEL_BLUE, shape_r=wall_r),
)

# 2. Highlighted bricks in PASTEL_BLUE_LIGHT (interior non-corner bricks)
rectangle((46.0, 75.75), width=24.0, height=14.5, style=no_border_fill(PASTEL_BLUE_LIGHT))
rectangle((34.5, 61.25), width=23.0, height=14.5, style=no_border_fill(PASTEL_BLUE_LIGHT))
rectangle((34.5, 32.25), width=23.0, height=14.5, style=no_border_fill(PASTEL_BLUE_LIGHT))

# 3. Horizontal mortar lines (3 dividers for 4 brick courses)
for y_line in (39.5, 54.0, 68.5):
    draw_round_segment((12.4, y_line), (79.6, y_line), width_units=mortar_w, color=DARK)

# 4. Staggered vertical brick joints per course
# Course 4 (top, y=68.5..83.0)
for x_joint in (34.0, 58.0):
    draw_round_segment((x_joint, 68.5), (x_joint, 82.6), width_units=mortar_w, color=DARK)

# Course 3 (y=54.0..68.5)
for x_joint in (23.0, 46.0, 69.0):
    draw_round_segment((x_joint, 54.0), (x_joint, 68.5), width_units=mortar_w, color=DARK)

# Course 2 (y=39.5..54.0)
for x_joint in (34.0, 58.0):
    draw_round_segment((x_joint, 39.5), (x_joint, 54.0), width_units=mortar_w, color=DARK)

# Course 1 (bottom, y=25.0..39.5)
for x_joint in (23.0, 46.0, 69.0):
    draw_round_segment((x_joint, 25.4), (x_joint, 39.5), width_units=mortar_w, color=DARK)

# 5. Brick wall crisp outer border
rectangle(
    (wall_cx, wall_cy),
    width=wall_w,
    height=wall_h,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w_shape, shape_r=wall_r),
)

# 6. Foreground bottom-right security shield
cx = 64.0
y_bot, y_top = 14.0, 58.0
half_w = 19.0

left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(full_outline, width_units=w_shape, color=DARK, closed=True)

# 7. Inner WHITE badge circle with DARK checkmark inside the shield
circle(
    (cx, 38.0),
    radius=8.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)
draw_round_polyline(
    [(59.8, 37.8), (63.0, 34.5), (68.5, 41.0)],
    width_units=w_line,
    color=DARK,
)

save()
