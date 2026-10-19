# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: jenkins."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_inner = 1.65

PEACH = "#FFE4C4"
SLATE_BLUE = "#68849E"


def _quad(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 14,
) -> list[tuple[float, float]]:
    """Sample quadratic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0],
                (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1],
            )
        )
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
                (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


# 1. Coral-red background circle (Colors.Red3)
circle(
    (49.5, 49.5),
    radius=30.5,
    style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w),
)

# 2. Slate-blue butler jacket (#68849E)
jacket_pts = [
    (38.5, 51.5),
    *_quad((38.5, 51.5), (32.0, 48.0), (27.2, 44.5), 10),
    *_quad((27.2, 44.5), (25.5, 43.2), (26.2, 40.5), 6),
    *_quad((26.2, 40.5), (29.2, 32.0), (30.2, 22.0), 10),
    *_quad((30.2, 22.0), (30.6, 19.8), (33.5, 18.5), 6),
    *_quad((33.5, 18.5), (38.0, 16.5), (43.5, 16.5), 8),
    (60.5, 20.0),
    (67.5, 30.0),
    *_quad((67.5, 30.0), (70.5, 37.5), (72.5, 44.5), 10),
    *_quad((72.5, 44.5), (73.0, 46.2), (71.2, 47.8), 6),
    (66.0, 51.5),
]
polygon(jacket_pts, style=Icon.no_border_fill(SLATE_BLUE))
Icon.draw_round_polyline(jacket_pts, width_units=w, color=Icon.DARK, closed=True)

# 3. White shirt collar & V-front (WHITE)
shirt_collar_l = [
    (39.5, 50.8),
    (49.0, 47.2),
    (48.0, 43.0),
    *_quad((48.0, 43.0), (42.5, 45.8), (39.5, 50.8), 8),
]
polygon(shirt_collar_l, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(shirt_collar_l, width_units=w_inner, color=Icon.DARK, closed=True)

shirt_v = [
    (54.0, 43.0),
    (62.2, 43.0),
    (60.5, 30.0),
]
polygon(shirt_v, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(shirt_v, width_units=w_inner, color=Icon.DARK, closed=True)

# Jacket lapel notches framing the shirt V
lapel_l = [(54.0, 41.0), (50.2, 36.2), (60.2, 30.0)]
lapel_r = [(62.5, 41.2), (66.5, 38.2), (60.8, 30.0)]
Icon.draw_round_polyline(lapel_l, width_units=w_inner, color=Icon.DARK, closed=False)
Icon.draw_round_polyline(lapel_r, width_units=w_inner, color=Icon.DARK, closed=False)

# Left sleeve fold lines
Icon.draw_round_segment((41.4, 37.5), (42.0, 29.2), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((38.5, 29.2), (42.0, 29.2), width_units=w_inner, color=Icon.DARK)

# 4. Butler head dome, hair rim & ear
# Back-left bald hair rim crescent (PEACH)
bald_rim = [
    (33.8, 75.5),
    *_cubic((33.8, 75.5), (36.2, 84.2), (43.5, 88.6), (52.5, 87.5), 16),
    (52.0, 82.0),
    (42.0, 74.0),
]
polygon(bald_rim, style=Icon.no_border_fill(PEACH))
Icon.draw_round_polyline(bald_rim, width_units=w, color=Icon.DARK, closed=True)

# Side hair tuft above ear (SLATE_BLUE)
hair_tuft = [
    (32.0, 68.5),
    *_quad((32.0, 68.5), (31.5, 75.5), (36.5, 78.5), 10),
    *_quad((36.5, 78.5), (39.5, 79.8), (40.2, 77.2), 6),
    *_quad((40.2, 77.2), (39.5, 71.0), (40.2, 66.8), 8),
    (39.0, 65.5),
    *_quad((39.0, 65.5), (36.5, 69.5), (32.0, 68.5), 8),
]
polygon(hair_tuft, style=Icon.no_border_fill(SLATE_BLUE))
Icon.draw_round_polyline(hair_tuft, width_units=w, color=Icon.DARK, closed=True)

# Main face & dome (PEACH)
face_pts = [
    (39.8, 77.5),
    *_cubic((39.8, 77.5), (43.5, 85.8), (50.0, 89.2), (56.5, 88.5), 16),
    *_cubic((56.5, 88.5), (65.5, 87.2), (71.2, 79.0), (71.2, 67.5), 16),
    *_cubic((71.2, 67.5), (71.2, 55.5), (65.2, 48.2), (55.5, 48.2), 16),
    *_cubic((55.5, 48.2), (44.0, 48.2), (38.2, 52.5), (36.2, 59.5), 14),
    # Ear outer C-loop
    *_cubic((36.2, 59.5), (31.0, 59.2), (29.5, 64.5), (31.8, 68.2), 12),
    *_quad((31.8, 68.2), (34.5, 71.2), (38.8, 66.2), 10),
    *_quad((38.8, 66.2), (40.2, 66.0), (39.8, 71.5), 8),
]
polygon(face_pts, style=Icon.no_border_fill(PEACH))
Icon.draw_round_polyline(face_pts, width_units=w, color=Icon.DARK, closed=True)

# Ear inner curve
ear_inner = [(33.2, 66.0), *_quad((33.2, 66.0), (35.8, 66.5), (36.2, 63.2), 8)]
Icon.draw_round_polyline(ear_inner, width_units=w_inner, color=Icon.DARK, closed=False)

# Chin / jaw crease line
jaw_crease = [(44.5, 55.5), *_quad((44.5, 55.5), (49.5, 49.0), (57.5, 48.5), 12)]
Icon.draw_round_polyline(jaw_crease, width_units=w_inner, color=Icon.DARK, closed=False)

# 5. Facial features (eyebrows, closed butler eyelids, nose, mustache, smile)
# Eyebrows
brow_l = [(46.5, 74.8), *_quad((46.5, 74.8), (49.2, 77.2), (52.5, 77.2), 8)]
brow_r = [(64.2, 77.5), *_quad((64.2, 77.5), (67.2, 77.2), (69.5, 74.8), 8)]
Icon.draw_round_polyline(brow_l, width_units=1.7, color=Icon.DARK, closed=False)
Icon.draw_round_polyline(brow_r, width_units=1.7, color=Icon.DARK, closed=False)

# Calm downward-curved closed butler eyelids + inner vertical creases
lid_l = [(48.5, 69.8), *_quad((48.5, 69.8), (51.8, 67.2), (54.8, 69.8), 10)]
lid_r = [(63.4, 69.8), *_quad((63.4, 69.8), (66.1, 67.4), (68.6, 69.8), 10)]
Icon.draw_round_polyline(lid_l, width_units=1.7, color=Icon.DARK, closed=False)
Icon.draw_round_polyline(lid_r, width_units=1.7, color=Icon.DARK, closed=False)
Icon.draw_round_segment((53.0, 72.8), (53.6, 70.5), width_units=1.4, color=Icon.DARK)
Icon.draw_round_segment((67.0, 72.8), (67.6, 70.5), width_units=1.4, color=Icon.DARK)

# Nose
nose_pts = [
    (60.4, 71.2),
    *_quad((60.4, 71.2), (61.5, 67.5), (63.8, 63.2), 8),
    *_quad((63.8, 63.2), (64.6, 60.8), (62.2, 59.8), 8),
    *_quad((62.2, 59.8), (59.2, 59.2), (56.8, 60.2), 8),
]
Icon.draw_round_polyline(nose_pts, width_units=1.65, color=Icon.DARK, closed=False)

# Parted gentleman mustache
mustache_l = [
    (50.2, 58.6),
    *_quad((50.2, 58.6), (54.8, 57.6), (59.0, 57.8), 8),
    (59.0, 56.4),
    *_quad((59.0, 56.4), (54.2, 56.2), (50.2, 58.6), 8),
]
mustache_r = [
    (60.8, 57.8),
    *_quad((60.8, 57.8), (64.8, 57.8), (68.0, 58.8), 8),
    *_quad((68.0, 58.8), (65.0, 56.4), (60.8, 56.4), 8),
]
polygon(mustache_l, style=Icon.no_border_fill(Icon.DARK))
polygon(mustache_r, style=Icon.no_border_fill(Icon.DARK))
Icon.draw_round_polyline(mustache_l, width_units=1.1, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(mustache_r, width_units=1.1, color=Icon.DARK, closed=True)

# Gentle smile
smile_pts = [(52.0, 54.8), *_quad((52.0, 54.8), (58.0, 52.8), (63.5, 54.6), 12)]
Icon.draw_round_polyline(smile_pts, width_units=1.6, color=Icon.DARK, closed=False)

# 6. Bow tie (Colors.Red3)
bow_l = [
    (56.2, 44.5),
    *_quad((56.2, 44.5), (51.5, 47.2), (48.8, 47.0), 8),
    *_quad((48.8, 47.0), (47.8, 43.2), (49.2, 39.2), 8),
    *_quad((49.2, 39.2), (52.5, 39.5), (56.2, 42.2), 8),
]
bow_r = [
    (59.8, 44.6),
    *_quad((59.8, 44.6), (63.5, 47.2), (65.8, 47.2), 8),
    *_quad((65.8, 47.2), (66.8, 44.0), (65.8, 40.8), 8),
    *_quad((65.8, 40.8), (63.2, 40.5), (59.8, 42.4), 8),
]
bow_knot = [
    (56.2, 45.2),
    (59.8, 45.2),
    (59.8, 41.6),
    (56.2, 41.6),
]
for b_pts in (bow_l, bow_r):
    polygon(b_pts, style=Icon.no_border_fill(Colors.Red3))
    Icon.draw_round_polyline(b_pts, width_units=w_inner, color=Icon.DARK, closed=True)
polygon(bow_knot, style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w_inner, shape_r=1.0))

# 7. Back towel flap, forearm cuff, round gloved hand & front towel
back_towel = [
    (61.0, 20.0),
    (64.8, 20.0),
    (65.4, 13.5),
    *_quad((65.4, 13.5), (63.5, 12.0), (61.2, 12.2), 6),
]
polygon(back_towel, style=Icon.no_border_fill(Colors.Gray2))
Icon.draw_round_polyline(back_towel, width_units=w, color=Icon.DARK, closed=True)

# Forearm jacket cuff (SLATE_BLUE) & white shirt cuff (WHITE)
jacket_cuff = [
    (60.0, 29.2),
    (65.0, 29.0),
    (65.4, 20.2),
    (60.5, 20.0),
]
shirt_cuff = [
    (65.0, 28.6),
    (71.5, 28.4),
    (71.5, 21.0),
    (65.4, 20.6),
]
polygon(jacket_cuff, style=Icon.no_border_fill(SLATE_BLUE))
Icon.draw_round_polyline(jacket_cuff, width_units=w, color=Icon.DARK, closed=True)
polygon(shirt_cuff, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(shirt_cuff, width_units=w, color=Icon.DARK, closed=True)

# Round gloved hand (WHITE)
circle(
    (74.2, 25.0),
    radius=6.4,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

# Front main towel (WHITE)
front_towel = [
    (42.0, 29.2),
    *_quad((42.0, 29.2), (51.0, 30.2), (60.0, 29.4), 12),
    (61.6, 11.6),
    *_quad((61.6, 11.6), (53.8, 10.4), (46.2, 11.8), 12),
    *_quad((46.2, 11.8), (43.2, 18.5), (42.0, 29.2), 12),
]
polygon(front_towel, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(front_towel, width_units=w, color=Icon.DARK, closed=True)

save()
