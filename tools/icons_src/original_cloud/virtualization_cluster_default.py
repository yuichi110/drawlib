# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: virtualization_cluster."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Shared cluster interconnect bus and vertical stems
Icon.draw_round_segment((24.0, 41.0), (76.0, 41.0), width_units=w, color=Icon.DARK)
for x_host in (31.0, 69.0):
    Icon.draw_round_segment((x_host, 24.0), (x_host, 41.0), width_units=w, color=Icon.DARK)
for x_vm, y_vm in ((24.0, 51.0), (50.0, 60.0), (76.0, 51.0)):
    Icon.draw_round_segment((x_vm, 41.0), (x_vm, y_vm), width_units=w, color=Icon.DARK)

# Center HA cluster node on the interconnect bus
circle(
    (50.0, 41.0),
    radius=4.8,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

# 2 physical host blades at the base
for x_host in (31.0, 69.0):
    rectangle(
        (x_host, 23.0),
        width=34.0,
        height=14.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=3.5),
    )
    Icon.draw_round_segment((x_host - 10.0, 23.0), (x_host + 1.0, 23.0), width_units=2.0, color=Icon.DARK)
    circle(
        (x_host + 9.5, 23.0),
        radius=2.7,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
    )

# 3 coordinated isometric 3D VM cubes above the cluster bus
vms = [
    (24.0, 63.0, Icon.PASTEL_GREEN),
    (50.0, 72.0, Icon.PASTEL_BLUE_LIGHT),
    (76.0, 63.0, Icon.PASTEL_GREEN),
]
for cx, cy, r_col in vms:
    Icon.draw_iso_cube(
        cx,
        cy,
        radius=12.6,
        top_color=Icon.WHITE,
        left_color=Icon.PASTEL_BLUE,
        right_color=r_col,
        border_color=Icon.DARK,
        border_units=2.0,
    )

save()
