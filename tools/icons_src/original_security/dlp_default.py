# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: dlp."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, ellipse, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w_shape = 2.0
w_line = 2.0

# 1. Left/center 2-tier database cylinder (x=11..51, y=24..78)
db_cx = 31.0
db_w = 40.0
db_half_w = db_w / 2.0
db_ry = 7.0
db_eh = db_ry * 2.0

y_bot = 24.0
y_mid = 52.0
y_top = 78.0

# Cylinder solid fills
ellipse((db_cx, y_bot), width=db_w, height=db_eh, style=fill_style(PASTEL_BLUE))
rectangle((db_cx, (y_bot + y_top) / 2.0), width=db_w, height=y_top - y_bot, style=fill_style(PASTEL_BLUE))

# Cylinder bottom arc and middle tier divider arc
for yc in (y_bot, y_mid):
    arc(
        (db_cx, yc),
        width=db_w,
        height=db_eh,
        angle_start=180.0,
        angle_end=360.0,
        style=stroke_style(DARK, width_units=w_shape),
    )

# Cylinder left vertical wall (continuous) and right vertical wall (with doorway for outbound arrow)
x_left = db_cx - db_half_w
x_right = db_cx + db_half_w
draw_round_segment((x_left, y_bot), (x_left, y_top), width_units=w_shape, color=DARK)
draw_round_segment((x_right, y_bot), (x_right, 30.2), width_units=w_shape, color=DARK)
draw_round_segment((x_right, 37.8), (x_right, y_top), width_units=w_shape, color=DARK)

# Cylinder top cap
ellipse(
    (db_cx, y_top),
    width=db_w,
    height=db_eh,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_shape),
)

# 2. Outbound right-pointing DARK arrow emerging from lower tier toward padlock
arrow_y = 34.0
arrow_start = (33.0, arrow_y)
arrow_tip = (59.5, arrow_y)
draw_round_segment(arrow_start, arrow_tip, width_units=w_line, color=DARK)

head_len = 6.0
head_angle_deg = 36.0
a1 = math.radians(180.0 - head_angle_deg)
a2 = math.radians(-180.0 + head_angle_deg)
p1 = (arrow_tip[0] + head_len * math.cos(a1), arrow_tip[1] + head_len * math.sin(a1))
p2 = (arrow_tip[0] + head_len * math.cos(a2), arrow_tip[1] + head_len * math.sin(a2))
draw_round_polyline([p1, arrow_tip, p2], width_units=w_line, color=DARK)

# 3. Bottom-right PASTEL_GREEN padlock blocking the outbound arrow (x=64..88)
lock_cx = 76.0
lock_cy = 34.0
lock_w = 24.0
lock_h = 20.0
lock_top = lock_cy + lock_h / 2.0

shackle_w = 13.0
shackle_h = 13.0
shackle_r = shackle_w / 2.0
shackle_cy = 49.5

draw_round_segment((lock_cx - shackle_r, lock_top), (lock_cx - shackle_r, shackle_cy), width_units=w_line, color=DARK)
draw_round_segment((lock_cx + shackle_r, lock_top), (lock_cx + shackle_r, shackle_cy), width_units=w_line, color=DARK)
arc(
    (lock_cx, shackle_cy),
    width=shackle_w,
    height=shackle_h,
    angle_start=0.0,
    angle_end=180.0,
    style=stroke_style(DARK, width_units=w_line),
)

rectangle(
    (lock_cx, lock_cy),
    width=lock_w,
    height=lock_h,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape, shape_r=4.0),
)

# 4. Keyhole in center of padlock body
circle((lock_cx, 35.8), radius=2.2, style=fill_style(DARK))
draw_round_segment((lock_cx, 35.8), (lock_cx, 30.8), width_units=w_line, color=DARK)

save()
