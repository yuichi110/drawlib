# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: pulsar."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    build_sparkle_4pt_polygon,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

CX, CY = 50.0, 50.0
R_MEDALLION = 39.0


def _wave_points_clipped(
    y_base: float,
    peak_h: float,
    sigma: float,
    steps: int = 48,
) -> list[tuple[float, float]]:
    """Generate pulsar wave curve clipped cleanly inside the circular medallion."""
    pts: list[tuple[float, float]] = []
    # Find exact x range where y_base is inside circle of radius R_MEDALLION
    dy_base = y_base - CY
    max_dx = math.sqrt(max(0.0, R_MEDALLION * R_MEDALLION - dy_base * dy_base)) - 0.2
    x_start = CX - max_dx
    x_end = CX + max_dx
    for i in range(steps + 1):
        x = x_start + (x_end - x_start) * (i / steps)
        dx_norm = (x - CX) / sigma
        y = y_base + peak_h * math.exp(-(dx_norm * dx_norm))
        pts.append((x, y))
    return pts


setup_icon()

w = 2.0

# 1. Circular dark-bordered sky medallion (Colors.Blue1)
circle(
    (CX, CY),
    radius=R_MEDALLION,
    style=fill_style(Colors.Blue1, border_color=DARK, border_units=w),
)

# 2. Upper horizon wave band (Colors.Blue3)
wave_top = _wave_points_clipped(y_base=37.5, peak_h=17.5, sigma=12.5)
wave_mid = _wave_points_clipped(y_base=27.5, peak_h=12.5, sigma=14.0)

# Connect wave_top right end to wave_mid right end along the circle rim, and same on left
ang_top_r = math.atan2(wave_top[-1][1] - CY, wave_top[-1][0] - CX)
ang_mid_r = math.atan2(wave_mid[-1][1] - CY, wave_mid[-1][0] - CX)
ang_mid_l = math.atan2(wave_mid[0][1] - CY, wave_mid[0][0] - CX)
ang_top_l = math.atan2(wave_top[0][1] - CY, wave_top[0][0] - CX)

right_rim = [
    (CX + R_MEDALLION * math.cos(ang_top_r + (ang_mid_r - ang_top_r) * (i / 6)),
     CY + R_MEDALLION * math.sin(ang_top_r + (ang_mid_r - ang_top_r) * (i / 6)))
    for i in range(1, 6)
]
left_rim = [
    (CX + R_MEDALLION * math.cos(ang_mid_l + (ang_top_l - ang_mid_l) * (i / 6)),
     CY + R_MEDALLION * math.sin(ang_mid_l + (ang_top_l - ang_mid_l) * (i / 6)))
    for i in range(1, 6)
]

band_upper = [*wave_top, *right_rim, *reversed(wave_mid), *left_rim]
polygon(band_upper, style=no_border_fill(Colors.Blue3))

# 3. Lower horizon wave band (Colors.Gray6) filling down to bottom circle rim
bot_arc: list[tuple[float, float]] = []
steps_arc = 32
for i in range(steps_arc + 1):
    ang = ang_mid_r + (ang_mid_l - ang_mid_r) * (i / steps_arc)
    bot_arc.append((CX + R_MEDALLION * math.cos(ang), CY + R_MEDALLION * math.sin(ang)))

band_lower = [*wave_mid, *bot_arc]
polygon(band_lower, style=no_border_fill(Colors.Gray6))

# 4. Crisp wave ridge lines + clean outer medallion ring
draw_round_polyline(wave_top, width_units=1.8, color=DARK)
draw_round_polyline(wave_mid, width_units=1.8, color=DARK)

circle_rim = [
    (CX + R_MEDALLION * math.cos(math.radians(a)), CY + R_MEDALLION * math.sin(math.radians(a)))
    for a in range(0, 360, 4)
]
draw_round_polyline(circle_rim, width_units=w, color=DARK, closed=True)

# 5. Center pulsar 4-point star peak (Colors.Teal3) with clear breathing space above wave crest
star_cx, star_cy = 50.0, 71.0
star_pts = build_sparkle_4pt_polygon(star_cx, star_cy, outer_r=10.8, inner_r=3.4)
polygon(star_pts, style=no_border_fill(Colors.Teal3))
draw_round_polyline(star_pts, width_units=1.7, color=DARK, closed=True)

# 6. Symmetrical radio-wave pulse arcs flanking the center star
for side in (-1.0, 1.0):
    arc_pts: list[tuple[float, float]] = []
    for i in range(13):
        ang = math.radians(-30.0 + 60.0 * (i / 12))
        rx = star_cx + side * 15.2 * math.cos(ang)
        ry = star_cy + 15.2 * math.sin(ang)
        arc_pts.append((rx, ry))
    draw_round_polyline(arc_pts, width_units=1.7, color=DARK)

save()
