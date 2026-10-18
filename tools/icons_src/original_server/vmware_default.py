# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server vendor icon: vmware (default variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0


def _rounded_rect_ring(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    r: float,
    *,
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Build a counter-clockwise rounded rectangle ring in 100x100 coords."""
    pts: list[tuple[float, float]] = []
    corners = [
        (x1 - r, y0 + r, -90.0),
        (x1 - r, y1 - r, 0.0),
        (x0 + r, y1 - r, 90.0),
        (x0 + r, y0 + r, 180.0),
    ]
    for cx, cy, start_deg in corners:
        for i in range(steps + 1):
            ang = math.radians(start_deg + 90.0 * (i / steps))
            pts.append((round(cx + r * math.cos(ang), 2), round(cy + r * math.sin(ang), 2)))
    return pts


def _draw_frame(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    band: float,
    r_out: float,
    r_in: float,
    color: object,
) -> None:
    """Draw a hollow rounded-square frame with transparent interior hole."""
    outer = _rounded_rect_ring(x0, y0, x1, y1, r_out)
    inner = _rounded_rect_ring(x0 + band, y0 + band, x1 - band, y1 - band, r_in)
    draw_compound_polygon([outer, inner], color=color)
    draw_round_polyline(outer, width_units=w, color=DARK, closed=True)
    draw_round_polyline(inner, width_units=w, color=DARK, closed=True)


band_w = 3.8
r_outer = 5.9
r_inner = 2.4

frame1_color = "#94A3B8"
frame2_color = "#A8B5C4"
frame3_color = "#BAC6D4"

# 1. Bottom-left frame (slate-gray 1)
_draw_frame(9.0, 10.33, 64.79, 64.32, band_w, r_outer, r_inner, frame1_color)

# 2. Top-center frame (slate-gray 2)
_draw_frame(22.15, 35.68, 77.85, 89.67, band_w, r_outer, r_inner, frame2_color)

# 3. Middle-right frame (slate-gray 3)
_draw_frame(35.21, 23.04, 91.0, 76.96, band_w, r_outer, r_inner, frame3_color)

# 4. Over-under interlocking weave bridges
# Frame 1 top bar over Frame 2 left bar
polygon(
    [(20.8, 64.32 - band_w), (27.4, 64.32 - band_w), (27.4, 64.32), (20.8, 64.32)],
    style=no_border_fill(frame1_color),
)
draw_round_segment((20.8, 64.32), (27.4, 64.32), width_units=w, color=DARK)
draw_round_segment((20.8, 64.32 - band_w), (27.4, 64.32 - band_w), width_units=w, color=DARK)

# Frame 1 right bar over Frame 3 bottom bar
polygon(
    [(64.79 - band_w, 21.6), (64.79, 21.6), (64.79, 28.2), (64.79 - band_w, 28.2)],
    style=no_border_fill(frame1_color),
)
draw_round_segment((64.79 - band_w, 21.6), (64.79 - band_w, 28.2), width_units=w, color=DARK)
draw_round_segment((64.79, 21.6), (64.79, 28.2), width_units=w, color=DARK)

# Frame 2 right bar over Frame 3 top bar
polygon(
    [(77.85 - band_w, 71.8), (77.85, 71.8), (77.85, 78.4), (77.85 - band_w, 78.4)],
    style=no_border_fill(frame2_color),
)
draw_round_segment((77.85 - band_w, 71.8), (77.85 - band_w, 78.4), width_units=w, color=DARK)
draw_round_segment((77.85, 71.8), (77.85, 78.4), width_units=w, color=DARK)

save()
