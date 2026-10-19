# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: project_plan."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle, rhombus
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Gantt card background (x=12.5..87.5, y=16.0..84.0)
rectangle(
    (50.0, 50.0),
    width=75.0,
    height=68.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0),
)

# 2. Top PASTEL_BLUE header bar (y=70.0..84.0)
Gcp.draw_rounded_corner_block(
    12.5,
    70.0,
    87.5,
    84.0,
    r=6.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# 3. Header divider and outer frame border
Icon.draw_round_segment((12.5, 70.0), (87.5, 70.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (50.0, 50.0),
    width=75.0,
    height=68.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)

# 4. Header dots on left
for x_dot in (21.0, 29.0):
    circle(
        (x_dot, 77.0),
        radius=2.2,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
    )

# 5. Vertical milestone line at x=73.0 + top diamond marker
Icon.draw_round_segment((73.0, 16.0), (73.0, 70.0), width_units=w_inner, color=Icon.DARK)
rhombus(
    (73.0, 56.5),
    width=9.0,
    height=9.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner),
)

# 6. Three staggered horizontal timeline bars
timeline_bars = [
    # (cx, cy, width, fill_color)
    (32.5, 56.5, 25.0, Icon.PASTEL_BLUE),
    (46.5, 42.5, 27.0, Icon.PASTEL_GREEN),
    (59.0, 28.5, 28.0, Icon.PASTEL_BLUE_LIGHT),
]
for cx, cy, bw, col in timeline_bars:
    rectangle(
        (cx, cy),
        width=bw,
        height=8.8,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_inner, shape_r=4.4),
    )

save()
