# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: cli_tool."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w_shape = 2.0

# 1. Rounded WHITE terminal window body (width=76, height=64, shape_r=6.0 at (50, 50))
# x=12..88, y=18..82
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0),
)

# 2. PASTEL_BLUE top title bar (height=14 at (50, 75) -> y=68..82)
Gcp.draw_rounded_corner_block(
    12.0,
    68.0,
    88.0,
    82.0,
    r=6.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# 3. Title bar divider and outer frame border
Icon.draw_round_segment((12.0, 68.0), (88.0, 68.0), width_units=w_shape, color=Icon.DARK)
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_shape, shape_r=6.0),
)

# 4. Two small WHITE window dots on left of title bar
for x_dot in (21.0, 29.5):
    circle(
        (x_dot, 75.0),
        radius=2.4,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
    )

# 5. Bold PASTEL_GREEN `>` chevron polygon inside terminal body (centered around y=43)
chevron_pts = [
    (42.5, 43.0),
    (30.5, 55.0),
    (25.5, 50.0),
    (32.5, 43.0),
    (25.5, 36.0),
    (30.5, 31.0),
]
polygon(chevron_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(chevron_pts, width_units=w_shape, color=Icon.DARK, closed=True)

# 6. Horizontal `_` cursor bar to the right of `>`
rectangle(
    (59.0, 34.0),
    width=22.0,
    height=6.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_shape, shape_r=2.5),
)

save()
