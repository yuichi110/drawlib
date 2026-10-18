# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: honeypot."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cap,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w_shape = 2.0
w_line = 2.0


def build_flat_hex(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    """Build flat-top hexagon vertices centered at (cx, cy) with circumradius r."""
    return [
        (
            cx + r * math.cos(math.radians(60.0 * k)),
            cy + r * math.sin(math.radians(60.0 * k)),
        )
        for k in range(6)
    ]


# 3-cell honeycomb cluster (flat-top hexagons, r=15.32 so shared edges coincide at dy=26.5, dx=23.0)
cells = [
    (38.0, 60.0, PASTEL_BLUE),
    (38.0, 33.5, PASTEL_BLUE_LIGHT),
    (61.0, 46.75, PASTEL_GREEN),
]
cell_polys = [(build_flat_hex(hx, hy, 15.32), hcol) for hx, hy, hcol in cells]
for pts, hcol in cell_polys:
    polygon(pts, style=no_border_fill(hcol))
for pts, _ in cell_polys:
    draw_round_polyline(pts, width_units=w_shape, color=DARK, closed=True)

# WHITE inner hexagon inside the PASTEL_GREEN decoy cell
inner_pts = build_flat_hex(61.0, 46.75, 7.0)
polygon(inner_pts, style=no_border_fill(WHITE))
draw_round_polyline(inner_pts, width_units=w_shape, color=DARK, closed=True)

# 2 concentric DARK radar trap wave arcs radiating on the right side of the decoy cell
cx_w, cy_w = 59.5, 46.75
for r_wave in (23.0, 30.0):
    arc(
        (cx_w, cy_w),
        width=r_wave * 2.0,
        height=r_wave * 2.0,
        angle_start=-50.0,
        angle_end=50.0,
        style=stroke_style(DARK, width_units=w_line),
    )
    for deg in (-50.0, 50.0):
        rad = math.radians(deg)
        draw_cap(
            (cx_w + r_wave * math.cos(rad), cy_w + r_wave * math.sin(rad)),
            width_units=w_line,
            color=DARK,
        )

save()
