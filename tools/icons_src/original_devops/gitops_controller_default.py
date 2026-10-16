# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: gitops_controller."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Upper curved sync arrow (left Git repo -> right cluster)
upper_arc = [
    (
        50.0 + 25.0 * math.cos(math.radians(deg)),
        56.0 + 18.0 * math.sin(math.radians(deg)),
    )
    for deg in range(150, 29, -5)
]
draw_round_polyline(upper_arc, width_units=w, color=DARK)
draw_round_polyline(
    [(65.5, 66.5), upper_arc[-1], (72.5, 71.5)],
    width_units=2.4,
    color=DARK,
)

# Lower curved sync arrow (right cluster -> left Git repo)
lower_arc = [
    (
        50.0 + 25.0 * math.cos(math.radians(deg)),
        44.0 + 18.0 * math.sin(math.radians(deg)),
    )
    for deg in range(330, 209, -5)
]
draw_round_polyline(lower_arc, width_units=w, color=DARK)
draw_round_polyline(
    [(34.5, 33.5), lower_arc[-1], (27.5, 28.5)],
    width_units=2.4,
    color=DARK,
)

# Left Git repository node
rectangle(
    (22.0, 50.0),
    width=19.0,
    height=19.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.5),
)
circle(
    (22.0, 50.0),
    radius=3.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Right target cluster isometric cube
draw_iso_cube(
    77.0,
    50.0,
    radius=12.0,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=2.4,
)

# Central GitOps sync hub
circle(
    (50.0, 50.0),
    radius=10.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
circle(
    (50.0, 50.0),
    radius=3.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
