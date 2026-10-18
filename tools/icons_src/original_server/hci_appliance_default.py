# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: hci_appliance."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_iso_cube,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Interconnect bus from bottom chassis to VM cube and storage disk
draw_round_segment((50.0, 31.0), (50.0, 42.0), width_units=w, color=DARK)
draw_round_polyline(
    [(30.0, 50.0), (30.0, 42.0), (70.0, 42.0), (70.0, 50.0)],
    width_units=w,
    color=DARK,
)

# Bottom physical 1U server chassis
rectangle(
    (50.0, 22.0),
    width=74.0,
    height=18.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.5),
)
rectangle(
    (31.0, 22.0),
    width=24.0,
    height=7.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.0),
)
draw_round_segment((49.0, 22.0), (61.0, 22.0), width_units=2.0, color=DARK)
circle(
    (75.0, 22.0),
    radius=3.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# Top-left 3D isometric VM cube
draw_iso_cube(
    30.0,
    63.5,
    radius=16.5,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=2.0,
)

# Top-right 3D storage disk cylinder
draw_cylinder_tier(
    70.0,
    52.5,
    width=28.0,
    body_h=19.5,
    ry=5.5,
    body_color=PASTEL_BLUE,
    top_color=WHITE,
    border_color=DARK,
    border_units=2.0,
)

save()
