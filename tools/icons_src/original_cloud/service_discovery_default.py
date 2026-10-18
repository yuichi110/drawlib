# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: service_discovery."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
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
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

cx, cy = 50.0, 50.0

# Outer compass / radar dial
circle(
    (cx, cy),
    radius=36.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# Inner radar ring
circle(
    (cx, cy),
    radius=26.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0),
)

# 4 cardinal tick marks
draw_round_segment((50.0, 86.0), (50.0, 79.5), width_units=2.0, color=DARK)
draw_round_segment((50.0, 14.0), (50.0, 20.5), width_units=2.0, color=DARK)
draw_round_segment((86.0, 50.0), (79.5, 50.0), width_units=2.0, color=DARK)
draw_round_segment((14.0, 50.0), (20.5, 50.0), width_units=2.0, color=DARK)

# Two-tone compass diamond needle (NE pointing to discovered service node, SW tail)
p_ne = (61.5, 61.5)
p_sw = (36.5, 36.5)
p_nw = (44.0, 56.0)
p_se = (56.0, 44.0)

polygon([p_nw, p_ne, p_se], style=fill_style(PASTEL_GREEN))
polygon([p_nw, p_sw, p_se], style=fill_style(PASTEL_BLUE))
draw_round_polyline([p_nw, p_ne, p_se, p_sw], width_units=2.0, color=DARK, closed=True)
draw_round_segment(p_nw, p_se, width_units=2.0, color=DARK)

# Center pivot
circle(
    (cx, cy),
    radius=3.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Discovered target service node at NE (70, 70)
circle(
    (70.0, 70.0),
    radius=6.8,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

save()
