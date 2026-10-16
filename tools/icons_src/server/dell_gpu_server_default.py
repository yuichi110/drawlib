# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_gpu_server_default."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DELL_BLUE,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

BORDER = 4.8

# PCIe GPU card body (outer x=24..89, y=20..78)
rectangle(
    (56.5, 49.0),
    width=65.0 - BORDER,
    height=58.0 - BORDER,
    style=fill_style(
        Colors.Transparent,
        border_color=DELL_BLUE,
        border_units=BORDER,
        shape_r=2.5,
    ),
)

# Left PCIe I/O bracket: top lip (x=11..28.8, y=78..82.8) + vertical spine (x=24..28.8, y=15..80.4)
draw_rounded_corner_block(
    11.0,
    78.0,
    28.8,
    78.0 + BORDER,
    r=2.5,
    round_tr=True,
    color=DELL_BLUE,
)
rectangle(
    (26.4, 47.7),
    width=BORDER,
    height=65.4,
    style=no_border_fill(DELL_BLUE),
)

# Two left PCIe port tabs (x=16..24 at y=58..66 and y=36..44)
for tab_cy in (62.0, 40.0):
    rectangle(
        (20.0, tab_cy),
        width=8.0,
        height=8.0,
        style=no_border_fill(DELL_BLUE),
    )

# Circular cooling fan centered at (56.0, 49.0)
FAN_CX = 56.0
FAN_CY = 49.0
FAN_RING_W = 4.6
FAN_R_CENTERLINE = 17.0 - FAN_RING_W / 2.0

circle(
    (FAN_CX, FAN_CY),
    radius=FAN_R_CENTERLINE,
    style=stroke_style(DELL_BLUE, width_units=FAN_RING_W),
)

# 4 angled tangential fan blades + center rotated diamond hub (hole radius ~4.5)
U_IN = 3.2
BLADE_W = 4.3
U_OUT = U_IN + BLADE_W
U_TIP = math.sqrt(FAN_R_CENTERLINE**2 - U_IN**2)

for k in range(4):
    ang = math.radians(45.0 + k * 90.0)
    ux, uy = math.cos(ang), math.sin(ang)
    vx, vy = -uy, ux

    # Bar spans u in [-U_OUT, U_TIP], v in [U_IN, U_OUT]
    local_pts = [
        (-U_OUT, U_IN),
        (U_TIP, U_IN),
        (U_TIP, U_OUT),
        (-U_OUT, U_OUT),
    ]
    world_pts = [
        (FAN_CX + u * ux + v * vx, FAN_CY + u * uy + v * vy)
        for u, v in local_pts
    ]
    polygon(world_pts, style=no_border_fill(DELL_BLUE))

save()
