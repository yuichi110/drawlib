# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: voice_call."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# Rotated frame at -45 deg around (40.5, 40.5)
cx0, cy0 = 40.5, 40.5
s2 = math.sqrt(0.5)


def _to_xy(u: float, v: float) -> tuple[float, float]:
    return (cx0 + (u + v) * s2, cy0 + (-u + v) * s2)


def _local_arc(
    uc: float,
    vc: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 8,
) -> list[tuple[float, float]]:
    return [
        _to_xy(
            uc + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            vc + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Curved telephone handset (PASTEL_BLUE)
# Exact G1-tangent circular back curve: center (0, 19.5), R=31.0; corner circles at (+-22.0, 3.0), r=3.5
# (since 22.0^2 + 16.5^2 = 27.5^2 = (31.0 - 3.5)^2, exact 3-4-5 right triangle!)
ang_t = math.degrees(math.atan2(-16.5, 22.0))  # -36.8698976 deg
r_pad = 3.5

# Inner grip curve: circular arc centered at (0, 19.5) with radius 22.0
ang_in = math.degrees(math.asin(11.5 / 22.0))
grip_curve = _local_arc(0.0, 19.5, 22.0, -90.0 - ang_in, -90.0 + ang_in, 18)

handset_pts: list[tuple[float, float]] = [
    # Right mouthpiece outer-back fillet (0 deg down to ang_t)
    *_local_arc(22.0, 3.0, r_pad, 0.0, ang_t, 6),
    # Pure circular outer back arch (from ang_t to -180 - ang_t)
    *_local_arc(0.0, 19.5, 31.0, ang_t, -180.0 - ang_t, 28)[1:-1],
    # Left earpiece outer-back fillet (-180 - ang_t to -180 deg)
    *_local_arc(-22.0, 3.0, r_pad, -180.0 - ang_t, -180.0, 6),
    # Left earpiece top-left fillet (180 deg to 90 deg)
    *_local_arc(-22.0, 5.5, r_pad, 180.0, 90.0, 6),
    # Left earpiece top-right fillet (90 deg to 0 deg)
    *_local_arc(-15.0, 5.5, r_pad, 90.0, 0.0, 6),
    # Inner concave grip curve
    *grip_curve,
    # Right mouthpiece top-left fillet (180 deg to 90 deg)
    *_local_arc(15.0, 5.5, r_pad, 180.0, 90.0, 6),
    # Right mouthpiece top-right fillet (90 deg to 0 deg)
    *_local_arc(22.0, 5.5, r_pad, 90.0, 0.0, 6),
]

polygon(handset_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(handset_pts, width_units=w_outer, color=DARK, closed=True)

# Subtle inner receiver cap lines on earpiece & mouthpiece
draw_round_segment(_to_xy(-22.5, 4.5), _to_xy(-14.5, 4.5), width_units=w_inner, color=DARK)
draw_round_segment(_to_xy(14.5, 4.5), _to_xy(22.5, 4.5), width_units=w_inner, color=DARK)


# 2. Three concentric PASTEL_GREEN / DARK sound wave arcs radiating to top-right
def _wave_band(
    cx: float,
    cy: float,
    r_mid: float,
    half_t: float,
    deg_start: float,
    deg_end: float,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    steps_arc = 18
    steps_cap = 10
    r_in = r_mid - half_t
    r_out = r_mid + half_t

    for i in range(steps_arc + 1):
        ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps_arc))
        pts.append((cx + r_out * math.cos(ang), cy + r_out * math.sin(ang)))

    ec_x = cx + r_mid * math.cos(math.radians(deg_end))
    ec_y = cy + r_mid * math.sin(math.radians(deg_end))
    for i in range(1, steps_cap):
        ang = math.radians(deg_end + 180.0 * (i / steps_cap))
        pts.append((ec_x + half_t * math.cos(ang), ec_y + half_t * math.sin(ang)))

    for i in range(steps_arc + 1):
        ang = math.radians(deg_end - (deg_end - deg_start) * (i / steps_arc))
        pts.append((cx + r_in * math.cos(ang), cy + r_in * math.sin(ang)))

    sc_x = cx + r_mid * math.cos(math.radians(deg_start))
    sc_y = cy + r_mid * math.sin(math.radians(deg_start))
    for i in range(1, steps_cap):
        ang = math.radians(deg_start + 180.0 + 180.0 * (i / steps_cap))
        pts.append((sc_x + half_t * math.cos(ang), sc_y + half_t * math.sin(ang)))

    return pts


for r_wave in (14.5, 24.0, 33.5):
    w_pts = _wave_band(51.5, 51.5, r_wave, 2.1, 14.0, 76.0)
    polygon(w_pts, style=no_border_fill(PASTEL_GREEN))
    draw_round_polyline(w_pts, width_units=w_inner, color=DARK, closed=True)

save()
