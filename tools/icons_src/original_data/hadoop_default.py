# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data icon: Hadoop."""

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

# Warm golden yellow slightly darker than Colors.Amber2 (#F8D88C), paired with Colors.Amber3 (#F2B43A)
BODY_YELLOW = "#F5C768"


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

# 1. Far legs (behind the main body)
# Far hind leg (stepping back-left)
far_hind_pts = [
    (17.5, 40.5),
    *_bezier((17.5, 40.5), (15.0, 34.0), (12.2, 28.5), (11.0, 26.2), 8),
    *_bezier((11.0, 26.2), (10.2, 24.8), (11.5, 23.2), (14.2, 20.8), 6),
    *_bezier((14.2, 20.8), (16.5, 18.8), (18.2, 18.8), (19.8, 20.8), 6),
    *_bezier((19.8, 20.8), (21.8, 23.8), (24.0, 27.5), (25.2, 30.5), 8),
]
polygon(far_hind_pts, style=no_border_fill(BODY_YELLOW))
draw_round_polyline(far_hind_pts, width_units=w, color=DARK, closed=True)

# Far front leg (stepping forward-right)
far_front_pts = [
    (62.2, 42.5),
    *_bezier((62.2, 42.5), (66.5, 36.5), (71.2, 27.5), (73.5, 21.0), 10),
    *_bezier((73.5, 21.0), (74.0, 19.2), (73.0, 18.2), (70.8, 18.0), 6),
    *_bezier((70.8, 18.0), (67.8, 17.8), (65.2, 17.5), (63.8, 18.2), 6),
    *_bezier((63.8, 18.2), (62.5, 18.8), (62.0, 20.5), (60.5, 24.5), 6),
    *_bezier((60.5, 24.5), (58.8, 28.5), (56.8, 31.5), (55.5, 33.5), 8),
]
polygon(far_front_pts, style=no_border_fill(BODY_YELLOW))
draw_round_polyline(far_front_pts, width_units=w, color=DARK, closed=True)

# 2. Tail stem and solid dark leaf tuft on the left
draw_round_polyline(
    [(17.2, 55.2), *_bezier((17.2, 55.2), (14.2, 52.8), (12.2, 49.2), (11.5, 45.8), 10)],
    width_units=w,
    color=DARK,
)
tail_tuft = [
    (11.8, 47.2),
    *_bezier((11.8, 47.2), (8.2, 45.8), (7.6, 42.5), (8.6, 39.2), 8),
    *_bezier((8.6, 39.2), (12.2, 40.5), (14.0, 44.2), (11.8, 47.2), 8),
]
polygon(tail_tuft, style=fill_style(DARK))

# 3. Main body, head, trunk, jaw, near front leg, and near hind leg (BODY_YELLOW)
p_rump_bot = (18.8, 36.0)
p_back_ear = (35.5, 70.2)
p_head_ear = (48.0, 75.5)
p_head_top = (59.0, 79.8)
p_forehead = (72.5, 74.0)
p_trunk_dip = (80.0, 61.5)
p_trunk_tip_l = (84.8, 84.0)
p_trunk_tip_m = (86.8, 81.6)
p_trunk_tip_r = (88.4, 79.2)
p_trunk_outer = (90.5, 61.5)
p_trunk_bot = (77.5, 47.8)
p_mouth_in = (68.0, 52.2)
p_jaw_tip = (73.5, 44.5)
p_throat = (64.8, 45.8)
p_chest = (57.2, 36.8)
p_ff_ankle = (48.8, 18.8)
p_ff_toe = (46.2, 18.2)
p_ff_heel = (41.2, 24.5)
p_ff_knee = (45.5, 31.2)
p_belly_l = (33.5, 31.2)
p_nh_toe = (36.2, 18.2)
p_nh_heel = (25.5, 18.2)

body_fill_pts = [
    p_rump_bot,
    *_bezier(p_rump_bot, (15.5, 46.5), (16.5, 59.5), (24.5, 65.8), 14),
    *_bezier((24.5, 65.8), (28.5, 68.5), (32.0, 69.8), p_back_ear, 8),
    p_head_ear,
    *_bezier(p_head_ear, (51.5, 78.2), (55.0, 79.8), p_head_top, 10),
    *_bezier(p_head_top, (65.0, 79.8), (70.0, 77.2), p_forehead, 10),
    *_bezier(p_forehead, (75.5, 70.0), (77.0, 61.8), p_trunk_dip, 12),
    *_bezier(p_trunk_dip, (82.8, 61.2), (83.2, 68.5), (81.5, 74.5), 10),
    *_bezier((81.5, 74.5), (80.5, 78.5), (82.2, 82.8), p_trunk_tip_l, 10),
    *_bezier(p_trunk_tip_l, (85.6, 84.2), (87.8, 81.2), p_trunk_tip_r, 8),
    *_bezier(p_trunk_tip_r, (88.8, 76.2), (90.6, 68.5), p_trunk_outer, 12),
    *_bezier(p_trunk_outer, (90.4, 53.0), (84.5, 47.8), p_trunk_bot, 14),
    *_bezier(p_trunk_bot, (73.5, 47.8), (70.5, 50.0), p_mouth_in, 8),
    *_bezier(p_mouth_in, (71.5, 49.5), (74.2, 46.5), p_jaw_tip, 8),
    *_bezier(p_jaw_tip, (72.5, 43.2), (68.0, 46.0), p_throat, 8),
    *_bezier(p_throat, (62.8, 45.6), (59.5, 40.5), p_chest, 8),
    *_bezier(p_chest, (55.5, 30.0), (52.5, 22.5), p_ff_ankle, 12),
    *_bezier(p_ff_ankle, (48.0, 17.8), (47.0, 17.8), p_ff_toe, 6),
    *_bezier(p_ff_toe, (44.0, 19.5), (41.5, 22.2), p_ff_heel, 8),
    *_bezier(p_ff_heel, (41.0, 26.2), (43.8, 28.8), p_ff_knee, 8),
    *_bezier(p_ff_knee, (41.5, 30.8), (37.5, 30.8), p_belly_l, 8),
    *_bezier(p_belly_l, (34.8, 26.5), (36.0, 21.5), p_nh_toe, 8),
    *_bezier(p_nh_toe, (36.5, 17.8), (35.0, 17.8), (30.8, 17.8), 6),
    *_bezier((30.8, 17.8), (26.5, 17.8), (25.2, 17.8), p_nh_heel, 6),
    *_bezier(p_nh_heel, (23.5, 23.5), (20.8, 30.5), p_rump_bot, 10),
]
polygon(body_fill_pts, style=no_border_fill(BODY_YELLOW))

# 4. Warm golden amber shade along the outer trunk curve (Colors.Amber3)
trunk_shade_pts = [
    p_trunk_tip_m,
    p_trunk_tip_r,
    *_bezier(p_trunk_tip_r, (88.8, 76.2), (90.6, 68.5), p_trunk_outer, 12),
    *_bezier(p_trunk_outer, (90.4, 53.0), (84.5, 47.8), p_trunk_bot, 14),
    *_bezier(p_trunk_bot, (73.5, 47.8), (70.5, 50.0), (69.5, 51.0), 8),
    # Inner edge of the amber trunk shade (parallel ~3.6 units inside)
    *_bezier((69.5, 51.0), (74.5, 50.5), (81.5, 51.2), (85.6, 56.8), 10),
    *_bezier((85.6, 56.8), (87.8, 62.0), (86.8, 69.0), (84.8, 75.2), 10),
    *_bezier((84.8, 75.2), (84.2, 78.0), (85.2, 80.2), p_trunk_tip_m, 8),
]
polygon(trunk_shade_pts, style=no_border_fill(Colors.Amber3))

# 5. Body, head, trunk, jaw, and near-leg outlines (clean open strokes with round caps)
# Rump + near hind leg + belly + near front leg + chest + lower jaw + mouth
back_and_legs_line = [
    p_back_ear,
    *_bezier(p_back_ear, (32.0, 69.8), (28.5, 68.5), (24.5, 65.8), 8),
    *_bezier((24.5, 65.8), (16.5, 59.5), (15.5, 46.5), p_rump_bot, 14),
    *_bezier(p_rump_bot, (20.8, 30.5), (23.5, 23.5), p_nh_heel, 10),
    *_bezier(p_nh_heel, (25.2, 17.8), (26.5, 17.8), (30.8, 17.8), 6),
    *_bezier((30.8, 17.8), (35.0, 17.8), (36.5, 17.8), p_nh_toe, 6),
    *_bezier(p_nh_toe, (36.0, 21.5), (34.8, 26.5), p_belly_l, 8),
    *_bezier(p_belly_l, (33.0, 33.5), (32.2, 35.5), (31.8, 36.8), 6),
]
draw_round_polyline(back_and_legs_line, width_units=w, color=DARK)

# Belly line between near hind leg and near front leg
draw_round_polyline(
    [p_belly_l, *_bezier(p_belly_l, (37.5, 30.8), (41.5, 30.8), p_ff_knee, 8)],
    width_units=w,
    color=DARK,
)

# Near front leg back crease + foot + front crease + smooth chin/throat + lower jaw
front_leg_and_jaw_line = [
    (45.8, 36.8),
    *_bezier((45.8, 36.8), (45.8, 34.5), (45.7, 32.5), p_ff_knee, 6),
    *_bezier(p_ff_knee, (43.8, 28.8), (41.0, 26.2), p_ff_heel, 8),
    *_bezier(p_ff_heel, (41.5, 22.2), (44.0, 19.5), p_ff_toe, 8),
    *_bezier(p_ff_toe, (47.0, 17.8), (48.0, 17.8), p_ff_ankle, 6),
    *_bezier(p_ff_ankle, (52.5, 22.5), (55.5, 30.0), p_chest, 12),
    *_bezier(p_chest, (59.5, 40.5), (62.8, 45.6), p_throat, 8),
    *_bezier(p_throat, (68.0, 46.0), (72.5, 43.2), p_jaw_tip, 8),
    *_bezier(p_jaw_tip, (74.2, 46.5), (71.5, 49.5), (69.5, 51.0), 8),
]
draw_round_polyline(front_leg_and_jaw_line, width_units=w, color=DARK)

# Near front leg upper front crease
draw_round_polyline(
    [(55.8, 32.8), (57.2, 36.8)],
    width_units=w,
    color=DARK,
)

# Head dome + smooth trunk + upper lip / mouth corner
head_and_trunk_line = [
    p_head_ear,
    *_bezier(p_head_ear, (51.5, 78.2), (55.0, 79.8), p_head_top, 10),
    *_bezier(p_head_top, (65.0, 79.8), (70.0, 77.2), p_forehead, 10),
    *_bezier(p_forehead, (75.5, 70.0), (77.0, 61.8), p_trunk_dip, 12),
    *_bezier(p_trunk_dip, (82.8, 61.2), (83.2, 68.5), (81.5, 74.5), 10),
    *_bezier((81.5, 74.5), (80.5, 78.5), (82.2, 82.8), p_trunk_tip_l, 10),
    *_bezier(p_trunk_tip_l, (85.6, 84.2), (87.8, 81.2), p_trunk_tip_r, 8),
    *_bezier(p_trunk_tip_r, (88.8, 76.2), (90.6, 68.5), p_trunk_outer, 12),
    *_bezier(p_trunk_outer, (90.4, 53.0), (84.5, 47.8), p_trunk_bot, 14),
    *_bezier(p_trunk_bot, (73.5, 47.8), (70.5, 50.0), p_mouth_in, 8),
]
draw_round_polyline(head_and_trunk_line, width_units=w, color=DARK)

# 6. Floppy Ear (BODY_YELLOW outer rim + Colors.Amber3 inner pad + open right cheek attachment)
p_ear_top_r = (54.2, 71.8)
p_ear_top_l = (43.5, 75.5)
p_ear_mid_l = (32.8, 62.5)
p_ear_bot = (47.5, 45.0)
p_ear_bot_r = (54.0, 54.5)

ear_outer_pts = [
    p_ear_top_r,
    *_bezier(p_ear_top_r, (51.0, 74.5), (47.5, 75.8), p_ear_top_l, 8),
    *_bezier(p_ear_top_l, (37.5, 75.0), (32.8, 69.0), p_ear_mid_l, 10),
    *_bezier(p_ear_mid_l, (32.8, 56.5), (37.5, 52.8), (41.5, 48.2), 10),
    *_bezier((41.5, 48.2), (44.0, 45.2), (45.8, 44.8), p_ear_bot, 6),
    *_bezier(p_ear_bot, (50.8, 45.2), (53.8, 49.5), p_ear_bot_r, 8),
]
polygon(ear_outer_pts, style=no_border_fill(BODY_YELLOW))

# Inner warm golden amber ear pad with uniform ~3.0-unit BODY_YELLOW rim
ear_inner_pts = [
    (52.5, 69.2),
    *_bezier((52.5, 69.2), (49.5, 71.5), (46.2, 72.2), (43.5, 71.8), 8),
    *_bezier((43.5, 71.8), (39.2, 71.0), (35.8, 66.5), (35.8, 61.8), 8),
    *_bezier((35.8, 61.8), (35.8, 57.2), (39.8, 53.8), (43.5, 49.8), 8),
    *_bezier((43.5, 49.8), (45.5, 47.6), (46.8, 47.2), (48.0, 47.5), 6),
    *_bezier((48.0, 47.5), (50.5, 48.0), (52.5, 51.0), (53.0, 54.8), 8),
    *_bezier((53.0, 54.8), (53.3, 59.5), (53.1, 65.0), (52.5, 69.2), 8),
]
polygon(ear_inner_pts, style=no_border_fill(Colors.Amber3))

# Open C-curve dark outline of the ear
draw_round_polyline(ear_outer_pts, width_units=w, color=DARK)

# 7. Simple solid dark dot eye
circle((65.8, 63.0), radius=2.2, style=fill_style(DARK))

save()
