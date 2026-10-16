# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: docker."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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

# 5 container squares stacked on whale back (3 bottom + 2 top)
containers = [
    (25.0, 55.5, PASTEL_BLUE_LIGHT),
    (40.0, 55.5, WHITE),
    (55.0, 55.5, PASTEL_GREEN),
    (40.0, 70.5, PASTEL_GREEN),
    (55.0, 70.5, WHITE),
]
for cx, cy, col in containers:
    rectangle(
        (cx, cy),
        width=13.0,
        height=13.0,
        style=fill_style(col, border_color=DARK, border_units=2.2, shape_r=2.0),
    )

# Whale body silhouette
p_nose = (12.0, 46.0)
p_deck_end = (64.0, 46.0)
p_tail_neck_l = (73.0, 52.0)
p_fluke_l_tip = (74.0, 66.0)
p_fluke_notch = (80.5, 56.5)
p_fluke_r_tip = (90.0, 55.5)
p_tail_base = (78.5, 43.5)
p_belly_bot = (39.0, 17.5)

whale_pts: list[tuple[float, float]] = [
    p_nose,
    p_deck_end,
    *_bezier(p_deck_end, (69.0, 46.0), (71.5, 48.5), p_tail_neck_l, 12),
    *_bezier(p_tail_neck_l, (70.0, 58.0), (71.0, 63.5), p_fluke_l_tip, 14),
    *_bezier(p_fluke_l_tip, (77.5, 64.0), (79.5, 60.5), p_fluke_notch, 12),
    *_bezier(p_fluke_notch, (83.5, 58.5), (87.5, 58.0), p_fluke_r_tip, 12),
    *_bezier(p_fluke_r_tip, (88.0, 48.5), (84.0, 44.5), p_tail_base, 14),
    *_bezier(p_tail_base, (71.0, 24.5), (56.0, 17.5), p_belly_bot, 24),
    *_bezier(p_belly_bot, (21.0, 17.5), (10.5, 31.0), p_nose, 24),
]

polygon(whale_pts, style=no_border_fill(PASTEL_BLUE))

# White lower belly curve patch on front-bottom of whale
p_belly_l = (14.8, 32.0)
p_belly_r = (58.0, 21.0)
belly_patch = [
    p_belly_l,
    *_bezier(p_belly_l, (28.0, 30.0), (45.0, 28.0), p_belly_r, 18),
    *_bezier(p_belly_r, (50.0, 18.2), (44.0, 17.5), p_belly_bot, 12),
    *_bezier(p_belly_bot, (25.5, 17.5), (17.5, 23.5), p_belly_l, 16),
]
polygon(belly_patch, style=no_border_fill(WHITE))
draw_round_polyline(
    [p_belly_l, *_bezier(p_belly_l, (28.0, 30.0), (45.0, 28.0), p_belly_r, 18)],
    width_units=2.1,
    color=DARK,
)

# Whale outer border
draw_round_polyline(whale_pts, width_units=w, color=DARK, closed=True)

# Whale eye
circle((25.0, 36.5), radius=2.4, style=fill_style(DARK))

save()
