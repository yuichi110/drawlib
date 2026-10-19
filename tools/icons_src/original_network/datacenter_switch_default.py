# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: datacenter_switch."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Wide spine/leaf fabric switch chassis
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=54.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Inner white fabric panel
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=42.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=5.0),
)

# Crossing X-fabric lines between the 4 corner port nodes
Icon.draw_round_segment((34.0, 39.0), (66.0, 61.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((34.0, 61.0), (66.0, 39.0), width_units=2.0, color=Icon.DARK)

# Outward horizontal fabric arrows from the 4 X-corners
for y_port in (39.0, 61.0):
    Cisco.draw_arrow(
        (34.0, y_port),
        (21.0, y_port),
        shaft_w=2.8,
        head_len=5.5,
        head_w=7.2,
        color=Icon.DARK,
    )
    Cisco.draw_arrow(
        (66.0, y_port),
        (79.0, y_port),
        shaft_w=2.8,
        head_len=5.5,
        head_w=7.2,
        color=Icon.DARK,
    )

# 4 corner port dots at the X junctions
for x_port in (34.0, 66.0):
    for y_port in (39.0, 61.0):
        circle(
            (x_port, y_port),
            radius=3.2,
            style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8),
        )

# Central pastel green fabric hub node
circle(
    (50.0, 50.0),
    radius=6.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
