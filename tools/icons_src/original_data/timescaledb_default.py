# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: timescaledb."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = 1.9
cx, cy = 50.0, 51.0


def _polar(r: float, deg: float) -> tuple[float, float]:
    """Convert polar coordinates around (cx, cy) to canvas (x, y)."""
    rad = math.radians(deg)
    return (cx + r * math.cos(rad), cy + r * math.sin(rad))


def _arc_pts(r: float, deg_start: float, deg_end: float, steps: int = 16) -> list[tuple[float, float]]:
    """Sample circular arc points around (cx, cy)."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        deg = deg_start + (deg_end - deg_start) * (i / steps)
        pts.append(_polar(r, deg))
    return pts


# 1. Left & right geometric tiger ears (Colors.Amber2)
for sign in (-1.0, 1.0):
    a_in = 90.0 - sign * 30.0
    a_out = 90.0 - sign * 54.0
    ear_pts = [
        _polar(33.0, a_in),
        _polar(41.5, a_in - sign * 3.0),
        _polar(41.5, a_out + sign * 3.0),
        _polar(33.0, a_out),
    ]
    polygon(ear_pts, style=fill_style(Colors.Amber2, border_color=DARK, border_units=w, shape_r=2.5))

# 2. Flared lower-left & lower-right cheek ruff wings (Colors.Amber2)
left_ruff = [
    *_arc_pts(41.5, 194.0, 244.0, 16),
    *_arc_pts(33.0, 244.0, 194.0, 16),
]
right_ruff = [
    *_arc_pts(41.5, -14.0, -64.0, 16),
    *_arc_pts(33.0, -64.0, -14.0, 16),
]
for ruff in (left_ruff, right_ruff):
    polygon(ruff, style=no_border_fill(Colors.Amber2))
    draw_round_polyline(ruff, width_units=w, color=DARK, closed=True)

# 3. Bottom chin block (Colors.Amber2)
chin_pts = [
    *_arc_pts(40.5, 253.0, 287.0, 10),
    *_arc_pts(33.0, 287.0, 253.0, 10),
]
polygon(chin_pts, style=no_border_fill(Colors.Amber2))
draw_round_polyline(chin_pts, width_units=w, color=DARK, closed=True)

# 4. Main circular tiger head rim (Colors.Amber3) with transparent inner clock face
draw_compound_polygon(
    [_arc_pts(34.2, 0.0, 360.0, 64)[:-1], _arc_pts(26.6, 0.0, 360.0, 64)[:-1]],
    color=Colors.Amber3,
)
circle((cx, cy), radius=34.2, style=stroke_style(DARK, width_units=w))
circle((cx, cy), radius=26.6, style=stroke_style(DARK, width_units=1.8))

# 5. Concentric curved tiger-stripe / clock-scale arcs inside face
stripes = [
    (21.8, 114.0, 226.0),
    (21.8, 66.0, -46.0),
    (17.2, 118.0, 156.0),
    (17.2, 196.0, 224.0),
    (17.2, 62.0, 24.0),
]
for r_s, a0, a1 in stripes:
    draw_round_polyline(_arc_pts(r_s, a0, a1, 12), width_units=1.6, color=DARK)

# 6. Two angled geometric tiger eyes (Colors.Orange3)
left_eye = [(33.8, 55.0), (37.0, 57.6), (42.6, 55.4), (41.2, 52.0), (35.8, 52.3)]
right_eye = [(66.2, 55.0), (63.0, 57.6), (57.4, 55.4), (58.8, 52.0), (64.2, 52.3)]
for eye in (left_eye, right_eye):
    polygon(eye, style=no_border_fill(Colors.Orange3))
    draw_round_polyline(eye, width_units=1.5, color=DARK, closed=True)

# 7. Central Timescale clock hands (12:00 vertical + 4:00 angled) in Colors.Orange3
clock_hands = [
    (49.2, 73.0),  # 12:00 tip
    (51.4, 73.0),
    (53.2, 53.3),  # Inner elbow
    (67.8, 41.8),  # 4:00 tip
    (66.4, 39.8),
    (47.2, 50.0),  # Outer elbow
]
polygon(clock_hands, style=no_border_fill(Colors.Orange3))
draw_round_polyline(clock_hands, width_units=1.7, color=DARK, closed=True)

# 8. Geometric tiger nose & mouth below the clock hands
nose_pts = [
    (43.2, 39.2),
    (50.0, 36.5),
    (56.8, 39.2),
    (55.4, 42.0),
    (50.0, 39.8),
    (44.6, 42.0),
]
polygon(nose_pts, style=fill_style(DARK))
draw_round_polyline([(50.0, 36.5), (50.0, 32.5)], width_units=1.6, color=DARK)
draw_round_polyline([(44.6, 32.0), (47.5, 31.2), (50.0, 32.8)], width_units=1.5, color=DARK)
draw_round_polyline([(55.4, 32.0), (52.5, 31.2), (50.0, 32.8)], width_units=1.5, color=DARK)

save()
