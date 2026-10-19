# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: secret_vault."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# U-shaped shackle at top: outer arc (r=17, x=33..67, top y=84) + inner arc (r=8.5, x=41.5..58.5)
shackle_cy = 67.0
r_out = 17.0
r_in = 8.5

outer_arc = [
    (
        50.0 + r_out * math.cos(math.radians(deg)),
        shackle_cy + r_out * math.sin(math.radians(deg)),
    )
    for deg in range(180, -1, -6)
]
inner_arc = [
    (
        50.0 + r_in * math.cos(math.radians(deg)),
        shackle_cy + r_in * math.sin(math.radians(deg)),
    )
    for deg in range(0, 181, 6)
]
shackle_pts = [
    (50.0 - r_out, 52.0),
    *outer_arc,
    (50.0 + r_out, 52.0),
    (50.0 + r_in, 52.0),
    *inner_arc,
    (50.0 - r_in, 52.0),
]
polygon(shackle_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(shackle_pts, width_units=w, color=Icon.DARK, closed=True)

# Main padlock body
rectangle(
    (50.0, 38.0),
    width=60.0,
    height=44.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Center keyhole badge
Icon.draw_round_segment((50.0, 34.0), (50.0, 26.0), width_units=3.2, color=Icon.DARK)
circle(
    (50.0, 42.0),
    radius=8.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
circle(
    (50.0, 42.0),
    radius=4.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN),
)

save()
