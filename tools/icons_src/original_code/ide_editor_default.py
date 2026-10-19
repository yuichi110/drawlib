# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: ide_editor."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w_shape = 2.0

# 1. Wide WHITE editor window body (width=78, height=64, shape_r=6.0 at (50, 50))
# x=11..89, y=18..82
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=64.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0),
)

# 2. PASTEL_BLUE_LIGHT left sidebar pane (x=11..30, y=18..68)
Gcp.draw_rounded_corner_block(
    11.0,
    18.0,
    30.0,
    68.0,
    r=6.0,
    round_bl=True,
    color=Icon.PASTEL_BLUE_LIGHT,
)

# 3. PASTEL_BLUE top header bar (x=11..89, y=68..82)
Gcp.draw_rounded_corner_block(
    11.0,
    68.0,
    89.0,
    82.0,
    r=6.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# 4. Header divider, sidebar divider, and outer window border
Icon.draw_round_segment((11.0, 68.0), (89.0, 68.0), width_units=w_shape, color=Icon.DARK)
Icon.draw_round_segment((30.0, 18.0), (30.0, 68.0), width_units=w_shape, color=Icon.DARK)
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=64.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_shape, shape_r=6.0),
)

# 5. Two small WHITE window dots in top-left of header bar
for x_dot in (19.5, 27.5):
    circle(
        (x_dot, 75.0),
        radius=2.3,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
    )

# 6. Three subtle file-tree indicator lines in left sidebar pane
for y_side in (57.0, 48.0, 39.0):
    Icon.draw_round_segment((16.5, y_side), (24.5, y_side), width_units=w_shape, color=Icon.DARK)

# 7. Four horizontal syntax-highlighted code pill bars in main editor pane
code_pills = [
    # (cx, cy, width, fill_color)
    (50.0, 58.0, 28.0, Icon.PASTEL_BLUE),
    (60.0, 48.0, 36.0, Icon.PASTEL_GREEN),
    (57.0, 38.0, 30.0, Icon.PASTEL_BLUE_LIGHT),
    (47.0, 28.0, 22.0, Icon.WHITE),
]
for cx, cy, pw, col in code_pills:
    rectangle(
        (cx, cy),
        width=pw,
        height=5.6,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_shape, shape_r=2.8),
    )

save()
