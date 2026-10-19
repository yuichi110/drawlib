# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data icon: Flink (Pattern 2 modern implementation)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

# Brand-harmonized Flink palette
BODY_BERRY = "#D4456E"
TAIL_PURPLE = "#8B61D8"
TAIL_CORAL = "#F26153"
TAIL_AMBER = "#F6B836"
ACORN_GOLD = "#F6B836"


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

# ---------------------------------------------------------------------------
# 1. Bushy S-curved tail (3 smooth color zones + berry root)
# ---------------------------------------------------------------------------
p_tail_curl_tip = (32.0, 82.8)
p_tail_curl_neck = (40.2, 71.2)
p_tail_left_mid = (7.2, 36.5)
p_tail_root_bot = (36.0, 6.5)
p_tail_crest_top = (51.5, 93.2)
p_tail_right_top = (71.8, 81.2)
p_tail_right_ear = (74.2, 53.5)
p_coral_bot_l = (23.2, 46.2)
p_coral_bot_r = (50.5, 53.0)
p_purple_taper = (7.4, 33.0)
p_purple_rib_start = (16.2, 27.5)
p_back_join = (46.5, 42.2)

# Outer tail contour curves
c_curl_tip_to_neck = _bezier(p_tail_curl_tip, (37.2, 81.2), (40.5, 76.5), p_tail_curl_neck, 12)
c_neck_to_left_mid = _bezier(p_tail_curl_neck, (34.0, 63.5), (9.5, 62.5), p_tail_left_mid, 18)
c_left_mid_to_taper = _bezier(p_tail_left_mid, (7.0, 35.0), (7.1, 34.0), p_purple_taper, 4)
c_taper_to_root = _bezier(p_purple_taper, (6.8, 19.5), (19.0, 6.8), p_tail_root_bot, 16)
c_curl_tip_to_crest = _bezier(p_tail_curl_tip, (37.5, 90.0), (44.0, 93.2), p_tail_crest_top, 12)
c_crest_to_right_top = _bezier(p_tail_crest_top, (61.5, 93.2), (68.5, 87.8), p_tail_right_top, 14)
c_right_top_to_ear = _bezier(p_tail_right_top, (77.5, 72.5), (77.2, 60.5), p_tail_right_ear, 14)

# Seam between Amber crest and Coral center
c_amber_coral_seam = _bezier(p_tail_curl_tip, (45.0, 86.2), (64.5, 81.5), (64.2, 68.5), 16) + _bezier(
    (64.2, 68.5), (64.0, 60.0), (57.5, 55.2), p_coral_bot_r, 12
)

# Seam between Coral center and left Purple wave
c_neck_to_coral_bot_l = _bezier(p_tail_curl_neck, (41.2, 61.5), (23.8, 58.2), p_coral_bot_l, 16)

# Continuous S-seam from Coral bottom-left across to right tail top (separating Coral/Amber from Purple ribbon)
c_coral_bot_l_to_r = _bezier(p_coral_bot_l, (30.5, 50.2), (41.5, 51.0), p_coral_bot_r, 14)
c_coral_bot_r_to_right_top = _bezier(p_coral_bot_r, (64.5, 55.2), (72.5, 67.5), p_tail_right_top, 16)

# Seam from Coral bottom-left down into the tail root
c_coral_bot_l_to_taper = _bezier(p_coral_bot_l, (16.5, 40.5), (15.0, 32.5), p_purple_rib_start, 10)
p_crease_touch = (19.5, 19.2)
c_rib_start_to_touch = _bezier(p_purple_rib_start, (16.6, 24.2), (17.6, 21.5), p_crease_touch, 8)
c_touch_to_root_in = _bezier(p_crease_touch, (22.5, 15.2), (27.0, 12.8), (31.8, 11.2), 10)

# Seam between Purple middle ribbon and Berry rump
c_purple_bot_seam = _bezier(p_purple_rib_start, (18.8, 37.5), (30.0, 41.2), p_back_join, 16)

# Smooth tangent taper from outer left tail edge into the inner tail crease
c_outer_purple_taper = _bezier(p_purple_taper, (9.2, 26.5), (14.2, 21.8), p_crease_touch, 12)

# 1a. Full tail base fill in TAIL_PURPLE
tail_full_pts = [
    p_tail_curl_tip,
    *c_curl_tip_to_neck,
    *c_neck_to_left_mid,
    *c_left_mid_to_taper,
    *c_taper_to_root,
    (55.0, 12.0),
    p_tail_right_ear,
    *reversed([p_tail_right_top, *c_right_top_to_ear[:-1]]),
    *reversed([p_tail_crest_top, *c_crest_to_right_top[:-1]]),
    *reversed([p_tail_curl_tip, *c_curl_tip_to_crest[:-1]]),
]
polygon(tail_full_pts, style=Icon.no_border_fill(TAIL_PURPLE))

# 1b. Berry tail root & rump fill
tail_root_pts = [
    p_purple_taper,
    *c_taper_to_root,
    (48.0, 12.0),
    p_back_join,
    *reversed([p_purple_rib_start, *c_purple_bot_seam[:-1]]),
    *c_rib_start_to_touch,
    *reversed([p_purple_taper, *c_outer_purple_taper[:-1]]),
]
polygon(tail_root_pts, style=Icon.no_border_fill(BODY_BERRY))

# 1c. Amber top crest fill (TAIL_AMBER)
tail_amber_pts = [
    p_tail_curl_tip,
    *c_curl_tip_to_crest,
    *c_crest_to_right_top,
    *reversed([p_coral_bot_r, *c_coral_bot_r_to_right_top[:-1]]),
    *reversed([p_tail_curl_tip, *c_amber_coral_seam[:-1]]),
]
polygon(tail_amber_pts, style=Icon.no_border_fill(TAIL_AMBER))

# 1d. Coral center curl fill (TAIL_CORAL)
tail_coral_pts = [
    p_tail_curl_tip,
    *c_amber_coral_seam,
    *reversed([p_coral_bot_l, *c_coral_bot_l_to_r[:-1]]),
    *reversed([p_tail_curl_neck, *c_neck_to_coral_bot_l[:-1]]),
    *reversed([p_tail_curl_tip, *c_curl_tip_to_neck[:-1]]),
]
polygon(tail_coral_pts, style=Icon.no_border_fill(TAIL_CORAL))

# 1e. Tail dark strokes
tail_outer_stroke = [
    p_tail_right_ear,
    *reversed([p_tail_right_top, *c_right_top_to_ear[:-1]]),
    *reversed([p_tail_crest_top, *c_crest_to_right_top[:-1]]),
    *reversed([p_tail_curl_tip, *c_curl_tip_to_crest[:-1]]),
    *c_curl_tip_to_neck,
    *c_neck_to_left_mid,
    *c_left_mid_to_taper,
    *c_taper_to_root,
]
Icon.draw_round_polyline(tail_outer_stroke, width_units=w, color=Icon.DARK)

# Interior tail wave seams
Icon.draw_round_polyline([p_tail_curl_tip, *c_amber_coral_seam], width_units=w, color=Icon.DARK)
Icon.draw_round_polyline([p_tail_curl_neck, *c_neck_to_coral_bot_l], width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(
    [p_coral_bot_l, *c_coral_bot_l_to_r, *c_coral_bot_r_to_right_top], width_units=w, color=Icon.DARK
)

# Inner curved line inside the coral curl
coral_inner_curve = [
    (47.2, 72.8),
    *_bezier((47.2, 72.8), (57.2, 68.5), (56.5, 58.2), p_coral_bot_r, 14),
]
Icon.draw_round_polyline(coral_inner_curve, width_units=w, color=Icon.DARK)

# Left lower purple ribbon seams
Icon.draw_round_polyline(
    [p_coral_bot_l, *c_coral_bot_l_to_taper, *c_rib_start_to_touch, *c_touch_to_root_in],
    width_units=w,
    color=Icon.DARK,
)
Icon.draw_round_polyline([p_purple_rib_start, *c_purple_bot_seam], width_units=w, color=Icon.DARK)

# ---------------------------------------------------------------------------
# 2. Acorn (Golden nut + Berry-pink saucer cap at bottom-right)
# ---------------------------------------------------------------------------
p_nut_l = (79.2, 17.5)
p_nut_r = (92.8, 16.5)
nut_pts = [
    p_nut_l,
    *_bezier(p_nut_l, (78.8, 24.5), (83.5, 28.2), (87.5, 27.8), 12),
    *_bezier((87.5, 27.8), (92.2, 27.2), (93.8, 21.8), p_nut_r, 12),
    *_bezier(p_nut_r, (88.5, 13.5), (83.2, 13.8), p_nut_l, 10),
]
polygon(nut_pts, style=Icon.no_border_fill(ACORN_GOLD))
Icon.draw_round_polyline(nut_pts, width_units=w, color=Icon.DARK, closed=True)

p_cap_l = (78.5, 18.2)
p_cap_r = (93.2, 16.5)
p_stem_l = (82.2, 9.2)
p_stem_tip_1 = (82.8, 7.2)
p_stem_notch = (84.8, 7.8)
p_stem_tip_2 = (86.6, 6.2)
p_stem_r = (87.6, 9.2)

cap_pts = [
    p_cap_l,
    *_bezier(p_cap_l, (82.8, 14.2), (88.8, 13.8), p_cap_r, 12),
    *_bezier(p_cap_r, (94.0, 13.5), (91.8, 9.8), p_stem_r, 10),
    *_bezier(p_stem_r, (87.8, 7.2), (87.4, 6.2), p_stem_tip_2, 6),
    *_bezier(p_stem_tip_2, (85.6, 6.2), (85.2, 7.5), p_stem_notch, 6),
    *_bezier(p_stem_notch, (84.0, 7.0), (83.2, 6.8), p_stem_tip_1, 6),
    *_bezier(p_stem_tip_1, (81.8, 7.5), (81.8, 8.8), p_stem_l, 6),
    *_bezier(p_stem_l, (78.2, 10.5), (76.8, 15.2), p_cap_l, 10),
]
polygon(cap_pts, style=Icon.no_border_fill(BODY_BERRY))
Icon.draw_round_polyline(cap_pts, width_units=w, color=Icon.DARK, closed=True)

# ---------------------------------------------------------------------------
# 3. Squirrel Body, Head, Ear, Front Arm/Paw & Hind Foot (BODY_BERRY)
# ---------------------------------------------------------------------------
p_rump_bot = (36.0, 6.5)
p_hind_toe_bot = (75.5, 6.5)
p_hind_toe_top = (73.5, 11.8)
p_hind_ankle = (69.0, 10.8)
p_belly_low = (74.2, 19.8)
p_paw_bot_l = (83.2, 23.2)
p_paw_tip_bot = (89.5, 25.5)
p_paw_tip_top = (88.2, 31.2)
p_chin_join = (81.2, 31.4)
p_snout_bot = (91.8, 35.8)
p_nose_tip = (93.5, 40.2)
p_forehead = (88.5, 51.5)
p_ear_r_base = (81.8, 54.8)
p_ear_tip = (79.0, 60.2)
p_ear_l_base = (74.8, 53.2)
p_neck_back = (62.5, 45.2)
p_haunch_top = (44.0, 41.2)

squirrel_pts = [
    p_rump_bot,
    p_hind_toe_bot,
    *_bezier(p_hind_toe_bot, (78.2, 6.5), (78.5, 11.8), p_hind_toe_top, 10),
    p_hind_ankle,
    *_bezier(p_hind_ankle, (72.2, 13.5), (74.0, 16.5), p_belly_low, 10),
    *_bezier(p_belly_low, (77.5, 19.5), (81.5, 20.8), p_paw_bot_l, 10),
    *_bezier(p_paw_bot_l, (85.2, 26.2), (87.5, 26.2), p_paw_tip_bot, 8),
    *_bezier(p_paw_tip_bot, (92.0, 26.2), (91.8, 31.2), p_paw_tip_top, 10),
    *_bezier(p_paw_tip_top, (85.5, 31.6), (83.2, 30.8), p_chin_join, 8),
    *_bezier(p_chin_join, (85.5, 32.2), (89.8, 33.8), p_snout_bot, 10),
    *_bezier(p_snout_bot, (93.2, 37.2), (93.8, 38.8), p_nose_tip, 8),
    *_bezier(p_nose_tip, (92.5, 45.5), (91.2, 49.2), p_forehead, 12),
    *_bezier(p_forehead, (86.2, 53.8), (83.8, 54.5), p_ear_r_base, 8),
    *_bezier(p_ear_r_base, (81.2, 58.2), (80.0, 60.2), p_ear_tip, 8),
    *_bezier(p_ear_tip, (77.2, 59.5), (75.5, 56.5), p_ear_l_base, 8),
    *_bezier(p_ear_l_base, (70.5, 49.5), (67.5, 46.5), p_neck_back, 12),
    *_bezier(p_neck_back, (55.5, 43.5), (49.5, 42.8), p_haunch_top, 12),
    *_bezier(p_haunch_top, (34.5, 38.2), (31.5, 20.0), p_rump_bot, 18),
]
polygon(squirrel_pts, style=Icon.no_border_fill(BODY_BERRY))

# Back + haunch crease extending down inside hip
back_and_haunch_line = [
    p_ear_l_base,
    *_bezier(p_ear_l_base, (70.5, 49.5), (67.5, 46.5), p_neck_back, 12),
    *_bezier(p_neck_back, (55.5, 43.5), (49.5, 42.8), p_haunch_top, 12),
    *_bezier(p_haunch_top, (35.2, 36.8), (33.8, 25.5), (35.5, 17.8), 16),
]
Icon.draw_round_polyline(back_and_haunch_line, width_units=w, color=Icon.DARK)

# Ear stroke (both bases extend slightly down into the head)
ear_line = [
    (75.5, 51.0),
    p_ear_l_base,
    *_bezier(p_ear_l_base, (75.5, 56.5), (77.2, 59.5), p_ear_tip, 8),
    *_bezier(p_ear_tip, (80.0, 60.2), (81.2, 58.2), p_ear_r_base, 8),
    (81.0, 51.2),
]
Icon.draw_round_polyline(ear_line, width_units=w, color=Icon.DARK)

# Forehead, snout, and cheek crease (extending back into cheek)
head_and_cheek_line = [
    p_ear_r_base,
    *_bezier(p_ear_r_base, (83.8, 54.5), (86.2, 53.8), p_forehead, 8),
    *_bezier(p_forehead, (91.2, 49.2), (92.5, 45.5), p_nose_tip, 12),
    *_bezier(p_nose_tip, (93.8, 38.8), (93.2, 37.2), p_snout_bot, 8),
    *_bezier(p_snout_bot, (89.8, 33.8), (85.5, 32.2), p_chin_join, 10),
    *_bezier(p_chin_join, (77.5, 31.0), (74.5, 32.2), (72.2, 34.0), 10),
]
Icon.draw_round_polyline(head_and_cheek_line, width_units=w, color=Icon.DARK)

# Front arm shoulder crease + forearm + paw holding acorn
arm_and_paw_line = [
    (53.5, 35.2),
    *_bezier((53.5, 35.2), (62.8, 35.0), (64.8, 28.5), (66.8, 22.8), 14),
    *_bezier((66.8, 22.8), (68.8, 19.5), (73.5, 19.2), p_belly_low, 10),
    *_bezier(p_belly_low, (77.5, 19.5), (81.5, 20.8), p_paw_bot_l, 10),
    *_bezier(p_paw_bot_l, (85.2, 26.2), (87.5, 26.2), p_paw_tip_bot, 8),
    *_bezier(p_paw_tip_bot, (92.0, 26.2), (91.8, 31.2), p_paw_tip_top, 10),
    *_bezier(p_paw_tip_top, (85.5, 31.6), (83.2, 30.8), p_chin_join, 8),
]
Icon.draw_round_polyline(arm_and_paw_line, width_units=w, color=Icon.DARK)

# Lower belly, hind foot, and flat bottom base back to tail root
bottom_and_hind_foot_line = [
    p_belly_low,
    *_bezier(p_belly_low, (74.0, 16.5), (72.2, 13.5), p_hind_ankle, 10),
    p_hind_toe_top,
    *_bezier(p_hind_toe_top, (78.5, 11.8), (78.2, 6.5), p_hind_toe_bot, 10),
    p_rump_bot,
]
Icon.draw_round_polyline(bottom_and_hind_foot_line, width_units=w, color=Icon.DARK)

# 4. Eye and small nose tip
circle((84.8, 44.5), radius=1.9, style=Icon.fill_style(Icon.DARK))

nose_pts = [
    (91.5, 40.5),
    p_nose_tip,
    (92.4, 38.2),
]
polygon(nose_pts, style=Icon.no_border_fill(Icon.DARK))
Icon.draw_round_polyline(nose_pts, width_units=1.0, color=Icon.DARK, closed=True)

save()
