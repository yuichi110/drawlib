# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: nosql_database."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx = 50.0
width = 68.0
w_half = width / 2.0
ry = 10.0
eh = ry * 2.0
y_bot = 20.0
y_top = 76.0
body_h = y_top - y_bot

# 1. Single bold cylinder body
ellipse(
    (cx, y_bot),
    width=width,
    height=eh,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (cx, y_bot + body_h / 2.0),
    width=width,
    height=body_h,
    style=Icon.fill_style(Icon.PASTEL_BLUE),
)
Icon.draw_round_segment((cx - w_half, y_bot), (cx - w_half, y_top), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((cx + w_half, y_bot), (cx + w_half, y_top), width_units=w, color=Icon.DARK)

ellipse(
    (cx, y_top),
    width=width,
    height=eh,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

# 2. Front rounded document/JSON badge
badge_cy = 43.0
rectangle(
    (cx, badge_cy),
    width=42.0,
    height=28.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=6.0),
)

# 3. Geometric curly braces { } and center accent dot
left_brace = [
    (42.5, 51.0),
    (39.0, 51.0),
    (39.0, 45.2),
    (36.0, 43.0),
    (39.0, 40.8),
    (39.0, 35.0),
    (42.5, 35.0),
]
right_brace = [
    (57.5, 51.0),
    (61.0, 51.0),
    (61.0, 45.2),
    (64.0, 43.0),
    (61.0, 40.8),
    (61.0, 35.0),
    (57.5, 35.0),
]
Icon.draw_round_polyline(left_brace, width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(right_brace, width_units=2.0, color=Icon.DARK)

circle(
    (cx, badge_cy),
    radius=3.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
)

save()
