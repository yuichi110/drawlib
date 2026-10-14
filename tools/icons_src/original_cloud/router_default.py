# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: router."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

draw_cylinder_tier(
    50.0,
    36.0,
    width=72.0,
    body_h=22.0,
    ry=16.0,
    body_color=PASTEL_BLUE,
    top_color=WHITE,
    border_color=DARK,
    border_units=w,
)

for led_x in (36.0, 64.0):
    circle(
        (led_x, 35.0),
        radius=3.5,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
    )

aw = 2.4
# Left and right horizontal arrows on top ellipse (center=(50.0, 58.0))
draw_round_segment((26.0, 58.0), (43.0, 58.0), width_units=aw, color=DARK)
draw_round_polyline([(32.0, 62.5), (26.0, 58.0), (32.0, 53.5)], width_units=aw, color=DARK)

draw_round_segment((57.0, 58.0), (74.0, 58.0), width_units=aw, color=DARK)
draw_round_polyline([(68.0, 62.5), (74.0, 58.0), (68.0, 53.5)], width_units=aw, color=DARK)

# Up and down vertical arrows on top ellipse
draw_round_segment((50.0, 62.0), (50.0, 70.0), width_units=aw, color=DARK)
draw_round_polyline([(45.5, 66.0), (50.0, 70.0), (54.5, 66.0)], width_units=aw, color=DARK)

draw_round_segment((50.0, 46.0), (50.0, 54.0), width_units=aw, color=DARK)
draw_round_polyline([(45.5, 50.0), (50.0, 46.0), (54.5, 50.0)], width_units=aw, color=DARK)

save()
