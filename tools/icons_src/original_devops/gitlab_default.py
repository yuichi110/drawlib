# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: gitlab."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_inner = 1.65
scale = 0.95


def _sc(x: float, y: float) -> tuple[float, float]:
    return (50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale)


def _arc(xc: float, yc: float, r: float, deg0: float, deg1: float, steps: int = 12) -> list[tuple[float, float]]:
    return [
        _sc(
            xc + r * math.cos(math.radians(deg0 + (deg1 - deg0) * (i / steps))),
            yc + r * math.sin(math.radians(deg0 + (deg1 - deg0) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# Key structural vertices (in unscaled 100x100 space)
p_fl = _sc(34.80, 64.26)
p_fr = _sc(65.20, 64.26)
p_cl = _sc(10.47, 58.35)
p_cr = _sc(89.53, 58.35)

# Rounded ear tips (center at (24.59, 86.65) and (75.41, 86.65), r=2.83)
ear_l_tip = _arc(24.59, 86.65, 2.83, 160.0, 20.0, steps=10)
ear_r_tip = _arc(75.41, 86.65, 2.83, 160.0, 20.0, steps=10)

# Rounded nose tip (center at (50.0, 14.0), r=3.48)
nose_tip = _arc(50.00, 14.00, 3.48, 232.0, 308.0, steps=10)
p_nose = nose_tip[len(nose_tip) // 2]

# Rounded outer side curves (from official GitLab contour)
_LEFT_SIDE_RAW: list[tuple[float, float]] = [
    (10.47, 58.35),
    (9.97, 56.90),
    (9.61, 55.58),
    (9.34, 54.26),
    (9.16, 52.93),
    (9.06, 51.60),
    (9.05, 50.27),
    (9.13, 48.95),
    (9.29, 47.64),
    (9.54, 46.35),
    (9.86, 45.08),
    (10.27, 43.83),
    (10.75, 42.60),
    (11.31, 41.41),
    (11.95, 40.25),
    (12.66, 39.13),
    (13.45, 38.05),
    (14.31, 37.02),
    (15.24, 36.03),
    (16.25, 35.11),
    (17.32, 34.24),
    (34.43, 21.44),
]
left_side = [_sc(x, y) for x, y in _LEFT_SIDE_RAW]
right_side = [_sc(100.0 - x, y) for x, y in reversed(_LEFT_SIDE_RAW)]

# 1. Center facet (Colors.Red3)
center_facet = [p_fl, p_fr, p_nose]
polygon(center_facet, style=Icon.no_border_fill(Colors.Red3))

# 2. Inner cheek facets (Colors.Orange3)
left_cheek = [p_cl, p_fl, p_nose]
right_cheek = [p_fr, p_cr, p_nose]
polygon(left_cheek, style=Icon.no_border_fill(Colors.Orange3))
polygon(right_cheek, style=Icon.no_border_fill(Colors.Orange3))

# 3. Outer ears and outer sides (Colors.Amber3)
left_ear = [p_cl, *ear_l_tip, p_fl]
right_ear = [p_fr, *ear_r_tip, p_cr]
left_outer_side = [*left_side, *nose_tip[: len(nose_tip) // 2 + 1]]
right_outer_side = [*nose_tip[len(nose_tip) // 2 :], *right_side]

polygon(left_ear, style=Icon.no_border_fill(Colors.Amber3))
polygon(right_ear, style=Icon.no_border_fill(Colors.Amber3))
polygon(left_outer_side, style=Icon.no_border_fill(Colors.Amber3))
polygon(right_outer_side, style=Icon.no_border_fill(Colors.Amber3))

# 4. Internal facet seams (DARK, w_inner)
for p_start, p_end in (
    (p_cl, p_fl),
    (p_fr, p_cr),
    (p_fl, p_nose),
    (p_fr, p_nose),
    (p_cl, p_nose),
    (p_cr, p_nose),
):
    Icon.draw_round_segment(p_start, p_end, width_units=w_inner, color=Icon.DARK)

# 5. Outer fox silhouette border (DARK, w=1.9)
outer_fox = [
    *ear_l_tip,
    p_fl,
    p_fr,
    *ear_r_tip,
    *reversed(right_side),
    *reversed(nose_tip),
    *reversed(left_side),
]
Icon.draw_round_polyline(outer_fox, width_units=w, color=Icon.DARK, closed=True)

save()
