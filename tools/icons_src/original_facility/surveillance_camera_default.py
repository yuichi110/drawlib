# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: surveillance_camera."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Left wall mount plate (PASTEL_BLUE, x=12..19, y=24..58)
rectangle(
    (15.5, 41.0),
    width=7.0,
    height=34.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)
for sy in (30.0, 52.0):
    circle((15.5, sy), radius=1.2, style=Icon.fill_style(Icon.DARK))

# 2. Articulated mount arm (PASTEL_BLUE_LIGHT) + pivot joint (PASTEL_BLUE)
arm_pts = [
    (19.0, 38.0),
    (36.0, 38.0),
    (43.0, 52.0),
    (37.0, 54.0),
    (32.0, 44.0),
    (19.0, 44.0),
]
polygon(arm_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(arm_pts, width_units=w_outer, color=Icon.DARK, closed=True)

circle(
    (40.0, 52.0),
    radius=5.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer),
)
circle((40.0, 52.0), radius=1.8, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.2))

# 3. Bullet camera housing tilted at -18 degrees around (55.0, 64.0)
cx, cy = 55.0, 64.0
ang_deg = -18.0
rad = math.radians(ang_deg)
ux, uy = math.cos(rad), math.sin(rad)
nx, ny = -uy, ux


def _rot(s: float, n: float) -> tuple[float, float]:
    return (cx + s * ux + n * nx, cy + s * uy + n * ny)


# Rear cable gland cap (PASTEL_BLUE_LIGHT)
rear_cap = [_rot(-24.0, -5.0), _rot(-19.0, -5.0), _rot(-19.0, 5.0), _rot(-24.0, 5.0)]
polygon(rear_cap, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(rear_cap, width_units=w_outer, color=Icon.DARK, closed=True)

# Main camera barrel (WHITE, s=-20..+18, n=-11..+11)
body_pts = [
    _rot(-20.0, -11.0),
    _rot(18.0, -11.0),
    _rot(18.0, 11.0),
    _rot(-20.0, 11.0),
]
polygon(body_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(body_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# Side detail groove & status dot on WHITE camera barrel
Icon.draw_round_segment(_rot(-13.0, -3.0), _rot(8.0, -3.0), width_units=w_inner, color=Icon.DARK)
circle(_rot(-14.0, 4.0), radius=1.8, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.3))

# 4. Front 3/4 elliptical PASTEL_GREEN lens ring + inner dark-blue lens
lens_xy = _rot(18.0, 0.0)
ellipse(
    lens_xy,
    width=13.0,
    height=22.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, angle=ang_deg),
)
ellipse(
    lens_xy,
    width=7.0,
    height=12.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_inner, angle=ang_deg),
)
circle(
    _rot(17.2, 2.5),
    radius=1.4,
    style=Icon.fill_style(Icon.WHITE),
)

# 5. Top weather sun-hood (PASTEL_BLUE, overhanging front lens)
hood_pts = [
    _rot(-21.0, 11.0),
    _rot(23.5, 11.0),
    _rot(20.5, 16.5),
    _rot(-21.0, 16.5),
]
polygon(hood_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(hood_pts, width_units=w_outer, color=Icon.DARK, closed=True)

save()
