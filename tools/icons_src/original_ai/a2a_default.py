# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: a2a."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = 2.0
cx, cy = 50.0, 50.0


def _circle_pts(xc: float, yc: float, r: float, steps: int = 72) -> list[tuple[float, float]]:
    """Sample a circle polygon."""
    return [
        (xc + r * math.cos(2.0 * math.pi * i / steps), yc + r * math.sin(2.0 * math.pi * i / steps))
        for i in range(steps)
    ]


def _draw_a_glyph(gx: float, gy: float) -> None:
    """Draw a clean rounded-cap vector 'A' glyph in WHITE centered at (gx, gy)."""
    legs = [
        (gx - 6.6, gy - 6.8),
        (gx, gy + 7.6),
        (gx + 6.6, gy - 6.8),
    ]
    draw_round_polyline(legs, width_units=2.8, color=WHITE)
    draw_round_segment(
        (gx - 4.3, gy - 2.0),
        (gx + 4.3, gy - 2.0),
        width_units=2.0,
        color=WHITE,
    )


def _draw_2_glyph(gx: float, gy: float) -> None:
    """Draw a clean rounded-cap vector '2' glyph in WHITE centered at (gx, gy)."""
    pts: list[tuple[float, float]] = []
    # Top arch from 165 deg clockwise to -30 deg
    arc_cx, arc_cy = gx + 0.2, gy + 3.2
    rx, ry = 5.8, 4.6
    steps = 16
    for i in range(steps + 1):
        ang = math.radians(165.0 - 195.0 * (i / steps))
        pts.append((arc_cx + rx * math.cos(ang), arc_cy + ry * math.sin(ang)))
    # Smooth diagonal sweep down-left and horizontal base
    pts.extend(
        [
            (gx + 3.2, gy - 0.6),
            (gx - 2.5, gy - 4.5),
            (gx - 6.0, gy - 7.8),
            (gx + 6.4, gy - 7.8),
        ]
    )
    draw_round_polyline(pts, width_units=2.9, color=WHITE, corner_r=1.8)


# 1. Central orbital circle ring (Colors.Blue3 band with transparent inner hole)
outer_orbit = _circle_pts(cx, cy, 34.8)
inner_orbit = _circle_pts(cx, cy, 30.8)

draw_compound_polygon([outer_orbit, inner_orbit], color=Colors.Blue3)
draw_round_polyline(outer_orbit, width_units=w, color=DARK, closed=True)
draw_round_polyline(inner_orbit, width_units=1.7, color=DARK, closed=True)

# 2. Three circular node badges (top-left 'A', center '2', bottom-right 'A')
tl_xy = (25.5, 74.5)
br_xy = (74.5, 25.5)

circle(
    tl_xy,
    radius=14.6,
    style=fill_style(Colors.Blue3, border_color=DARK, border_units=w),
)
circle(
    (cx, cy),
    radius=15.4,
    style=fill_style(Colors.Blue3, border_color=DARK, border_units=w),
)
circle(
    br_xy,
    radius=14.6,
    style=fill_style(Colors.Blue3, border_color=DARK, border_units=w),
)

# 3. Clean polygon/polyline vector glyphs in WHITE
_draw_a_glyph(*tl_xy)
_draw_2_glyph(cx, cy)
_draw_a_glyph(*br_xy)

save()
