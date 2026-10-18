# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: cassandra."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = 2.0
cx, cy = 50.0, 50.0


def _cubic_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 28,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


def _quad_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Sample quadratic Bezier curve including p0."""
    pts: list[tuple[float, float]] = [p0]
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append((
            (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0],
            (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1],
        ))
    return pts


# 1. Almond eye contour (left tear duct at (11, 47) -> arched top lid -> right corner (89, 51) -> bottom lid)
p_left = (11.0, 47.0)
p_right = (89.0, 51.0)

upper_lid = _cubic_bezier(p_left, (29.0, 76.0), (68.0, 77.0), p_right, 28)
lower_lid = _cubic_bezier(p_right, (68.0, 24.0), (31.0, 25.0), p_left, 28)
eye_pts = [p_left, *upper_lid, *lower_lid]

# Sclera background (Colors.Teal3 outer eyelid ring + WHITE inner sclera)
polygon(eye_pts, style=no_border_fill(Colors.Teal3))

inner_upper = _cubic_bezier((16.5, 47.5), (32.0, 70.0), (65.0, 71.0), (83.0, 50.5), 24)
inner_lower = _cubic_bezier((83.0, 50.5), (65.0, 29.0), (33.0, 29.5), (16.5, 47.5), 24)
polygon([(16.5, 47.5), *inner_upper, *inner_lower], style=no_border_fill(WHITE))

# 2. Central circular iris (Colors.Blue3)
r_iris = 18.8
circle(
    (cx, cy),
    radius=r_iris,
    style=fill_style(Colors.Blue3, border_color=DARK, border_units=1.8),
)

# 3. Signature Cassandra orbital arc + nodes inside the iris
arc(
    (cx + 2.0, cy - 1.0),
    width=27.5,
    height=27.5,
    angle_start=110.0,
    angle_end=265.0,
    style=stroke_style(WHITE, width_units=1.6),
)
arc(
    (cx - 2.0, cy + 1.5),
    width=25.5,
    height=25.5,
    angle_start=-65.0,
    angle_end=55.0,
    style=stroke_style(WHITE, width_units=1.6),
)

# 4. Inner iris ring (Colors.Teal4) + dark pupil (DARK) + crisp white catchlight
circle(
    (cx, cy),
    radius=9.8,
    style=fill_style(Colors.Teal4, border_color=DARK, border_units=1.7),
)
circle(
    (cx, cy),
    radius=4.6,
    style=fill_style(DARK),
)
circle(
    (cx - 3.6, cy + 3.9),
    radius=2.2,
    style=fill_style(WHITE),
)

# Small white orbital nodes on the iris ring
for deg_node in (135.0, 215.0, 15.0):
    rad_n = math.radians(deg_node)
    circle(
        (cx + 13.4 * math.cos(rad_n), cy + 13.4 * math.sin(rad_n)),
        radius=2.2,
        style=fill_style(WHITE, border_color=DARK, border_units=1.3),
    )

# 5. Outer eye border + gracefully curved eyelashes (3 upper-right, 3 lower)
draw_round_polyline(eye_pts, width_units=w, color=DARK, closed=True)

# Sweeping curved upper-right eyelashes
upper_lashes = [
    ((60.0, 69.2), (65.0, 74.5), (71.5, 78.5)),
    ((71.5, 65.5), (77.5, 70.0), (84.0, 73.5)),
    ((81.0, 59.0), (86.0, 62.0), (91.0, 64.5)),
]
for p0, p1, p2 in upper_lashes:
    draw_round_polyline(_quad_bezier(p0, p1, p2, 10), width_units=1.8, color=DARK)

# Sweeping curved lower eyelashes
lower_lashes = [
    ((45.0, 30.8), (44.0, 25.0), (41.5, 20.5)),
    ((58.5, 31.5), (59.5, 25.5), (62.0, 20.5)),
    ((71.0, 35.8), (74.5, 30.5), (78.5, 26.5)),
]
for p0, p1, p2 in lower_lashes:
    draw_round_polyline(_quad_bezier(p0, p1, p2, 10), width_units=1.8, color=DARK)

save()
