# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: fluentd."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 24,
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

w = ORIG_STROKE

# Key bird landmarks
p_back_wing = (53.0, 62.0)
p_wing_tip = (13.5, 81.5)
p_wing_mid = (24.5, 48.0)
p_center_seam = (54.0, 45.0)
p_tail_tip = (13.5, 17.5)
p_beak_tip = (88.0, 56.0)

# Shared internal seam curves
seam_wing_mid_to_center = _bezier(p_wing_mid, (34.0, 44.0), (45.0, 44.0), p_center_seam, 18)
seam_center_to_back = _bezier(p_center_seam, (55.0, 51.0), (54.0, 57.0), p_back_wing, 14)
seam_tail_to_center = _bezier(p_tail_tip, (30.0, 26.0), (43.0, 36.0), p_center_seam, 20)

# 1. Upper wing facet (PASTEL_BLUE_LIGHT)
upper_wing = [
    p_back_wing,
    *_bezier(p_back_wing, (39.0, 72.0), (24.0, 84.5), p_wing_tip, 22),
    *_bezier(p_wing_tip, (9.5, 75.0), (14.5, 58.0), p_wing_mid, 20),
    *seam_wing_mid_to_center,
    *seam_center_to_back,
]
polygon(upper_wing, style=no_border_fill(PASTEL_BLUE_LIGHT))

# 2. Lower wing / tail back facet (PASTEL_GREEN)
lower_wing = [
    p_wing_mid,
    *_bezier(p_wing_mid, (31.0, 36.0), (28.0, 22.0), p_tail_tip, 20),
    *seam_tail_to_center,
    *reversed([p_wing_mid, *seam_wing_mid_to_center[:-1]]),
]
polygon(lower_wing, style=no_border_fill(PASTEL_GREEN))

# 3. Main body, neck, head & beak facet (PASTEL_BLUE)
p_head_top = (74.0, 65.5)
p_beak_top = (82.5, 59.5)
p_chin = (79.5, 53.5)

body_pts = [
    p_tail_tip,
    *seam_tail_to_center,
    *seam_center_to_back,
    *_bezier(p_back_wing, (60.0, 59.0), (66.0, 66.5), p_head_top, 16),
    *_bezier(p_head_top, (78.5, 65.0), (80.5, 61.5), p_beak_top, 10),
    p_beak_tip,
    *_bezier(p_beak_tip, (85.0, 54.5), (82.0, 54.0), p_chin, 8),
    *_bezier(p_chin, (69.0, 49.0), (62.0, 34.0), (50.0, 23.0), 18),
    *_bezier((50.0, 23.0), (39.0, 14.5), (25.0, 15.0), p_tail_tip, 18),
]
polygon(body_pts, style=no_border_fill(PASTEL_BLUE))

# Internal facet seams
draw_round_polyline([p_wing_mid, *seam_wing_mid_to_center], width_units=2.2, color=DARK)
draw_round_polyline([p_tail_tip, *seam_tail_to_center, *seam_center_to_back], width_units=2.2, color=DARK)

# Outer silhouette border
outer_pts = [
    p_back_wing,
    *_bezier(p_back_wing, (39.0, 72.0), (24.0, 84.5), p_wing_tip, 22),
    *_bezier(p_wing_tip, (9.5, 75.0), (14.5, 58.0), p_wing_mid, 20),
    *_bezier(p_wing_mid, (31.0, 36.0), (28.0, 22.0), p_tail_tip, 20),
    *_bezier(p_tail_tip, (25.0, 15.0), (39.0, 14.5), (50.0, 23.0), 18),
    *_bezier((50.0, 23.0), (62.0, 34.0), (69.0, 49.0), p_chin, 18),
    *_bezier(p_chin, (82.0, 54.0), (85.0, 54.5), p_beak_tip, 8),
    p_beak_top,
    *_bezier(p_beak_top, (80.5, 61.5), (78.5, 65.0), p_head_top, 10),
    *_bezier(p_head_top, (66.0, 66.5), (60.0, 59.0), p_back_wing, 16),
]
draw_round_polyline(outer_pts, width_units=w, color=DARK, closed=True)

# Bird eye
circle(
    (73.5, 59.0),
    radius=3.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
