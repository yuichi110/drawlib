# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: snyk."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
cx = 50.0

SHIELD_LEFT = Colors.Gray2
SHIELD_RIGHT = "#DFE6EE"
COAT = "#6173DF"
TAN = "#F3A366"


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 16,
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


def _mirror(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Mirror point list horizontally across x = 50.0."""
    return [(100.0 - x, y) for x, y in pts]


# 1. Background heraldic shield (two-tone cool pastel grey)
shield_left_half = [
    (50.0, 74.8),
    *_cubic((50.0, 74.8), (38.0, 74.2), (27.5, 72.0), (22.0, 70.0), 12),
    *_cubic((22.0, 70.0), (19.8, 69.2), (19.2, 67.8), (19.2, 65.5), 8),
    (19.2, 39.5),
    *_cubic((19.2, 39.5), (19.2, 24.5), (33.0, 15.2), (50.0, 10.2), 20),
]
shield_right_half = _mirror(shield_left_half)
shield_outline = shield_left_half + list(reversed(shield_right_half[1:-1]))

polygon(shield_left_half, style=Icon.no_border_fill(SHIELD_LEFT))
polygon(shield_right_half, style=Icon.no_border_fill(SHIELD_RIGHT))
Icon.draw_round_polyline(shield_outline, width_units=w, color=Icon.DARK, closed=True)

# 2. Doberman neck, head, and tall pointed ears (COAT)
# Neck base follows the exact bottom curve of the shield from shield_left_half[-7]
neck_bottom_left = shield_left_half[-7:]
neck_start_left = neck_bottom_left[0]
head_left = [
    neck_start_left,
    (37.4, 38.2),
    *_cubic((37.4, 38.2), (35.0, 41.8), (34.4, 44.5), (34.6, 48.0), 10),
    *_cubic((34.6, 48.0), (34.8, 52.0), (35.2, 55.2), (35.6, 57.8), 8),
    # Outer left ear
    *_cubic((35.6, 57.8), (32.5, 62.5), (31.4, 65.5), (32.2, 69.5), 10),
    *_cubic((32.2, 69.5), (33.5, 75.5), (37.8, 82.5), (39.2, 89.2), 14),
    # Inner left ear down to crown
    *_cubic((39.2, 89.2), (40.5, 89.2), (42.0, 74.5), (43.8, 63.2), 14),
    # Forehead crown to center
    *_cubic((43.8, 63.2), (46.5, 64.2), (48.2, 64.5), (50.0, 64.5), 8),
]
head_right = _mirror(head_left)
neck_bottom_right = _mirror(neck_bottom_left)
dog_outline = (
    head_left + list(reversed(head_right[:-1])) + neck_bottom_right[1:] + list(reversed(neck_bottom_left[1:-1]))
)
polygon(dog_outline, style=Icon.no_border_fill(COAT))

# 3. Peach-tan inner ears (TAN)
ear_in_left = [
    (36.8, 61.2),
    *_cubic((36.8, 61.2), (33.6, 65.2), (33.6, 69.5), (35.8, 75.0), 12),
    *_cubic((35.8, 75.0), (37.2, 78.2), (38.2, 80.5), (38.8, 81.2), 8),
    *_cubic((38.8, 81.2), (39.8, 75.5), (40.2, 68.5), (39.4, 64.2), 12),
    *_cubic((39.4, 64.2), (38.8, 62.5), (37.8, 61.5), (36.8, 61.2), 6),
]
ear_in_right = _mirror(ear_in_left)
for ear_in in (ear_in_left, ear_in_right):
    polygon(ear_in, style=Icon.no_border_fill(TAN))
    Icon.draw_round_polyline(ear_in, width_units=1.6, color=Icon.DARK, closed=True)

# 4. Peach-tan muzzle cheeks (TAN) + chin & white teeth
# Chin underneath jowls
chin_pts = [
    (44.8, 26.2),
    *_cubic((44.8, 26.2), (45.8, 22.8), (54.2, 22.8), (55.2, 26.2), 14),
    (50.0, 28.5),
]
polygon(chin_pts, style=Icon.no_border_fill(TAN))

# Tiny white teeth arch at top of chin
teeth_pts = [
    (46.8, 26.2),
    *_cubic((46.8, 26.2), (48.5, 25.4), (51.5, 25.4), (53.2, 26.2), 8),
    (50.0, 29.0),
]
polygon(teeth_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(
    [(46.8, 26.2), *_cubic((46.8, 26.2), (48.5, 25.4), (51.5, 25.4), (53.2, 26.2), 8)],
    width_units=1.5,
    color=Icon.DARK,
)
Icon.draw_round_polyline(
    [(44.8, 26.2), *_cubic((44.8, 26.2), (45.8, 22.8), (54.2, 22.8), (55.2, 26.2), 14)],
    width_units=1.8,
    color=Icon.DARK,
)

# Tan cheek patches (leaving purple nasal bridge down the center)
muzzle_tan_left = [
    (38.0, 39.2),
    *_cubic((38.0, 39.2), (40.5, 39.8), (43.5, 41.2), (45.8, 43.2), 10),
    (46.4, 34.5),
    (50.0, 34.5),
    (50.0, 28.8),
    *_cubic((50.0, 28.8), (48.2, 26.0), (43.5, 25.5), (41.6, 28.2), 10),
    *_cubic((41.6, 28.2), (40.5, 30.0), (40.5, 33.5), (39.8, 35.8), 8),
    (38.0, 39.2),
]
muzzle_tan_right = _mirror(muzzle_tan_left)
polygon(muzzle_tan_left, style=Icon.no_border_fill(TAN))
polygon(muzzle_tan_right, style=Icon.no_border_fill(TAN))

# 5. Eyebrow dots (TAN, borderless ovals)
ellipse((43.8, 54.0), width=5.6, height=3.2, style=Icon.fill_style(TAN, angle=-18.0))
ellipse((56.2, 54.0), width=5.6, height=3.2, style=Icon.fill_style(TAN, angle=18.0))

# 6. Watchful half-lidded eyes (WHITE sclera + DARK pupil + tiny catchlight)
for side in (-1.0, 1.0):
    ex_out = 50.0 + side * 10.6
    ex_in = 50.0 + side * 3.8
    ey_out = 50.6
    ey_in = 50.1
    lid_l = (ex_out, ey_out) if side < 0 else (ex_in, ey_in)
    lid_r = (ex_in, ey_in) if side < 0 else (ex_out, ey_out)
    eye_cx = 50.0 + side * 7.2
    sclera_pts = [
        lid_l,
        lid_r,
        *_cubic(
            lid_r,
            (eye_cx + 3.2, 46.2),
            (eye_cx - 3.2, 46.2),
            lid_l,
            14,
        ),
    ]
    polygon(sclera_pts, style=Icon.no_border_fill(Icon.WHITE))
    # Pupil clipped under top eyelid
    pupil_pts: list[tuple[float, float]] = []
    pr = 1.65
    pcx, pcy = eye_cx, 49.3
    for i in range(17):
        a = math.radians(180.0 + 180.0 * (i / 16))
        pupil_pts.append((pcx + pr * math.cos(a), pcy + pr * math.sin(a)))
    pupil_pts.extend([(pcx + pr, pcy + 0.8), (pcx - pr, pcy + 0.8)])
    polygon(pupil_pts, style=Icon.no_border_fill(Icon.DARK))
    # Tiny white catchlight on left side of pupil
    circle((pcx - 0.75, pcy - 0.05), radius=0.42, style=Icon.no_border_fill(Icon.WHITE))
    # Eye outline + slightly thicker upper lid
    Icon.draw_round_polyline(sclera_pts, width_units=1.6, color=Icon.DARK, closed=True)
    Icon.draw_round_segment(lid_l, lid_r, width_units=1.8, color=Icon.DARK)

# 7. Nose (DARK) and jowl/muzzle outlines
nose_pts = [
    (50.0, 36.2),
    *_cubic((50.0, 36.2), (54.2, 36.2), (54.8, 34.0), (53.6, 32.2), 10),
    *_cubic((53.6, 32.2), (52.4, 30.8), (51.0, 30.5), (50.0, 30.5), 8),
    *_cubic((50.0, 30.5), (49.0, 30.5), (47.6, 30.8), (46.4, 32.2), 8),
    *_cubic((46.4, 32.2), (45.2, 34.0), (45.8, 36.2), (50.0, 36.2), 10),
]
polygon(nose_pts, style=Icon.no_border_fill(Icon.DARK))
Icon.draw_round_segment((50.0, 31.0), (50.0, 28.6), width_units=1.8, color=Icon.DARK)

# Jowl curves from jaw down to center philtrum
jowl_left = [
    (37.4, 38.2),
    *_cubic((37.4, 38.2), (39.6, 35.8), (40.5, 33.5), (40.8, 29.8), 10),
    *_cubic((40.8, 29.8), (41.2, 25.8), (47.5, 25.2), (50.0, 28.6), 12),
]
jowl_right = _mirror(jowl_left)
Icon.draw_round_polyline(jowl_left, width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(jowl_right, width_units=w, color=Icon.DARK)

# 8. Crisp outer head/ear/neck contours & forehead crease
# Left and right neck lines
Icon.draw_round_segment(neck_start_left, (37.4, 38.2), width_units=w, color=Icon.DARK)
Icon.draw_round_segment(neck_bottom_right[0], (62.6, 38.2), width_units=w, color=Icon.DARK)

# Left and right head + ear outlines
head_ear_left = head_left[1:-1]
head_ear_right = _mirror(head_ear_left)
Icon.draw_round_polyline(head_ear_left, width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(head_ear_right, width_units=w, color=Icon.DARK)

# Overlapping crown arch & temple notches
crown_arch = [
    (41.8, 62.2),
    *_cubic((41.8, 62.2), (45.5, 64.5), (54.5, 64.5), (58.2, 62.2), 14),
]
Icon.draw_round_polyline(crown_arch, width_units=w, color=Icon.DARK)
Icon.draw_round_segment((35.6, 57.8), (36.2, 59.6), width_units=1.7, color=Icon.DARK)
Icon.draw_round_segment((64.4, 57.8), (63.8, 59.6), width_units=1.7, color=Icon.DARK)

# 9. Re-stroke bottom V of shield so neck terminates cleanly inside shield frame
shield_bottom_v = shield_left_half[-10:] + list(reversed(shield_right_half[-10:-1]))
Icon.draw_round_polyline(shield_bottom_v, width_units=w, color=Icon.DARK)

save()
