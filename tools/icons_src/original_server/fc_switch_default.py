# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: fc_switch."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Wide low-profile SAN switch chassis
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=44.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)

# Inner white fabric panel
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=32.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.5),
)

# Crossing X-fabric lines between corner port junctions
Icon.draw_round_segment((32.0, 42.0), (68.0, 58.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((32.0, 58.0), (68.0, 42.0), width_units=2.0, color=Icon.DARK)

# 4 outward horizontal fabric arrows pointing left/right
for y_port in (42.0, 58.0):
    Cisco.draw_arrow(
        (32.0, y_port),
        (20.5, y_port),
        shaft_w=2.4,
        head_len=5.0,
        head_w=6.6,
        color=Icon.DARK,
    )
    Cisco.draw_arrow(
        (68.0, y_port),
        (79.5, y_port),
        shaft_w=2.4,
        head_len=5.0,
        head_w=6.6,
        color=Icon.DARK,
    )

# Central pastel green SAN fabric ring/node
circle(
    (50.0, 50.0),
    radius=6.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
