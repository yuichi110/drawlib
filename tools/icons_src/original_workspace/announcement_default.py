# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: announcement."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# Megaphone local coordinate frame tilted upward by 14 deg
tilt_deg = 14.0
tilt_rad = math.radians(tilt_deg)
ux, uy = math.cos(tilt_rad), math.sin(tilt_rad)
nx, ny = -uy, ux
ox, oy = 21.0, 44.0


def _pt(u: float, v: float) -> tuple[float, float]:
    return (ox + u * ux + v * nx, oy + u * uy + v * ny)


def _local_arc(
    uc: float,
    vc: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 8,
) -> list[tuple[float, float]]:
    return [
        _pt(
            uc + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            vc + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Handle (PASTEL_BLUE_LIGHT) under megaphone throat
handle_pts: list[tuple[float, float]] = [
    _pt(5.0, -5.5),
    _pt(14.5, -8.5),
    *_local_arc(12.5, -21.5, 3.8, 0.0, -180.0, 12),
]
polygon(handle_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(handle_pts, width_units=w_outer, color=DARK, closed=True)

# 2. Rear nozzle cap (PASTEL_BLUE_LIGHT)
rear_pts: list[tuple[float, float]] = [
    _pt(1.0, -6.5),
    _pt(1.0, 6.5),
    *_local_arc(-2.5, 3.0, 3.5, 90.0, 180.0),
    *_local_arc(-2.5, -3.0, 3.5, 180.0, 270.0),
]
polygon(rear_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(rear_pts, width_units=w_outer, color=DARK, closed=True)

# 3. Main megaphone cone (PASTEL_BLUE)
cone_pts: list[tuple[float, float]] = [
    _pt(0.0, -6.5),
    _pt(40.0, -19.5),
    _pt(40.0, 19.5),
    _pt(0.0, 6.5),
]
polygon(cone_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(cone_pts, width_units=w_outer, color=DARK, closed=True)

# 4. Front rim (WHITE)
r_rim = 3.4
rim_pts: list[tuple[float, float]] = [
    *_local_arc(40.0 + r_rim, -22.5 + r_rim, r_rim, 180.0, 360.0, 10),
    *_local_arc(40.0 + r_rim, 22.5 - r_rim, r_rim, 0.0, 180.0, 10),
]
polygon(rim_pts, style=no_border_fill(WHITE))
draw_round_polyline(rim_pts, width_units=w_outer, color=DARK, closed=True)


# 5. Broadcast wave arcs (PASTEL_GREEN)
def _wave_band(
    uc: float,
    vc: float,
    r_mid: float,
    half_t: float,
    deg_start: float,
    deg_end: float,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    steps_arc = 16
    steps_cap = 8
    r_in = r_mid - half_t
    r_out = r_mid + half_t

    for i in range(steps_arc + 1):
        ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps_arc))
        pts.append(_pt(uc + r_out * math.cos(ang), vc + r_out * math.sin(ang)))

    ec_u = uc + r_mid * math.cos(math.radians(deg_end))
    ec_v = vc + r_mid * math.sin(math.radians(deg_end))
    for i in range(1, steps_cap):
        ang = math.radians(deg_end + 180.0 * (i / steps_cap))
        pts.append(_pt(ec_u + half_t * math.cos(ang), ec_v + half_t * math.sin(ang)))

    for i in range(steps_arc + 1):
        ang = math.radians(deg_end - (deg_end - deg_start) * (i / steps_arc))
        pts.append(_pt(uc + r_in * math.cos(ang), vc + r_in * math.sin(ang)))

    sc_u = uc + r_mid * math.cos(math.radians(deg_start))
    sc_v = vc + r_mid * math.sin(math.radians(deg_start))
    for i in range(1, steps_cap):
        ang = math.radians(deg_start + 180.0 + 180.0 * (i / steps_cap))
        pts.append(_pt(sc_u + half_t * math.cos(ang), sc_v + half_t * math.sin(ang)))

    return pts


for r_wave, deg_span in ((14.0, 28.0), (23.5, 32.0)):
    w_pts = _wave_band(43.5, 0.0, r_wave, 2.1, -deg_span, deg_span)
    polygon(w_pts, style=no_border_fill(PASTEL_GREEN))
    draw_round_polyline(w_pts, width_units=w_inner, color=DARK, closed=True)

save()
