# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: virtual_switch."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Vertical port stems from top 2 VMs down to virtual switch chassis
for x_port in (32.0, 68.0):
    Icon.draw_round_segment((x_port, 51.0), (x_port, 62.0), width_units=w, color=Icon.DARK)

# Central wide virtual switch chassis
rectangle(
    (50.0, 34.0),
    width=76.0,
    height=34.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=6.5),
)

# Inner WHITE switch fabric panel
rectangle(
    (50.0, 34.0),
    width=64.0,
    height=22.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.0),
)

# Opposing horizontal switching arrows inside switch panel
Cisco.draw_arrow(
    (25.0, 39.2),
    (75.0, 39.2),
    shaft_w=2.4,
    head_len=6.6,
    head_w=5.8,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (75.0, 28.8),
    (25.0, 28.8),
    shaft_w=2.4,
    head_len=6.6,
    head_w=5.8,
    color=Icon.DARK,
)

# Central PASTEL_GREEN virtual bridge dot
circle(
    (50.0, 34.0),
    radius=2.6,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
)

# Top 2 virtual machine 3D isometric cubes
for x_vm in (32.0, 68.0):
    Icon.draw_iso_cube(
        x_vm,
        72.0,
        radius=13.0,
        top_color=Icon.WHITE,
        left_color=Icon.PASTEL_BLUE,
        right_color=Icon.PASTEL_BLUE_LIGHT,
        border_color=Icon.DARK,
        border_units=2.0,
    )

save()
