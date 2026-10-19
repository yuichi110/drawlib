# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: airflow."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
cx, cy = 50.0, 50.0


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
        pts.append(
            (
                (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


def _rot(pt: tuple[float, float], deg: float) -> tuple[float, float]:
    """Rotate point (x, y) around (50, 50) by deg degrees counter-clockwise."""
    rad = math.radians(deg)
    ca, sa = math.cos(rad), math.sin(rad)
    dx, dy = pt[0] - cx, pt[1] - cy
    return (cx + dx * ca - dy * sa, cy + dx * sa + dy * ca)


def _rot_list(pts: list[tuple[float, float]], deg: float) -> list[tuple[float, float]]:
    return [_rot(p, deg) for p in pts]


# Base Top-Left pinwheel blade (before 0 / 90 / 180 / 270 deg CCW rotation):
# - Leading straight edge: center (50, 50) -> Top-Left tip (12.5, 87.5)
# - Outer curved edge: (12.5, 87.5) -> fold split (52.5, 81.0) -> elbow (69.5, 69.5)
#   Notice (69.5, 69.5) lies directly on the next blade's 45-deg leading edge!
p_center = (50.0, 50.0)
p_tip = (12.5, 87.5)
p_split = (52.5, 81.0)
p_elbow = (69.5, 69.5)

# Main outer sail facet (center -> tip -> split -> curved crease back to center)
base_sail: list[tuple[float, float]] = [
    p_center,
    p_tip,
    *_cubic(p_tip, (28.0, 87.5), (43.0, 85.5), p_split, 18),
    *_cubic(p_split, (56.5, 72.0), (54.5, 60.5), p_center, 16),
]

# Inner folded triangle pocket (center -> curved crease to split -> outer fold to elbow -> straight edge to center)
base_flap: list[tuple[float, float]] = [
    p_center,
    *_cubic(p_center, (54.5, 60.5), (56.5, 72.0), p_split, 16),
    *_cubic(p_split, (59.5, 78.0), (65.5, 73.5), p_elbow, 12),
]

blade_styles = [
    (0.0, Colors.Red3, Colors.Red2),
    (270.0, Colors.Green3, Colors.Green2),
    (180.0, Colors.Blue3, Colors.Blue2),
    (90.0, Colors.Teal3, Colors.Teal2),
]

# 1. Fill all 4 blade sails and inner fold pockets
for deg, col_sail, col_flap in blade_styles:
    polygon(_rot_list(base_sail, deg), style=Icon.no_border_fill(col_sail))
    polygon(_rot_list(base_flap, deg), style=Icon.no_border_fill(col_flap))

# 2. Draw crisp inner fold creases and outer blade borders
for deg, _, _ in blade_styles:
    Icon.draw_round_polyline(_rot_list(base_flap, deg), width_units=1.6, color=Icon.DARK, closed=True)

for deg, _, _ in blade_styles:
    Icon.draw_round_polyline(_rot_list(base_sail, deg), width_units=w, color=Icon.DARK, closed=True)

# 3. Central pinwheel hub
circle(
    (cx, cy),
    radius=4.0,
    style=Icon.fill_style(Icon.DARK),
)
circle(
    (cx, cy),
    radius=1.4,
    style=Icon.fill_style(Icon.WHITE),
)

save()
