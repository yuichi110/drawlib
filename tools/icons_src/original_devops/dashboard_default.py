# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: dashboard."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Wide observability dashboard base fill
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=58.0,
    style=Icon.fill_style(Icon.WHITE, shape_r=7.0),
)

# Top header bar
Gcp.draw_rounded_corner_block(
    13.0,
    65.0,
    87.0,
    79.0,
    r=7.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# Outer frame border and header divider
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=58.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)
Icon.draw_round_segment((13.0, 65.0), (87.0, 65.0), width_units=w, color=Icon.DARK)

# Header dots
for x_dot, col in ((22.0, Icon.PASTEL_GREEN), (30.5, Icon.WHITE)):
    circle(
        (x_dot, 72.0),
        radius=2.5,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=1.8),
    )

# Bottom-left gauge widget
circle(
    (32.0, 42.5),
    radius=12.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)
Icon.draw_round_segment((32.0, 42.5), (39.5, 50.0), width_units=2.0, color=Icon.DARK)
circle(
    (32.0, 42.5),
    radius=3.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8),
)

# Bottom-right 3 rising metric bars
bars = [
    (54.0, 11.0, Icon.PASTEL_BLUE_LIGHT),
    (64.0, 18.0, Icon.PASTEL_BLUE),
    (74.0, 25.0, Icon.PASTEL_GREEN),
]
for bx, bh, bcol in bars:
    rectangle(
        (bx, 30.0 + bh / 2.0),
        width=6.5,
        height=bh,
        style=Icon.fill_style(bcol, border_color=Icon.DARK, border_units=2.0, shape_r=1.5),
    )

save()
