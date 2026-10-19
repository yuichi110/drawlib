# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: e_signature."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Contract page (WHITE sheet, x=15.0..71.0, y=14.0..84.0)
rectangle(
    (43.0, 49.0),
    width=56.0,
    height=70.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.5),
)

# 2. Contract top header pill and text lines
rectangle(
    (34.5, 73.0),
    width=23.0,
    height=5.2,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=2.6),
)
for y_line, x_end in ((62.5, 61.5), (54.0, 61.5), (45.5, 49.5)):
    Icon.draw_round_segment((23.0, y_line), (x_end, y_line), width_units=w_inner, color=Icon.DARK)

# 3. PASTEL_GREEN signature ribbon/box at bottom of contract
rectangle(
    (43.0, 27.5),
    width=42.0,
    height=15.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=3.0),
)

# 4. Wavy DARK signature stroke inside signature box
sig_pts = [
    (26.5, 25.0),
    (30.5, 30.8),
    (33.5, 24.5),
    (38.0, 29.8),
    (41.5, 25.0),
    (46.5, 28.0),
    (53.0, 26.0),
]
Icon.draw_round_polyline(sig_pts, width_units=w_inner, color=Icon.DARK, corner_r=1.4)

# 5. Tilted PASTEL_BLUE fountain/stylus pen signing at (53.0, 26.0)
ang = math.radians(45.0)
ux, uy = math.cos(ang), math.sin(ang)
nx, ny = -uy, ux
tx, ty = 53.0, 26.0


def _pen_pt(s: float, d: float) -> tuple[float, float]:
    return (tx + s * ux + d * nx, ty + s * uy + d * ny)


# Nib (WHITE triangle from s=0 to s=9.0, half-width=3.8)
nib_pts = [_pen_pt(0.0, 0.0), _pen_pt(9.0, -3.8), _pen_pt(9.0, 3.8)]
polygon(nib_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(nib_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# Barrel (PASTEL_BLUE from s=9.0 to s=37.0, half-width=3.8)
barrel_pts = [
    _pen_pt(9.0, -3.8),
    _pen_pt(37.0, -3.8),
    _pen_pt(37.0, 3.8),
    _pen_pt(9.0, 3.8),
]
polygon(barrel_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(barrel_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# End cap (PASTEL_BLUE_LIGHT from s=37.0 to s=43.5, half-width=3.8)
cap_pts = [
    _pen_pt(37.0, -3.8),
    _pen_pt(43.5, -3.8),
    _pen_pt(43.5, 3.8),
    _pen_pt(37.0, 3.8),
]
polygon(cap_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(cap_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# Pocket clip along top side of pen barrel
clip_pts = [
    _pen_pt(36.0, 3.8),
    _pen_pt(36.0, 6.4),
    _pen_pt(24.5, 6.4),
]
Icon.draw_round_polyline(clip_pts, width_units=w_inner, color=Icon.DARK, corner_r=1.2)

save()
