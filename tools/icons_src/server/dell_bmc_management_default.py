# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_bmc_management_default."""

import math

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DELL_BLUE,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

BORDER = 4.8

# Top left rack server (x=15..46 bottom, x=15..85 top, y=62..87)
draw_round_polyline(
    [(82.6, 84.6), (17.4, 84.6), (17.4, 64.4), (43.6, 64.4)],
    width_units=BORDER,
    color=DELL_BLUE,
    corner_r=2.5,
)
rectangle(
    (40.5, 74.5),
    width=11.0,
    height=5.0,
    style=no_border_fill(DELL_BLUE),
)

# Middle left rack server (x=15..46 top, x=15..52 bottom, y=30..55)
draw_round_polyline(
    [(43.6, 52.6), (17.4, 52.6), (17.4, 32.4), (49.6, 32.4)],
    width_units=BORDER,
    color=DELL_BLUE,
    corner_r=2.5,
)
rectangle(
    (40.5, 42.5),
    width=11.0,
    height=5.0,
    style=no_border_fill(DELL_BLUE),
)

# Bottom left T-base (horizontal bar x=15..52, y=12..17 + vertical stem x=47..52, y=12..23)
rectangle(
    (33.5, 14.5),
    width=37.0,
    height=5.0,
    style=no_border_fill(DELL_BLUE),
)
rectangle(
    (49.5, 17.5),
    width=5.0,
    height=11.0,
    style=no_border_fill(DELL_BLUE),
)

# Foreground upright open-end wrench on the right (cx=69.0, y=12..78.5)
WRENCH_CX = 69.0
HEAD_CY = 62.5
R_OUT = 16.8
R_IN = 12.0
HW_OUT = 7.2
HW_IN = 2.4
R_CORNER = 2.4
BOT_CY = 12.0 + HW_OUT
JAW_FLOOR_Y = 64.0
JAW_IN_FLOOR_Y = JAW_FLOOR_Y - (R_OUT - R_IN)

# Exact jaw tip fillet center (internally tangent to R_OUT and tangent to x = WRENCH_CX +/- HW_IN)
dy_tip = math.sqrt((R_OUT - R_CORNER) ** 2 - (HW_IN + R_CORNER) ** 2)
tip_cy = HEAD_CY + dy_tip
ang_tip_l = math.degrees(math.atan2(dy_tip, -(HW_IN + R_CORNER)))
ang_tip_r = math.degrees(math.atan2(dy_tip, HW_IN + R_CORNER))
ang_neck_l = 270.0 - math.degrees(math.asin(HW_OUT / R_OUT))
ang_neck_r = 270.0 + math.degrees(math.asin(HW_OUT / R_OUT))

# Outer wrench contour (CCW)
outer_pts: list[tuple[float, float]] = [
    (WRENCH_CX + HW_IN, JAW_FLOOR_Y),
    (WRENCH_CX - HW_IN, JAW_FLOOR_Y),
]

# Left jaw tip fillet (0 deg to ang_tip_l around (WRENCH_CX - HW_IN - R_CORNER, tip_cy))
for i in range(11):
    ang = math.radians(ang_tip_l * (i / 10.0))
    outer_pts.append(
        (WRENCH_CX - HW_IN - R_CORNER + R_CORNER * math.cos(ang), tip_cy + R_CORNER * math.sin(ang))
    )

# Left head outer arc (ang_tip_l CCW down to ang_neck_l)
for i in range(1, 29):
    ang = math.radians(ang_tip_l + (ang_neck_l - ang_tip_l) * (i / 28.0))
    outer_pts.append((WRENCH_CX + R_OUT * math.cos(ang), HEAD_CY + R_OUT * math.sin(ang)))

# Bottom handle outer semicircle (180 deg CCW to 360 deg)
for i in range(25):
    ang = math.radians(180.0 + 180.0 * (i / 24.0))
    outer_pts.append((WRENCH_CX + HW_OUT * math.cos(ang), BOT_CY + HW_OUT * math.sin(ang)))

# Right head outer arc (ang_neck_r CCW up to 360 + ang_tip_r)
ang_tip_r_ccw = 360.0 + ang_tip_r
for i in range(29):
    ang = math.radians(ang_neck_r + (ang_tip_r_ccw - ang_neck_r) * (i / 28.0))
    outer_pts.append((WRENCH_CX + R_OUT * math.cos(ang), HEAD_CY + R_OUT * math.sin(ang)))

# Right jaw tip fillet (ang_tip_r CCW to 180 deg around (WRENCH_CX + HW_IN + R_CORNER, tip_cy))
for i in range(1, 11):
    ang = math.radians(ang_tip_r + (180.0 - ang_tip_r) * (i / 10.0))
    outer_pts.append(
        (WRENCH_CX + HW_IN + R_CORNER + R_CORNER * math.cos(ang), tip_cy + R_CORNER * math.sin(ang))
    )

# Inner transparent wrench cutout (CCW)
inner_pts: list[tuple[float, float]] = []
dy_in_top = math.sqrt(R_IN**2 - HW_OUT**2)
ang_in_top_l = math.degrees(math.atan2(dy_in_top, -HW_OUT))
ang_in_top_r = 360.0 + math.degrees(math.atan2(dy_in_top, HW_OUT))
ang_in_neck_l = 270.0 - math.degrees(math.asin(HW_IN / R_IN))
ang_in_neck_r = 270.0 + math.degrees(math.asin(HW_IN / R_IN))

# Left inner head arc (ang_in_top_l CCW down to ang_in_neck_l)
for i in range(25):
    ang = math.radians(ang_in_top_l + (ang_in_neck_l - ang_in_top_l) * (i / 24.0))
    inner_pts.append((WRENCH_CX + R_IN * math.cos(ang), HEAD_CY + R_IN * math.sin(ang)))

# Bottom handle inner semicircle (180 deg CCW to 360 deg)
for i in range(17):
    ang = math.radians(180.0 + 180.0 * (i / 16.0))
    inner_pts.append((WRENCH_CX + HW_IN * math.cos(ang), BOT_CY + HW_IN * math.sin(ang)))

# Right inner head arc (ang_in_neck_r CCW up to ang_in_top_r)
for i in range(25):
    ang = math.radians(ang_in_neck_r + (ang_in_top_r - ang_in_neck_r) * (i / 24.0))
    inner_pts.append((WRENCH_CX + R_IN * math.cos(ang), HEAD_CY + R_IN * math.sin(ang)))

# Right inner jaw wall down to rounded inner jaw floor
for i in range(9):
    ang = math.radians(0.0 - 90.0 * (i / 8.0))
    inner_pts.append(
        (
            WRENCH_CX + HW_OUT - R_CORNER + R_CORNER * math.cos(ang),
            JAW_IN_FLOOR_Y + R_CORNER + R_CORNER * math.sin(ang),
        )
    )
for i in range(9):
    ang = math.radians(270.0 - 90.0 * (i / 8.0))
    inner_pts.append(
        (
            WRENCH_CX - HW_OUT + R_CORNER + R_CORNER * math.cos(ang),
            JAW_IN_FLOOR_Y + R_CORNER + R_CORNER * math.sin(ang),
        )
    )

draw_compound_polygon([outer_pts, inner_pts], color=DELL_BLUE)

save()
