# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_run."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_BLUE, GCP_GREEN, GCP_RED, GCP_YELLOW, fill_style, setup_icon

setup_icon()

steps = 28

x_mid_l, y_mid = 25.0, 50.0
x_cap_l, y_cap_top = 10.8, 86.2
r_l = 3.5
dx_l = x_cap_l - x_mid_l
dy_l = y_cap_top - y_mid
len_l = math.hypot(dx_l, dy_l)
hw_l = r_l * len_l / dy_l

ang_dir_l = math.degrees(math.atan2(dy_l, dx_l))
ang_norm_l = ang_dir_l - 90.0

yellow_pts: list[tuple[float, float]] = [
    (x_mid_l - hw_l, 49.8),
    (x_mid_l + hw_l, 49.8),
]
for i in range(steps + 1):
    ang = math.radians(ang_norm_l + 180.0 * (i / steps))
    yellow_pts.append((x_cap_l + r_l * math.cos(ang), y_cap_top + r_l * math.sin(ang)))
polygon(yellow_pts, style=fill_style(GCP_YELLOW))

green_pts: list[tuple[float, float]] = [
    (x_mid_l - hw_l, 50.0),
    (x_mid_l + hw_l, 50.0),
]
for i in range(steps + 1):
    ang = math.radians(ang_norm_l + 180.0 * (i / steps))
    px = x_cap_l + r_l * math.cos(ang)
    py = 100.0 - (y_cap_top + r_l * math.sin(ang))
    green_pts.append((px, py))
polygon(green_pts, style=fill_style(GCP_GREEN))

x_tl, y_tl = 34.4, 85.8
r_tl = 4.0
x_back_out = 46.2
x_back_in = 53.6
x_cut_tl, y_cut_tl = 41.6, 75.8
x_cut_r = 83.2
x_tip_c, y_tip_c = 89.8, 50.0
r_tip = 2.6

dx_b = x_tl - x_back_out
dy_b = y_tl - 50.0
ang_tl_start = math.degrees(math.atan2(dy_b, dx_b)) + 90.0

dx_f = x_tip_c - x_tl
dy_f = y_tip_c - y_tl
ang_front_norm = math.degrees(math.atan2(dy_f, dx_f)) + 90.0


def _build_half_arrow(y_split: float, mirror_y: bool) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = [(x_back_out, y_split)]
    for i in range(steps + 1):
        ang = math.radians(ang_tl_start - (ang_tl_start - ang_front_norm) * (i / steps))
        pts.append((x_tl + r_tl * math.cos(ang), y_tl + r_tl * math.sin(ang)))
    for i in range(steps + 1):
        ang = math.radians(ang_front_norm * (1.0 - i / steps))
        pts.append((x_tip_c + r_tip * math.cos(ang), y_tip_c + r_tip * math.sin(ang)))
    pts.extend(
        [
            (x_cut_r, y_split),
            (x_cut_tl, y_cut_tl),
            (x_back_in, y_split),
        ]
    )
    if mirror_y:
        return [(px, 100.0 - py) for (px, py) in pts]
    return pts


polygon(_build_half_arrow(49.8, mirror_y=False), style=fill_style(GCP_RED))
polygon(_build_half_arrow(50.0, mirror_y=True), style=fill_style(GCP_BLUE))

save()
