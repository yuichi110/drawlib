# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: bastion_host."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Main fortress / terminal body
rectangle(
    (50.0, 41.0),
    width=64.0,
    height=50.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.0),
)

# Top castle battlements / crenelations
battlement_pts = [
    (16.0, 64.0),
    (16.0, 84.0),
    (32.0, 84.0),
    (32.0, 74.0),
    (42.0, 74.0),
    (42.0, 84.0),
    (58.0, 84.0),
    (58.0, 74.0),
    (68.0, 74.0),
    (68.0, 84.0),
    (84.0, 84.0),
    (84.0, 64.0),
]
polygon(battlement_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(battlement_pts, width_units=w, color=DARK, closed=True)

# Inner SSH terminal screen
rectangle(
    (50.0, 40.0),
    width=48.0,
    height=32.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=4.5),
)

# Terminal prompt `>_`
draw_round_polyline(
    [(35.0, 46.5), (44.0, 40.0), (35.0, 33.5)],
    width_units=2.0,
    color=DARK,
)
draw_round_segment((49.0, 33.5), (62.0, 33.5), width_units=2.0, color=DARK)

save()
