# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_template."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

# Back document sheet (x=24..88, y=18..90, clipped at front sheet) (vvd_icons/template.svg)
draw_round_polyline(
    [(24.0, 80.0), (24.0, 90.0), (88.0, 90.0), (88.0, 18.0), (76.0, 18.0)],
    width_units=4.2,
    color=VMWARE_NAVY,
    corner_r=1.5,
)

# Front folded-corner blueprint document (x=12..76, y=10..80, top-right fold (58,80)-(76,62))
front_pts = [
    (12.0, 10.0),
    (76.0, 10.0),
    (76.0, 62.0),
    (58.0, 80.0),
    (12.0, 80.0),
]
draw_round_polyline(front_pts, width_units=4.5, color=VMWARE_NAVY, closed=True)

# Top-right dog-ear fold crease
draw_round_polyline(
    [(58.0, 80.0), (58.0, 62.0), (76.0, 62.0)],
    width_units=4.2,
    color=VMWARE_NAVY,
)

# 3 small circular status rings in a row at y=56
for cx in (26.0, 38.0, 50.0):
    circle(
        (cx, 56.0),
        radius=3.8,
        style=fill_style(Colors.Transparent, border_color=VMWARE_CYAN, border_units=3.0),
    )

# Modular layout blocks below (y=26..44)
# 2 horizontal rectangles on left (x=22..44 at y=41 & y=29)
rectangle((33.0, 41.0), width=22.0, height=6.0, style=no_border_fill(VMWARE_CYAN, shape_r=0.8))
rectangle((33.0, 29.0), width=22.0, height=6.0, style=no_border_fill(VMWARE_CYAN, shape_r=0.8))
# 1 vertical rectangle on right (x=49..58, y=26..44)
rectangle((53.5, 35.0), width=9.0, height=18.0, style=no_border_fill(VMWARE_CYAN, shape_r=0.8))

# Bottom geometric line (replacing baked-in TEMPLATE text)
draw_round_segment((22.0, 18.0), (58.0, 18.0), width_units=3.4, color=VMWARE_NAVY)

save()
