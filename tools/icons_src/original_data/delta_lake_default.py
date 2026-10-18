# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: delta_lake."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 20,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


setup_icon()

w = 2.0

# Upper Delta A-frame ribbon (Colors.Teal3) with hollow center and left wave hook
p_top_l = (47.8, 86.2)
p_top_r = (53.2, 86.2)
p_left_leg_bot = (17.0, 35.5)
p_hook_tip = (53.0, 35.5)
p_inner_bl = (38.0, 44.5)
p_inner_top = (50.5, 65.5)
p_inner_br = (72.5, 27.5)

# Collinear point on right outer leg from p_top_r (53.2, 86.2) toward (87.8, 26.8)
p_seam_outer_r = (86.2, 29.5)
seam_curve = _bezier(p_inner_br, (77.5, 27.5), (82.0, 28.2), p_seam_outer_r, 12)

upper_delta_pts = [
    p_top_l,
    p_left_leg_bot,
    *_bezier(p_left_leg_bot, (16.0, 33.8), (17.8, 33.0), (21.5, 34.4), 10),
    *_bezier((21.5, 34.4), (31.5, 38.2), (43.0, 38.8), p_hook_tip, 18),
    *_bezier(p_hook_tip, (54.5, 35.2), (54.8, 36.8), (52.8, 38.2), 8),
    *_bezier((52.8, 38.2), (48.0, 41.5), (43.0, 43.2), p_inner_bl, 14),
    p_inner_top,
    p_inner_br,
    *seam_curve,
    p_top_r,
    *_bezier(p_top_r, (51.8, 88.6), (49.2, 88.6), p_top_l, 12),
]

polygon(upper_delta_pts, style=no_border_fill(Colors.Teal3))

# Lower sweeping lake wave ribbon (Colors.Blue4) with uniform clear channel gap
p_wave_tip_l = (11.5, 18.0)

lower_wave_pts = [
    p_inner_br,
    *_bezier(p_inner_br, (65.0, 24.0), (56.0, 26.5), (46.5, 29.8), 16),
    *_bezier((46.5, 29.8), (33.5, 34.2), (21.0, 29.8), p_wave_tip_l, 20),
    *_bezier(p_wave_tip_l, (10.2, 16.5), (11.2, 15.5), (13.8, 16.6), 8),
    *_bezier((13.8, 16.6), (25.5, 21.8), (36.5, 23.5), (48.0, 18.5), 18),
    *_bezier((48.0, 18.5), (62.0, 12.2), (76.5, 11.8), (85.8, 18.8), 20),
    *_bezier((85.8, 18.8), (89.0, 21.5), (88.8, 25.0), p_seam_outer_r, 12),
    *reversed([p_inner_br, *seam_curve[:-1]]),
]

polygon(lower_wave_pts, style=no_border_fill(Colors.Blue4))

# Internal seam and crisp outer borders
draw_round_polyline([p_inner_br, *seam_curve], width_units=1.8, color=DARK)
draw_round_polyline(upper_delta_pts, width_units=w, color=DARK, closed=True)
draw_round_polyline(lower_wave_pts, width_units=w, color=DARK, closed=True)

save()
