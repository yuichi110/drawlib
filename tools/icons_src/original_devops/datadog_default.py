# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: datadog."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
EAR_SHADOW = "#C5B3E6"


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
                (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


def _tilted_rounded_rect(
    cx: float,
    cy: float,
    width: float,
    height: float,
    r: float,
    deg: float,
    steps_corner: int = 10,
) -> list[tuple[float, float]]:
    """Build a smooth tilted rounded rectangle polygon rotated by deg degrees CCW."""
    hw = width / 2.0
    hh = height / 2.0
    rad = math.radians(deg)
    ca, sa = math.cos(rad), math.sin(rad)

    corners = [
        (hw - r, hh - r, 0.0, 90.0),
        (-hw + r, hh - r, 90.0, 180.0),
        (-hw + r, -hh + r, 180.0, 270.0),
        (hw - r, -hh + r, 270.0, 360.0),
    ]
    pts: list[tuple[float, float]] = []
    for ox, oy, a0, a1 in corners:
        for i in range(steps_corner + 1):
            a = math.radians(a0 + (a1 - a0) * (i / steps_corner))
            lx = ox + r * math.cos(a)
            ly = oy + r * math.sin(a)
            pts.append((cx + lx * ca - ly * sa, cy + lx * sa + ly * ca))
    return pts


# 1. Slightly tilted rounded square backdrop in Colors.Purple2
backdrop_pts = _tilted_rounded_rect(47.5, 52.2, width=66.5, height=68.0, r=7.0, deg=7.2)
polygon(backdrop_pts, style=no_border_fill(Colors.Purple2))
draw_round_polyline(backdrop_pts, width_units=w, color=DARK, closed=True)

# 2. Right floppy ear (drawn behind right forehead curve for seamless overlap)
right_ear_pts: list[tuple[float, float]] = [
    (53.5, 79.5),
    *_cubic((53.5, 79.5), (56.8, 83.2), (59.8, 86.2), (63.0, 85.6), 12),
    *_cubic((63.0, 85.6), (67.5, 84.6), (72.2, 77.2), (72.0, 72.2), 14),
    *_cubic((72.0, 72.2), (71.8, 69.8), (68.2, 69.5), (65.2, 72.0), 10),
    *_cubic((65.2, 72.0), (63.8, 75.5), (62.5, 78.5), (61.6, 80.5), 8),
    (57.0, 76.5),
]
polygon(right_ear_pts, style=no_border_fill(WHITE))

# Soft lavender (#C5B3E6) shadow inside right ear
right_ear_shadow: list[tuple[float, float]] = [
    (57.8, 78.2),
    *_cubic((57.8, 78.2), (61.0, 76.2), (63.6, 74.0), (65.2, 72.0), 10),
    *_cubic((65.2, 72.0), (63.8, 75.5), (62.5, 78.5), (61.6, 80.5), 8),
]
polygon(right_ear_shadow, style=no_border_fill(EAR_SHADOW))

# Right ear outer DARK w=1.9 border (from crown up over ear tip and into inner crease)
draw_round_polyline(right_ear_pts[:-1], width_units=w, color=DARK, closed=False)

# 3. Cute friendly WHITE dog head, neck & chest silhouette
dog_head_pts: list[tuple[float, float]] = [
    (41.0, 14.2),
    # Chest bottom curve sticking slightly below purple frame
    *_cubic((41.0, 14.2), (34.0, 11.2), (24.5, 11.8), (21.2, 16.5), 14),
    # Lower chest left curve up into neck indentation
    *_cubic((21.2, 16.5), (18.2, 21.5), (21.5, 28.0), (28.5, 33.8), 14),
    # Smooth S-curve from neck into left cheek (collinear tangent at (29.2, 47.0))
    *_cubic((28.5, 33.8), (33.8, 38.2), (33.5, 42.8), (29.2, 47.0), 12),
    *_cubic((29.2, 47.0), (25.2, 51.0), (24.4, 57.5), (24.8, 62.5), 12),
    # Left floppy ear outer contour
    *_cubic((24.8, 62.5), (20.0, 63.6), (16.4, 69.2), (17.4, 74.2), 14),
    *_cubic((17.4, 74.2), (18.4, 78.5), (23.8, 82.2), (28.2, 83.0), 12),
    *_cubic((28.2, 83.0), (31.8, 83.5), (34.5, 81.0), (37.2, 78.5), 10),
    # Head crown dome across to right brow
    *_cubic((37.2, 78.5), (43.0, 81.6), (49.2, 81.6), (53.5, 79.5), 14),
    # Continuous smooth right forehead & brow curve down to snout
    *_cubic((53.5, 79.5), (60.8, 77.5), (67.2, 70.5), (68.0, 63.5), 16),
    # Right snout (muzzle) bulge down behind chart card
    *_cubic((68.0, 63.5), (73.0, 59.5), (74.2, 52.2), (71.2, 44.2), 16),
    # Hidden closure behind chart card and paw
    (52.0, 25.0),
]
polygon(dog_head_pts, style=no_border_fill(WHITE))

# Soft lavender (#C5B3E6) crescent shadow under left ear
left_ear_shadow: list[tuple[float, float]] = [
    (24.9, 62.3),
    *_cubic((24.9, 62.3), (24.6, 57.0), (28.5, 55.6), (32.8, 59.2), 12),
    *_cubic((32.8, 59.2), (36.8, 62.8), (36.5, 71.0), (32.4, 75.8), 12),
    (31.5, 74.8),
    *_cubic((31.5, 74.8), (34.2, 67.0), (31.5, 61.2), (24.9, 62.3), 12),
]
polygon(left_ear_shadow, style=no_border_fill(EAR_SHADOW))

# Dog head & chest outer DARK w=1.9 border
draw_round_polyline(dog_head_pts[:-1], width_units=w, color=DARK, closed=False)

# Left ear inner lobe crease (continuous from cheek edge up into ear)
left_ear_inner: list[tuple[float, float]] = [
    (24.8, 62.5),
    *_cubic((24.8, 62.5), (29.2, 61.0), (33.5, 63.8), (33.0, 69.8), 12),
    *_cubic((33.0, 69.8), (32.8, 72.8), (32.0, 75.2), (31.4, 76.6), 8),
]
draw_round_polyline(left_ear_inner, width_units=w, color=DARK, closed=False)

# 4. Shiny DARK eyes with WHITE catchlights
left_eye_pts: list[tuple[float, float]] = [
    (43.2, 63.8),
    *_cubic((43.2, 63.8), (42.6, 67.5), (44.8, 70.0), (47.5, 69.6), 12),
    *_cubic((47.5, 69.6), (50.2, 69.2), (51.2, 66.2), (50.4, 63.5), 12),
    *_cubic((50.4, 63.5), (48.2, 62.4), (45.2, 62.6), (43.2, 63.8), 10),
]
polygon(left_eye_pts, style=fill_style(DARK))
circle((47.6, 66.8), radius=1.25, style=fill_style(WHITE))

ellipse((63.3, 67.8), width=5.2, height=7.4, style=fill_style(DARK, angle=6.0))
circle((62.9, 69.1), radius=1.05, style=fill_style(WHITE))

# 5. DARK rounded nose and gentle smile line
nose_pts: list[tuple[float, float]] = [
    (60.5, 56.2),
    *_cubic((60.5, 56.2), (61.2, 58.6), (67.8, 59.0), (69.4, 56.8), 12),
    *_cubic((69.4, 56.8), (70.4, 55.2), (68.2, 52.0), (65.4, 51.8), 12),
    *_cubic((65.4, 51.8), (62.5, 51.6), (60.0, 54.2), (60.5, 56.2), 12),
]
polygon(nose_pts, style=fill_style(DARK))

smile_pts: list[tuple[float, float]] = [
    (44.8, 49.0),
    *_cubic((44.8, 49.0), (49.5, 42.2), (58.2, 41.2), (63.2, 45.2), 14),
    *_cubic((63.2, 45.2), (64.8, 46.8), (65.5, 49.5), (65.4, 52.0), 8),
]
draw_round_polyline(smile_pts, width_units=w, color=DARK, closed=False)

# 6. Tilted WHITE chart card at bottom-right + Colors.Purple2 mountain area chart
card_pts = _tilted_rounded_rect(67.2, 28.5, width=41.5, height=29.2, r=4.2, deg=7.2)
polygon(card_pts, style=no_border_fill(WHITE))
draw_round_polyline(card_pts, width_units=w, color=DARK, closed=True)

chart_pts: list[tuple[float, float]] = [
    (52.0, 15.8),
    (84.6, 20.0),
    (82.6, 39.2),
    (76.6, 30.2),
    (70.5, 34.4),
    (64.6, 24.5),
    (58.0, 27.9),
    (51.8, 18.5),
]
polygon(chart_pts, style=no_border_fill(Colors.Purple2))
draw_round_polyline(chart_pts, width_units=1.7, color=DARK, closed=True)

# 7. Round WHITE paw at bottom-left overlapping chart card
circle(
    (42.2, 19.6),
    radius=8.4,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

save()
