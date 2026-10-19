# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: web_browser."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer browser base fill
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=Icon.fill_style(Icon.WHITE, shape_r=7.0),
)

# Top browser header fill
Gcp.draw_rounded_corner_block(
    12.0,
    64.0,
    88.0,
    82.0,
    r=7.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# Outer frame border and header divider
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)
Icon.draw_round_segment((12.0, 64.0), (88.0, 64.0), width_units=w, color=Icon.DARK)

# Window control dots
for x_dot, col in ((22.0, Icon.PASTEL_GREEN), (31.0, Icon.WHITE), (40.0, Icon.WHITE)):
    circle(
        (x_dot, 73.0),
        radius=2.8,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=1.8),
    )

# Content area hero block and text lines
rectangle(
    (36.0, 41.0),
    width=26.0,
    height=26.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=3.5),
)
Icon.draw_round_segment((57.0, 48.0), (77.0, 48.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((57.0, 34.0), (72.0, 34.0), width_units=2.0, color=Icon.DARK)

save()
