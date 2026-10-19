# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data icon: MariaDB."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

# Warm caramel-brown palette harmonized with Drawlib's Amber/Orange tones
BODY_CARAMEL = "#CA8B42"
BELLY_TAN = "#EAB24A"
FAR_FLIPPER_BRONZE = "#B47834"


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


Icon.setup()

w = 2.0

# 1. Far front flipper behind chest (drawn first so chest cleanly overlaps its top attachment)
p_far_back = (68.5, 33.2)
p_far_tip = (80.8, 29.8)
p_far_top = (74.0, 42.0)
far_flipper_pts = [
    p_far_back,
    *_bezier(p_far_back, (71.8, 27.8), (77.0, 27.8), p_far_tip, 14),
    *_bezier(p_far_tip, (77.0, 33.2), (75.5, 37.8), p_far_top, 14),
]
polygon(far_flipper_pts, style=Icon.no_border_fill(FAR_FLIPPER_BRONZE))
Icon.draw_round_polyline(far_flipper_pts, width_units=w, color=Icon.DARK)

# 2. Main sea lion silhouette landmarks
p_nose_tip = (92.5, 78.2)
p_snout_bridge = (86.5, 77.5)
p_head_crown = (78.0, 76.2)
p_neck_back = (63.5, 56.5)
p_back_mid = (42.5, 48.0)
p_tail_wrist_top = (19.5, 31.6)
p_tail_u_tip = (7.2, 29.2)
p_tail_notch = (14.5, 28.5)
p_tail_l_tip = (8.2, 24.2)
p_tail_bot_base = (25.8, 28.5)
p_belly_arch = (39.5, 31.8)
p_flip_front_body = (55.5, 29.8)
p_flip_front_top = (58.6, 38.2)
p_flip_tip = (50.8, 21.0)
p_flip_rear_body = (68.0, 33.2)
p_flip_rear_top = (69.5, 39.6)
p_chest_mid = (77.5, 46.8)
p_throat = (82.8, 63.2)
p_chin = (90.5, 71.2)

seal_body_pts = [
    p_nose_tip,
    *_bezier(p_nose_tip, (90.8, 79.2), (88.5, 77.8), p_snout_bridge, 8),
    *_bezier(p_snout_bridge, (83.5, 77.2), (80.8, 77.2), p_head_crown, 10),
    *_bezier(p_head_crown, (71.5, 74.2), (68.2, 63.5), p_neck_back, 16),
    *_bezier(p_neck_back, (57.5, 49.5), (50.5, 49.8), p_back_mid, 14),
    *_bezier(p_back_mid, (31.5, 45.8), (25.5, 34.5), p_tail_wrist_top, 16),
    *_bezier(p_tail_wrist_top, (15.8, 30.2), (10.5, 31.0), p_tail_u_tip, 12),
    *_bezier(p_tail_u_tip, (7.0, 27.8), (11.5, 28.0), p_tail_notch, 8),
    *_bezier(p_tail_notch, (11.5, 26.5), (7.8, 25.8), p_tail_l_tip, 8),
    *_bezier(p_tail_l_tip, (9.0, 22.8), (18.5, 23.2), p_tail_bot_base, 12),
    *_bezier(p_tail_bot_base, (30.5, 31.2), (34.5, 32.0), p_belly_arch, 10),
    *_bezier(p_belly_arch, (45.2, 31.6), (50.8, 30.6), p_flip_front_body, 12),
    *_bezier(p_flip_front_body, (54.0, 25.8), (52.0, 22.8), p_flip_tip, 10),
    *_bezier(p_flip_tip, (56.5, 21.8), (63.5, 25.8), p_flip_rear_body, 14),
    *_bezier(p_flip_rear_body, (72.8, 37.5), (75.5, 41.5), p_chest_mid, 12),
    *_bezier(p_chest_mid, (80.0, 52.8), (80.8, 58.8), p_throat, 14),
    *_bezier(p_throat, (84.8, 67.2), (88.5, 68.8), p_chin, 12),
    *_bezier(p_chin, (92.8, 73.5), (93.8, 76.8), p_nose_tip, 8),
]
polygon(seal_body_pts, style=Icon.no_border_fill(BODY_CARAMEL))

# 3. Light golden-tan chest & underbelly highlights (BELLY_TAN)
# 3a. Lower belly highlight (between tail base and front flipper)
belly_highlight_pts = [
    (26.8, 29.0),
    *_bezier((26.8, 29.0), (34.5, 35.2), (46.5, 35.0), (57.2, 36.2), 16),
    p_flip_front_body,
    *_bezier(p_flip_front_body, (50.8, 30.6), (45.2, 31.6), p_belly_arch, 12),
    *_bezier(p_belly_arch, (34.5, 32.0), (30.8, 31.2), (26.8, 29.0), 10),
]
polygon(belly_highlight_pts, style=Icon.no_border_fill(BELLY_TAN))

# 3b. Front chest & throat highlight (generous band from upper throat down to armpit)
chest_highlight_pts = [
    (82.4, 62.5),
    *_bezier((82.4, 62.5), (74.8, 53.0), (70.5, 43.0), (69.0, 38.6), 16),
    p_flip_rear_body,
    *_bezier(p_flip_rear_body, (72.8, 37.5), (75.5, 41.5), p_chest_mid, 12),
    *_bezier(p_chest_mid, (80.0, 52.8), (80.8, 58.8), (82.4, 62.5), 12),
]
polygon(chest_highlight_pts, style=Icon.no_border_fill(BELLY_TAN))

# 4. Nose tip dark cap (drawn before outer stroke so outer stroke wraps it cleanly)
nose_cap_pts = [
    (89.2, 77.8),
    *_bezier((89.2, 77.8), (90.8, 79.0), (92.0, 78.8), p_nose_tip, 6),
    *_bezier(p_nose_tip, (93.5, 77.2), (93.2, 75.5), (91.8, 74.2), 6),
    *_bezier((91.8, 74.2), (90.0, 74.5), (89.0, 76.0), (89.2, 77.8), 6),
]
polygon(nose_cap_pts, style=Icon.no_border_fill(Icon.DARK))

# 5. Bold dark slate-navy outlines (DARK, width=1.9)
outer_outline = [
    p_flip_rear_body,
    *_bezier(p_flip_rear_body, (72.8, 37.5), (75.5, 41.5), p_chest_mid, 12),
    *_bezier(p_chest_mid, (80.0, 52.8), (80.8, 58.8), p_throat, 14),
    *_bezier(p_throat, (84.8, 67.2), (88.5, 68.8), p_chin, 12),
    *_bezier(p_chin, (92.8, 73.5), (93.8, 76.8), p_nose_tip, 8),
    *_bezier(p_nose_tip, (90.8, 79.2), (88.5, 77.8), p_snout_bridge, 8),
    *_bezier(p_snout_bridge, (83.5, 77.2), (80.8, 77.2), p_head_crown, 10),
    *_bezier(p_head_crown, (71.5, 74.2), (68.2, 63.5), p_neck_back, 16),
    *_bezier(p_neck_back, (57.5, 49.5), (50.5, 49.8), p_back_mid, 14),
    *_bezier(p_back_mid, (31.5, 45.8), (25.5, 34.5), p_tail_wrist_top, 16),
    *_bezier(p_tail_wrist_top, (15.8, 30.2), (10.5, 31.0), p_tail_u_tip, 12),
    *_bezier(p_tail_u_tip, (7.0, 27.8), (11.5, 28.0), p_tail_notch, 8),
    *_bezier(p_tail_notch, (11.5, 26.5), (7.8, 25.8), p_tail_l_tip, 8),
    *_bezier(p_tail_l_tip, (9.0, 22.8), (18.5, 23.2), p_tail_bot_base, 12),
    *_bezier(p_tail_bot_base, (30.5, 31.2), (34.5, 32.0), p_belly_arch, 10),
    *_bezier(p_belly_arch, (45.2, 31.6), (50.8, 30.6), p_flip_front_body, 12),
]
Icon.draw_round_polyline(outer_outline, width_units=w, color=Icon.DARK)

# Foreground front flipper stroke (both ends extend cleanly inside the body with round caps)
front_flipper_line = [
    p_flip_front_top,
    *_bezier(p_flip_front_top, (57.5, 34.8), (56.5, 32.0), p_flip_front_body, 8),
    *_bezier(p_flip_front_body, (54.0, 25.8), (52.0, 22.8), p_flip_tip, 10),
    *_bezier(p_flip_tip, (56.5, 21.8), (63.5, 25.8), p_flip_rear_body, 14),
    *_bezier(p_flip_rear_body, (68.6, 35.5), (69.1, 37.5), p_flip_rear_top, 6),
]
Icon.draw_round_polyline(front_flipper_line, width_units=w, color=Icon.DARK)

# 6. Eye, ear flap, and 2 clean curved whiskers
circle((81.5, 72.2), radius=1.8, style=Icon.fill_style(Icon.DARK))

ear_pts = [
    (76.2, 69.2),
    *_bezier((76.2, 69.2), (74.2, 69.0), (73.5, 67.0), (74.6, 66.2), 8),
    *_bezier((74.6, 66.2), (75.5, 65.6), (76.6, 66.5), (77.0, 67.3), 6),
]
Icon.draw_round_polyline(ear_pts, width_units=1.35, color=Icon.DARK)

whisker_1 = [
    (88.0, 74.8),
    *_bezier((88.0, 74.8), (86.4, 73.4), (85.2, 71.5), (84.6, 69.5), 8),
]
whisker_2 = [
    (89.2, 73.6),
    *_bezier((89.2, 73.6), (88.0, 72.4), (87.2, 70.8), (86.8, 69.2), 8),
]
Icon.draw_round_polyline(whisker_1, width_units=1.15, color=Icon.DARK)
Icon.draw_round_polyline(whisker_2, width_units=1.15, color=Icon.DARK)

save()
