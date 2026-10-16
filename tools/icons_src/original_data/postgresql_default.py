# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: postgresql."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

# Slightly brightened slate-blue palette based on Pattern 1 (#3B6E99 -> #467BA6)
HEAD_BLUE = "#467BA6"
EAR_INNER = "#38678D"
TUSK_WHITE = "#F4F6F8"
TUSK_SHADE = "#D9E1E8"


def _cubic(
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

w = 1.9

# ---------------------------------------------------------------------------
# 1. Left ear (behind head): outer rim in HEAD_BLUE, inner lobe in EAR_INNER
# ---------------------------------------------------------------------------
left_ear_outer = [
    (41.5, 88.2),
    *_cubic((41.5, 88.2), (34.0, 92.0), (22.5, 92.4), (15.0, 88.0), 18),
    *_cubic((15.0, 88.0), (7.8, 83.8), (7.2, 72.8), (9.8, 59.8), 18),
    *_cubic((9.8, 59.8), (12.2, 47.8), (16.4, 36.8), (21.2, 31.2), 16),
    *_cubic((21.2, 31.2), (24.0, 28.0), (27.4, 28.8), (31.2, 33.8), 14),
    *_cubic((31.2, 33.8), (34.4, 38.0), (37.2, 41.6), (39.6, 44.2), 12),
]
polygon(left_ear_outer, style=no_border_fill(HEAD_BLUE))

left_ear_inner = [
    (40.2, 85.4),
    *_cubic((40.2, 85.4), (33.2, 89.0), (23.2, 89.2), (16.8, 85.4), 16),
    *_cubic((16.8, 85.4), (10.8, 81.8), (10.2, 72.0), (12.6, 59.8), 16),
    *_cubic((12.6, 59.8), (14.8, 48.6), (18.6, 38.6), (22.8, 33.8), 14),
    *_cubic((22.8, 33.8), (24.8, 31.4), (27.2, 32.0), (30.4, 36.2), 12),
    *_cubic((30.4, 36.2), (33.5, 40.2), (36.2, 43.4), (38.6, 45.8), 10),
]
polygon(left_ear_inner, style=no_border_fill(EAR_INNER))
draw_round_polyline(left_ear_outer, width_units=w, color=DARK, closed=True)

# ---------------------------------------------------------------------------
# 2. Right ear (behind head): outer rim in HEAD_BLUE, inner lobe in EAR_INNER
# ---------------------------------------------------------------------------
right_ear_outer = [
    (58.5, 90.0),
    *_cubic((58.5, 90.0), (65.5, 93.2), (75.8, 93.2), (83.5, 88.8), 18),
    *_cubic((83.5, 88.8), (90.8, 84.6), (92.8, 75.2), (90.2, 64.0), 18),
    *_cubic((90.2, 64.0), (87.8, 53.2), (82.4, 44.2), (77.5, 39.8), 16),
    *_cubic((77.5, 39.8), (75.2, 38.0), (73.0, 42.0), (73.0, 48.0), 10),
]
polygon(right_ear_outer, style=no_border_fill(HEAD_BLUE))

right_ear_inner = [
    (60.0, 87.4),
    *_cubic((60.0, 87.4), (66.4, 90.2), (75.2, 90.0), (81.6, 86.2), 16),
    *_cubic((81.6, 86.2), (87.8, 82.6), (89.6, 74.4), (87.4, 64.2), 16),
    *_cubic((87.4, 64.2), (85.2, 54.2), (80.4, 46.0), (76.0, 41.8), 14),
    *_cubic((76.0, 41.8), (74.2, 40.4), (72.5, 44.0), (72.5, 49.0), 10),
]
polygon(right_ear_inner, style=no_border_fill(EAR_INNER))
draw_round_polyline(right_ear_outer, width_units=w, color=DARK, closed=True)

# ---------------------------------------------------------------------------
# 3. Left tusk & Right tusk (behind trunk root / cheek fold)
# ---------------------------------------------------------------------------
left_tusk = [
    (43.5, 41.2),
    # Upper curve flowing seamlessly down-left from left_brow_cheek
    *_cubic((43.5, 41.2), (41.8, 36.8), (38.6, 34.0), (34.4, 32.8), 14),
    # Rounded left tip
    *_cubic((34.4, 32.8), (32.4, 32.2), (32.5, 29.8), (35.4, 29.2), 12),
    # Lower curve sweeping back up-right into trunk base
    *_cubic((35.4, 29.2), (40.8, 28.0), (46.8, 30.6), (49.8, 35.0), 14),
    *_cubic((49.8, 35.0), (50.2, 38.2), (47.5, 40.8), (43.5, 41.2), 10),
]
polygon(left_tusk, style=no_border_fill(TUSK_WHITE))

left_tusk_shade = [
    (33.4, 31.2),
    *_cubic((33.4, 31.2), (39.5, 30.4), (45.2, 32.6), (49.6, 37.0), 14),
    (49.8, 35.0),
    *_cubic((49.8, 35.0), (46.8, 30.6), (40.8, 28.0), (35.4, 29.2), 14),
    *_cubic((35.4, 29.2), (33.5, 29.6), (33.0, 30.6), (33.4, 31.2), 6),
]
polygon(left_tusk_shade, style=no_border_fill(TUSK_SHADE))
draw_round_polyline(left_tusk, width_units=w, color=DARK, closed=True)

right_tusk = [
    (75.8, 42.4),
    # Upper curve flowing seamlessly down-right from right_brow_cheek
    *_cubic((75.8, 42.4), (79.2, 40.2), (84.8, 40.6), (89.4, 41.8), 14),
    # Rounded right tip
    *_cubic((89.4, 41.8), (92.0, 42.4), (92.4, 39.4), (90.0, 37.0), 12),
    # Lower curve sweeping back into right trunk wall
    *_cubic((90.0, 37.0), (85.2, 32.6), (78.2, 32.0), (72.2, 34.4), 14),
    *_cubic((72.2, 34.4), (71.8, 38.2), (73.2, 41.4), (75.8, 42.4), 10),
]
polygon(right_tusk, style=no_border_fill(TUSK_WHITE))

right_tusk_shade = [
    (91.2, 40.0),
    *_cubic((91.2, 40.0), (85.8, 35.4), (78.6, 34.5), (72.2, 36.4), 14),
    (72.2, 34.4),
    *_cubic((72.2, 34.4), (78.2, 32.0), (85.2, 32.6), (90.0, 37.0), 14),
    *_cubic((90.0, 37.0), (91.4, 38.4), (91.6, 39.4), (91.2, 40.0), 6),
]
polygon(right_tusk_shade, style=no_border_fill(TUSK_SHADE))
draw_round_polyline(right_tusk, width_units=w, color=DARK, closed=True)

# ---------------------------------------------------------------------------
# 4. Head dome + Trunk (continuous 3/4 Slonik silhouette in HEAD_BLUE)
# ---------------------------------------------------------------------------
head_trunk = [
    # Start at left brow junction
    (32.8, 66.2),
    # Cranium dome up and over to right brow junction
    *_cubic((32.8, 66.2), (33.5, 81.5), (41.5, 91.0), (52.5, 91.0), 20),
    *_cubic((52.5, 91.0), (64.5, 91.0), (75.5, 81.5), (76.8, 69.2), 20),
    # Right outer cheek down to right tusk top
    *_cubic((76.8, 69.2), (76.3, 62.0), (77.3, 53.5), (75.8, 42.4), 16),
    # Right trunk root curving down into trunk right wall
    *_cubic((75.8, 42.4), (73.2, 41.2), (72.6, 38.5), (72.2, 33.5), 12),
    *_cubic((72.2, 33.5), (71.5, 24.5), (70.4, 15.5), (67.5, 11.2), 16),
    # Rounded trunk tip at bottom
    *_cubic((67.5, 11.2), (65.0, 7.5), (55.5, 7.2), (52.5, 11.2), 16),
    # Left trunk wall up to left tusk top
    *_cubic((52.5, 11.2), (49.8, 15.0), (49.6, 25.5), (49.6, 36.5), 16),
    *_cubic((49.6, 36.5), (49.6, 40.2), (46.8, 41.2), (43.5, 41.2), 12),
    # Left cheek up to left brow junction
    *_cubic((43.5, 41.2), (35.5, 42.5), (32.0, 48.0), (32.6, 56.5), 16),
    *_cubic((32.6, 56.5), (32.8, 61.0), (32.6, 63.8), (32.8, 66.2), 10),
]
polygon(head_trunk, style=no_border_fill(HEAD_BLUE))
draw_round_polyline(head_trunk, width_units=w, color=DARK, closed=True)

# ---------------------------------------------------------------------------
# 5. Internal brow-to-cheek lines (framing the eyes & trunk bridge)
# ---------------------------------------------------------------------------
left_brow_cheek = [
    (32.8, 66.2),
    *_cubic((32.8, 66.2), (38.5, 71.2), (45.2, 71.8), (47.6, 66.8), 16),
    *_cubic((47.6, 66.8), (49.5, 62.5), (49.2, 54.0), (46.4, 47.0), 16),
    *_cubic((46.4, 47.0), (45.0, 43.8), (44.1, 42.2), (43.5, 41.2), 10),
]
draw_round_polyline(left_brow_cheek, width_units=w, color=DARK, closed=False)

right_brow_cheek = [
    (76.8, 69.2),
    *_cubic((76.8, 69.2), (72.5, 71.5), (67.2, 71.0), (65.8, 66.5), 16),
    *_cubic((65.8, 66.5), (64.6, 62.5), (67.6, 54.5), (72.0, 47.8), 16),
    *_cubic((72.0, 47.8), (74.0, 44.8), (75.0, 43.2), (75.8, 42.4), 10),
]
draw_round_polyline(right_brow_cheek, width_units=w, color=DARK, closed=False)

# ---------------------------------------------------------------------------
# 6. Solid dark round dot eyes
# ---------------------------------------------------------------------------
circle((43.4, 65.5), radius=2.45, style=fill_style(DARK))
circle((70.2, 65.4), radius=2.45, style=fill_style(DARK))

save()
