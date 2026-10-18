# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: optical_transport."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cisco_arrow,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Wide 2D optical DWDM/ROADM shelf
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=52.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)

# Right optical plate
rectangle(
    (65.0, 50.0),
    width=28.0,
    height=34.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=5.0),
)

# 3 parallel horizontal wavelength arrows emerging from prism right edge
for x_start, y_pos in [(27.5, 60.0), (42.0, 50.0), (27.5, 40.0)]:
    draw_cisco_arrow(
        (x_start, y_pos),
        (76.0, y_pos),
        shaft_w=2.4,
        head_len=5.5,
        head_w=7.0,
        color=DARK,
    )

# Left optical prism triangle (drawn over arrow roots for a clean edge)
prism_pts = [(20.0, 34.0), (20.0, 66.0), (44.0, 50.0)]
polygon(prism_pts, style=fill_style(PASTEL_GREEN))
draw_round_polyline(prism_pts, width_units=2.0, color=DARK, closed=True)

save()
