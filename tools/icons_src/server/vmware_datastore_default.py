# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_datastore_default."""

from drawlib.canvas import save
from drawlib.shapes import arc, ellipse
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    draw_round_segment,
    setup_icon,
    stroke_style,
)

setup_icon()

cx = 50.0
width = 72.0
ry = 9.5
eh = ry * 2.0
y_bot_c = 12.0 + ry  # 21.5
y_top_c = 88.0 - ry  # 78.5
x_left = cx - width / 2.0
x_right = cx + width / 2.0

# Two horizontal waist curves across the cylinder body (y=58 and y=39)
for waist_cy in (59.5, 40.5):
    arc(
        (cx, waist_cy),
        width=width,
        height=eh,
        angle_start=180.0,
        angle_end=360.0,
        style=stroke_style(VMWARE_CYAN, width_units=4.4),
    )

# Outer structural cylinder outline (bottom arc, side walls, and full top ellipse)
arc(
    (cx, y_bot_c),
    width=width,
    height=eh,
    angle_start=180.0,
    angle_end=360.0,
    style=stroke_style(VMWARE_NAVY, width_units=4.6),
)
draw_round_segment((x_left, y_bot_c), (x_left, y_top_c), width_units=4.6, color=VMWARE_NAVY)
draw_round_segment((x_right, y_bot_c), (x_right, y_top_c), width_units=4.6, color=VMWARE_NAVY)
ellipse(
    (cx, y_top_c),
    width=width,
    height=eh,
    style=stroke_style(VMWARE_NAVY, width_units=4.6),
)

save()
