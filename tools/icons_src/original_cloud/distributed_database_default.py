# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: distributed_database."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
hub_xy = (50.0, 50.0)
nodes = [
    (50.0, 76.0, Icon.PASTEL_GREEN),
    (26.0, 35.0, Icon.PASTEL_BLUE),
    (74.0, 35.0, Icon.PASTEL_BLUE),
]

# 1. Central network ring and radial spoke connectors
circle(
    hub_xy,
    radius=24.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w),
)

for nx, ny, _ in nodes:
    Icon.draw_round_segment(hub_xy, (nx, ny), width_units=w, color=Icon.DARK)

# 2. Central hub node at (50, 50)
circle(
    hub_xy,
    radius=6.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w),
)
circle(
    hub_xy,
    radius=2.5,
    style=Icon.fill_style(Icon.DARK),
)

# 3. Three mini database cylinders at triangle vertices
cyl_w = 26.0
w_half = cyl_w / 2.0
ry = 4.5
eh = ry * 2.0
body_h = 16.0
tier_h = body_h / 2.0

for cx, cy, body_col in nodes:
    y_bot = cy - body_h / 2.0
    y_mid = cy
    y_top = cy + body_h / 2.0

    for yb in (y_bot, y_mid):
        ellipse(
            (cx, yb),
            width=cyl_w,
            height=eh,
            style=Icon.fill_style(body_col, border_color=Icon.DARK, border_units=w),
        )
        rectangle(
            (cx, yb + tier_h / 2.0),
            width=cyl_w,
            height=tier_h,
            style=Icon.fill_style(body_col),
        )

    Icon.draw_round_segment((cx - w_half, y_bot), (cx - w_half, y_top), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((cx + w_half, y_bot), (cx + w_half, y_top), width_units=w, color=Icon.DARK)

    ellipse(
        (cx, y_top),
        width=cyl_w,
        height=eh,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
    )

save()
