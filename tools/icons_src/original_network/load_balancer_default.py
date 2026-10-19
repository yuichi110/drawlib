# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: load_balancer."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer rounded appliance box
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=10.0),
)

# Inner white panel
rectangle(
    (50.0, 50.0),
    width=62.0,
    height=50.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=6.0),
)

# Split branches from x=46.0 to top (y=63.0) and bottom (y=37.0) output arrows
Icon.draw_round_polyline(
    [(46.0, 50.0), (46.0, 63.0), (63.0, 63.0)],
    width_units=2.0,
    color=Icon.DARK,
    corner_r=4.5,
)
Icon.draw_round_polyline(
    [(46.0, 50.0), (46.0, 37.0), (63.0, 37.0)],
    width_units=2.0,
    color=Icon.DARK,
    corner_r=4.5,
)

# 3 right output arrows (middle shaft spans from input node center at x=29.0)
Cisco.draw_arrow(
    (29.0, 50.0),
    (73.0, 50.0),
    shaft_w=2.4,
    head_len=5.2,
    head_w=6.8,
    color=Icon.DARK,
)
for ty in (63.0, 37.0):
    Cisco.draw_arrow(
        (54.0, ty),
        (73.0, ty),
        shaft_w=2.4,
        head_len=5.2,
        head_w=6.8,
        color=Icon.DARK,
    )

# Left input node circle
circle(
    (29.0, 50.0),
    radius=6.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
