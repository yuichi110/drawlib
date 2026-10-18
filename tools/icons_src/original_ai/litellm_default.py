# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: litellm."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
x0, y0, x1, y1 = 10.5, 10.5, 89.5, 89.5
r_badge = 12.0


def _arc(xc: float, yc: float, r: float, deg0: float, deg1: float, steps: int = 12) -> list[tuple[float, float]]:
    """Sample circular arc from deg0 to deg1."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = math.radians(deg0 + (deg1 - deg0) * (i / steps))
        pts.append((xc + r * math.cos(a), yc + r * math.sin(a)))
    return pts


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 18,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


badge_pts: list[tuple[float, float]] = [
    *_arc(x0 + r_badge, y0 + r_badge, r_badge, 180.0, 270.0),
    *_arc(x1 - r_badge, y0 + r_badge, r_badge, 270.0, 360.0),
    *_arc(x1 - r_badge, y1 - r_badge, r_badge, 0.0, 90.0),
    *_arc(x0 + r_badge, y1 - r_badge, r_badge, 90.0, 180.0),
]

# 1. Rounded square badge background (Colors.Blue4)
polygon(badge_pts, style=no_border_fill(Colors.Blue4))

# 2. Sleek bullet-train nose profile (WHITE body)
p_roof_l = (x0, 74.2)
p_nose_top = (88.8, 39.5)
p_nose_bot = (88.8, 34.0)
p_skirt_r = (74.0, 25.5)
p_skirt_l = (x0, 25.5)

roof_curve = _cubic(p_roof_l, (40.0, 74.4), (67.0, 58.8), p_nose_top, 22)
nose_bot_curve = _cubic(p_nose_bot, (85.5, 29.0), (79.8, 25.8), p_skirt_r, 10)

train_pts: list[tuple[float, float]] = [
    p_roof_l,
    *roof_curve,
    p_nose_bot,
    *nose_bot_curve,
    p_skirt_l,
]
polygon(train_pts, style=no_border_fill(WHITE))

# 3. Upper aerodynamic cockpit stripe (Colors.Blue4)
cockpit_l_top = (x0, 69.2)
cockpit_tip = (63.5, 55.2)
cockpit_l_bot = (x0, 61.8)
cockpit_pts: list[tuple[float, float]] = [
    cockpit_l_top,
    *_cubic(cockpit_l_top, (31.0, 69.0), (49.5, 61.2), cockpit_tip, 16),
    *_cubic(cockpit_tip, (46.5, 58.4), (27.5, 61.5), cockpit_l_bot, 16),
]
polygon(cockpit_pts, style=no_border_fill(Colors.Blue4))
draw_round_polyline(cockpit_pts, width_units=1.5, color=DARK, closed=True)

# 4. Left passenger window trapezoid (Colors.Blue4)
win_pts = [
    (x0, 52.0),
    (31.2, 52.0),
    (42.5, 37.2),
    (x0, 37.2),
]
polygon(win_pts, style=no_border_fill(Colors.Blue4))
draw_round_polyline(win_pts, width_units=1.6, color=DARK, closed=True)

# 5. Front nose-cone accent panel (Colors.Blue4)
nose_cone_pts = [
    (81.5, 44.5),
    *_cubic((81.5, 44.5), (85.2, 42.5), (87.4, 40.8), p_nose_top, 6),
    p_nose_bot,
    *_cubic(p_nose_bot, (86.8, 30.8), (84.0, 28.8), (81.5, 27.6), 6),
]
polygon(nose_cone_pts, style=no_border_fill(Colors.Blue4))
draw_round_polyline(nose_cone_pts, width_units=1.6, color=DARK, closed=True)

# 6. Front pill accent & speed lines (DARK)
pill_pts = [
    *_arc(59.5, 36.4, 1.5, 90.0, 270.0, 8),
    *_arc(73.8, 36.4, 1.5, 270.0, 450.0, 8),
]
polygon(pill_pts, style=no_border_fill(Colors.Blue4))
draw_round_polyline(pill_pts, width_units=1.4, color=DARK, closed=True)

sweep_line = [
    (x0, 58.0),
    *_cubic((x0, 58.0), (35.0, 57.8), (60.5, 51.8), (81.5, 44.5), 18),
]
draw_round_polyline(sweep_line, width_units=1.6, color=DARK)
draw_round_segment((x0, 33.4), (44.8, 33.4), width_units=1.7, color=DARK)

# Train roof & bottom skirt borders
draw_round_polyline([p_roof_l, *roof_curve], width_units=1.8, color=DARK)
draw_round_polyline([p_nose_bot, *nose_bot_curve, p_skirt_l], width_units=1.8, color=DARK)

# 7. Outer rounded-square border (w = 1.9, DARK) drawn last for crisp framing
draw_round_polyline(badge_pts, width_units=w, color=DARK, closed=True)

save()
