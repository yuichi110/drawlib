# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: hr_portal."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Top lanyard clasp tab
rectangle(
    (50.0, 82.0),
    width=14.0,
    height=10.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.5),
)

# 2. Employee ID vertical card (WHITE body, x=22.0..78.0, y=14.0..80.0)
rectangle(
    (50.0, 47.0),
    width=56.0,
    height=66.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0),
)

# 3. Top PASTEL_BLUE header band (y=64.0..80.0)
Gcp.draw_rounded_corner_block(
    22.0,
    64.0,
    78.0,
    80.0,
    r=6.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# 4. Header divider, outer border, and WHITE lanyard slot pill
Icon.draw_round_segment((22.0, 64.0), (78.0, 64.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (50.0, 47.0),
    width=56.0,
    height=66.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)
rectangle(
    (50.0, 71.0),
    width=18.0,
    height=4.4,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner, shape_r=2.2),
)

# 5. PASTEL_GREEN user avatar circle & shoulders dome
circle(
    (50.0, 52.8),
    radius=6.8,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner),
)
dome_pts = [
    (
        50.0 + 13.0 * math.cos(math.radians(deg)),
        33.0 + 10.5 * math.sin(math.radians(deg)),
    )
    for deg in range(0, 181, 6)
]
polygon(dome_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(dome_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 6. Two horizontal DARK employee info lines
Icon.draw_round_segment((34.0, 25.0), (66.0, 25.0), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((39.0, 19.5), (61.0, 19.5), width_units=w_inner, color=Icon.DARK)

save()
