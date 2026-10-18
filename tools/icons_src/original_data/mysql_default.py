# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data icon: MySQL."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

# Soft aqua-teal between Colors.Teal2 (#9EDEDE) and Colors.Teal3 (#55C3C3), paired with Colors.Teal4 (#2A989A)
BELLY_AQUA = "#70CCC7"


def _bezier(
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
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


setup_icon()

w = 2.0

# Key landmarks of the upward-left leaping dolphin
p_snout = (9.5, 86.2)
p_melon_base = (20.2, 84.5)
p_head_top = (30.5, 87.2)
p_back_mid = (54.0, 75.5)
p_tail_wrist_top = (76.8, 31.8)
p_fluke_r = (90.8, 22.0)
p_fluke_notch = (76.8, 21.8)
p_fluke_bot = (66.2, 11.8)
p_tail_wrist_bot = (69.8, 28.0)
p_flip_rear_body = (40.8, 54.5)
p_flip_rear_top = (43.2, 59.8)
p_flip_tip = (37.8, 44.8)
p_flip_front_body = (31.8, 61.2)
p_flip_front_top = (33.6, 67.2)

# 1. Full dolphin silhouette fill in ocean teal (Colors.Teal4)
body_pts = [
    p_snout,
    *_bezier(p_snout, (12.0, 88.2), (16.5, 86.2), p_melon_base, 10),
    *_bezier(p_melon_base, (23.2, 86.8), (26.5, 87.5), p_head_top, 10),
    *_bezier(p_head_top, (38.5, 86.8), (47.0, 82.2), p_back_mid, 14),
    *_bezier(p_back_mid, (63.5, 66.5), (72.8, 48.0), p_tail_wrist_top, 18),
    *_bezier(p_tail_wrist_top, (83.2, 31.2), (88.5, 27.5), p_fluke_r, 12),
    *_bezier(p_fluke_r, (91.5, 20.2), (82.5, 22.8), p_fluke_notch, 12),
    *_bezier(p_fluke_notch, (75.2, 16.5), (70.0, 12.0), p_fluke_bot, 12),
    *_bezier(p_fluke_bot, (64.2, 12.2), (65.2, 21.5), p_tail_wrist_bot, 12),
    *_bezier(p_tail_wrist_bot, (64.0, 38.5), (52.0, 47.5), p_flip_rear_body, 14),
    *_bezier(p_flip_rear_body, (39.6, 50.0), (39.4, 45.2), p_flip_tip, 10),
    *_bezier(p_flip_tip, (35.8, 44.5), (31.0, 53.0), p_flip_front_body, 12),
    *_bezier(p_flip_front_body, (24.5, 68.5), (18.5, 75.5), (14.5, 79.2), 12),
    *_bezier((14.5, 79.2), (10.8, 82.5), (8.2, 84.8), p_snout, 10),
]
polygon(body_pts, style=no_border_fill(Colors.Teal4))

# 2. Light aqua belly bands (BELLY_AQUA) — interrupted cleanly by the ocean-teal pectoral flipper
# Front throat/jaw band (from snout tip to front edge of flipper)
throat_band_pts = [
    (10.0, 85.4),
    *_bezier((10.0, 85.4), (17.5, 81.2), (26.2, 74.8), (33.2, 66.8), 14),
    *_bezier((33.2, 66.8), (32.4, 64.2), (32.0, 62.5), p_flip_front_body, 6),
    *_bezier(p_flip_front_body, (24.5, 68.5), (18.5, 75.5), (14.5, 79.2), 12),
    *_bezier((14.5, 79.2), (11.2, 82.2), (9.2, 84.4), (10.0, 85.4), 8),
]
polygon(throat_band_pts, style=no_border_fill(BELLY_AQUA))

# Rear belly band (from rear edge of flipper to tail wrist)
belly_band_pts = [
    (43.0, 59.5),
    *_bezier((43.0, 59.5), (54.2, 52.0), (64.5, 42.5), (70.6, 28.8), 16),
    p_tail_wrist_bot,
    *_bezier(p_tail_wrist_bot, (64.0, 38.5), (52.0, 47.5), p_flip_rear_body, 14),
    *_bezier(p_flip_rear_body, (41.6, 56.5), (42.3, 58.0), (43.0, 59.5), 6),
]
polygon(belly_band_pts, style=no_border_fill(BELLY_AQUA))

# 3. Bold dark slate-navy outlines (DARK, width=ORIG_STROKE)
top_to_tail_to_flipper_rear = [
    p_flip_front_body,
    *_bezier(p_flip_front_body, (24.5, 68.5), (18.5, 75.5), (14.5, 79.2), 12),
    *_bezier((14.5, 79.2), (10.8, 82.5), (8.2, 84.8), p_snout, 10),
    *_bezier(p_snout, (12.0, 88.2), (16.5, 86.2), p_melon_base, 10),
    *_bezier(p_melon_base, (23.2, 86.8), (26.5, 87.5), p_head_top, 10),
    *_bezier(p_head_top, (38.5, 86.8), (47.0, 82.2), p_back_mid, 14),
    *_bezier(p_back_mid, (63.5, 66.5), (72.8, 48.0), p_tail_wrist_top, 18),
    *_bezier(p_tail_wrist_top, (83.2, 31.2), (88.5, 27.5), p_fluke_r, 12),
    *_bezier(p_fluke_r, (91.5, 20.2), (82.5, 22.8), p_fluke_notch, 12),
    *_bezier(p_fluke_notch, (75.2, 16.5), (70.0, 12.0), p_fluke_bot, 12),
    *_bezier(p_fluke_bot, (64.2, 12.2), (65.2, 21.5), p_tail_wrist_bot, 12),
    *_bezier(p_tail_wrist_bot, (64.0, 38.5), (52.0, 47.5), p_flip_rear_body, 14),
]
draw_round_polyline(top_to_tail_to_flipper_rear, width_units=w, color=DARK)

# Pectoral flipper stroke (extends cleanly inside the body at both ends with round caps)
flipper_line = [
    p_flip_front_top,
    *_bezier(p_flip_front_top, (32.6, 64.2), (32.1, 62.6), p_flip_front_body, 6),
    *_bezier(p_flip_front_body, (31.0, 53.0), (35.8, 44.5), p_flip_tip, 12),
    *_bezier(p_flip_tip, (39.4, 45.2), (39.6, 50.0), p_flip_rear_body, 10),
    *_bezier(p_flip_rear_body, (41.6, 56.5), (42.4, 58.2), p_flip_rear_top, 6),
]
draw_round_polyline(flipper_line, width_units=w, color=DARK)

# 4. Simple solid dark dot eye
circle((29.5, 78.8), radius=2.0, style=fill_style(DARK))

save()
