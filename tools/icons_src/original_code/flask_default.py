# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: flask (default variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

SLATE_LID = "#62738B"
SLATE_SHADOW = "#8293AF"


def _catmull_rom(
    pts: list[tuple[float, float]],
    steps_per_seg: int = 12,
) -> list[tuple[float, float]]:
    """Interpolate smooth points through control points via Catmull-Rom spline."""
    if len(pts) < 3:
        return list(pts)
    ext = [pts[0], *pts, pts[-1]]
    out: list[tuple[float, float]] = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for s in range(steps_per_seg):
            t = s / steps_per_seg
            t2 = t * t
            t3 = t2 * t
            x = 0.5 * (
                (2.0 * p1[0])
                + (-p0[0] + p2[0]) * t
                + (2.0 * p0[0] - 5.0 * p1[0] + 4.0 * p2[0] - p3[0]) * t2
                + (-p0[0] + 3.0 * p1[0] - 3.0 * p2[0] + p3[0]) * t3
            )
            y = 0.5 * (
                (2.0 * p1[1])
                + (-p0[1] + p2[1]) * t
                + (2.0 * p0[1] - 5.0 * p1[1] + 4.0 * p2[1] - p3[1]) * t2
                + (-p0[1] + 3.0 * p1[1] - 3.0 * p2[1] + p3[1]) * t3
            )
            out.append((round(x, 2), round(y, 2)))
    out.append(pts[-1])
    return out


setup_icon()
w_outer = 2.0

# 1. Top finial knob (circle at top of lid)
circle(
    xy=(32.2, 85.2),
    radius=3.9,
    style=fill_style(SLATE_LID, border_color=DARK, border_units=w_outer),
)

# 2. Domed slate-blue lid sitting on the collar
dome_pts: list[tuple[float, float]] = []
for i in range(33):
    ang = math.pi * (1.0 - i / 32.0)
    dx = 32.2 + 13.0 * math.cos(ang)
    dy = 69.8 + 12.2 * math.sin(ang)
    dome_pts.append((round(dx, 2), round(dy, 2)))
polygon(dome_pts, style=no_border_fill(SLATE_LID))
draw_round_polyline(dome_pts, width_units=w_outer, color=DARK, closed=True)

# 3. Curved white horn body
horn_pts = _catmull_rom(
    [
        (18.9, 65.0),
        (19.0, 59.6),
        (19.6, 52.5),
        (20.8, 45.8),
        (22.8, 39.5),
        (25.8, 33.2),
        (29.8, 27.2),
        (35.0, 21.6),
        (41.8, 16.8),
        (50.5, 13.2),
        (60.8, 11.4),
        (71.5, 11.6),
        (80.6, 13.4),
        (84.4, 15.2),
        (84.6, 17.0),
        (82.2, 18.2),
        (74.8, 18.6),
        (66.5, 20.4),
        (59.6, 23.6),
        (53.8, 28.4),
        (49.5, 34.6),
        (46.8, 41.8),
        (45.2, 49.6),
        (44.8, 57.2),
        (45.5, 65.0),
    ],
    steps_per_seg=10,
)
polygon(horn_pts, style=no_border_fill(WHITE))
draw_round_polyline(horn_pts, width_units=w_outer, color=DARK, closed=True)

# 4. Smooth slate-blue crescent shadow inside the horn body (no border)
shadow_outer = _catmull_rom(
    [
        (26.8, 60.8),
        (25.2, 54.5),
        (24.8, 48.0),
        (25.8, 41.2),
        (28.0, 34.8),
        (31.5, 28.8),
        (36.6, 23.4),
        (43.2, 19.2),
        (49.2, 16.8),
    ],
    steps_per_seg=8,
)
shadow_inner = _catmull_rom(
    [
        (49.2, 16.8),
        (43.8, 20.6),
        (38.8, 25.8),
        (34.6, 31.8),
        (31.2, 38.2),
        (28.9, 45.0),
        (27.6, 52.5),
        (26.8, 60.8),
    ],
    steps_per_seg=8,
)
polygon([*shadow_outer, *shadow_inner[1:-1]], style=no_border_fill(SLATE_SHADOW))

# 5. White rim collar with right spout
collar_pts: list[tuple[float, float]] = []
for i in range(13):
    ang = 0.5 * math.pi + math.pi * (i / 12.0)
    cx = 17.6 + 2.6 * math.cos(ang)
    cy = 67.4 + 2.6 * math.sin(ang)
    collar_pts.append((round(cx, 2), round(cy, 2)))

spout_curve = _catmull_rom(
    [
        (47.8, 64.8),
        (48.6, 66.8),
        (50.2, 68.4),
        (52.2, 69.3),
        (52.4, 70.0),
        (50.8, 70.0),
    ],
    steps_per_seg=6,
)
collar_pts.extend(spout_curve)
polygon(collar_pts, style=no_border_fill(WHITE))
draw_round_polyline(collar_pts, width_units=w_outer, color=DARK, closed=True)

save()
