# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: harbor."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)


def _beam_sector(
    origin: tuple[float, float],
    deg_start: float,
    deg_end: float,
    *,
    cx: float = 50.0,
    cy: float = 50.0,
    r: float = 33.0,
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Build a triangular light beam fanning from origin to the circle of radius r."""
    pts: list[tuple[float, float]] = [origin]
    for i in range(steps + 1):
        ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0
r_outer = 40.0
r_inner = 33.0

# Outer circular badge ring
circle(
    (cx, cy),
    radius=r_outer,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (cx, cy),
    radius=r_inner,
    style=fill_style(WHITE),
)

# Two pastel green light beams fanning right from lighthouse lantern
beam_top = _beam_sector((45.0, 58.0), 11.0, 35.0)
beam_bot = _beam_sector((45.0, 56.0), -18.0, 4.0)

for beam in (beam_top, beam_bot):
    polygon(beam, style=no_border_fill(PASTEL_GREEN))
    draw_round_segment(beam[0], beam[1], width_units=2.0, color=DARK)
    draw_round_segment(beam[0], beam[-1], width_units=2.0, color=DARK)

# Lighthouse tower shaft sitting on bottom-left of inner circle
# At x=32, y_circle = 50 - sqrt(33^2 - 18^2) = 50 - 27.66 = 22.34
# At x=46, y_circle = 50 - sqrt(33^2 - 4^2) = 50 - 32.75 = 17.25
tower_pts: list[tuple[float, float]] = [
    (34.5, 50.0),
    (32.5, 23.2),
]
# Follow inner circle arc from x=32.5 to x=45.5
for i in range(1, 12):
    x = 32.5 + (45.5 - 32.5) * (i / 12)
    y = cy - math.sqrt(max(0.0, r_inner * r_inner - (x - cx) ** 2))
    tower_pts.append((x, y))
tower_pts.extend([(45.5, 17.3), (43.5, 50.0)])

polygon(tower_pts, style=no_border_fill(PASTEL_BLUE))

# Two diagonal white stripe accents across lighthouse shaft
stripe1 = [(33.5, 38.0), (44.3, 33.0), (44.1, 36.8), (33.8, 41.8)]
stripe2 = [(32.9, 28.5), (44.9, 23.5), (44.7, 27.3), (33.2, 32.3)]
for sp in (stripe1, stripe2):
    polygon(sp, style=no_border_fill(WHITE))
    draw_round_segment(sp[0], sp[1], width_units=2.0, color=DARK)
    draw_round_segment(sp[3], sp[2], width_units=2.0, color=DARK)

# Lighthouse tower shaft side borders
draw_round_segment((34.5, 50.0), (32.5, 23.2), width_units=2.0, color=DARK)
draw_round_segment((43.5, 50.0), (45.5, 17.3), width_units=2.0, color=DARK)

# Gallery / balcony overhang bar
rectangle(
    (39.0, 52.0),
    width=14.0,
    height=4.2,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=1.2),
)

# Lantern room
rectangle(
    (39.0, 58.2),
    width=9.5,
    height=8.2,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Pointed roof cap
roof_pts = [(32.5, 62.3), (45.5, 62.3), (39.0, 71.5)]
polygon(roof_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(roof_pts, width_units=2.0, color=DARK, closed=True)

# Re-stroke inner circle border cleanly on top of tower base & beam ends
circle((cx, cy), radius=r_inner, style=stroke_style(DARK, width_units=2.0))

save()
