# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: semiconductor_fab."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.5
w_grid = 1.3

# 1. Rooftop cleanroom HEPA air-handling unit (x=15..55, y=67..81)
rectangle(
    (35.0, 74.0),
    width=40.0,
    height=14.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=2.0),
)
for lx in (23.0, 35.0, 47.0):
    rectangle(
        (lx, 74.0),
        width=8.0,
        height=7.0,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_inner, shape_r=1.0),
    )

# Secondary rooftop exhaust stack (x=61..73, y=67..78)
rectangle(
    (67.0, 72.5),
    width=12.0,
    height=11.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.5),
)
rectangle(
    (67.0, 79.0),
    width=15.0,
    height=4.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.2),
)

# 2. Main cleanroom fab building wall (WHITE, x=11..81, y=16..63)
rectangle(
    (46.0, 39.5),
    width=70.0,
    height=47.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer),
)

# 3. Flat cleanroom roof fascia band (PASTEL_BLUE, x=9..83, y=62..68)
rectangle(
    (46.0, 65.0),
    width=74.0,
    height=6.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.5),
)

# 4. Left cleanroom viewing window band & airlock entrance
rectangle(
    (30.0, 49.0),
    width=26.0,
    height=12.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.5),
)
draw_round_segment((25.6, 43.0), (25.6, 55.0), width_units=w_inner, color=DARK)
draw_round_segment((34.4, 43.0), (34.4, 55.0), width_units=w_inner, color=DARK)

# Airlock double door (x=18..34, y=16..36)
rectangle(
    (26.0, 26.0),
    width=16.0,
    height=20.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.2),
)
draw_round_segment((26.0, 16.0), (26.0, 36.0), width_units=w_inner, color=DARK)
circle((22.2, 28.5), radius=1.8, style=fill_style(WHITE, border_color=DARK, border_units=1.2))
circle((29.8, 28.5), radius=1.8, style=fill_style(WHITE, border_color=DARK, border_units=1.2))

# 5. Foundation ground plinth (x=8..84, y=12.5..16.5)
rectangle(
    (46.0, 14.5),
    width=76.0,
    height=4.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.5),
)

# 6. Foreground silicon wafer with die grid at (68.0, 35.0)
wx, wy = 68.0, 35.0
r_wafer = 21.0
notch_deg = 22.0  # Flat orientation flat at the bottom (around 270 deg)
wafer_pts: list[tuple[float, float]] = []
steps = 64
start_deg = 270.0 + notch_deg
end_deg = 270.0 + 360.0 - notch_deg
for i in range(steps + 1):
    deg = start_deg + (end_deg - start_deg) * (i / steps)
    ang = math.radians(deg)
    wafer_pts.append((wx + r_wafer * math.cos(ang), wy + r_wafer * math.sin(ang)))

polygon(wafer_pts, style=no_border_fill(PASTEL_GREEN))

# Highlighted silicon dies inside the wafer grid
cell = 7.4
highlighted_dies = [
    (-1, 1, WHITE),
    (0, 0, WHITE),
    (1, 1, PASTEL_BLUE_LIGHT),
    (-1, -1, PASTEL_BLUE_LIGHT),
    (0, -2, WHITE),
]
for gx_idx, gy_idx, die_col in highlighted_dies:
    dx0 = wx + gx_idx * cell
    dy0 = wy + gy_idx * cell
    rectangle(
        (dx0 + cell / 2.0, dy0 + cell / 2.0),
        width=cell,
        height=cell,
        style=no_border_fill(die_col),
    )

# Grid lines clipped neatly to wafer contour
r_clip = r_wafer - 0.8
y_flat = wy + r_wafer * math.sin(math.radians(start_deg)) + 0.5
for k in (-2, -1, 0, 1, 2):
    offset = k * cell
    # Vertical grid line at x = wx + offset
    if abs(offset) < r_clip:
        half_span = math.sqrt(r_clip * r_clip - offset * offset)
        y_bot = max(y_flat, wy - half_span)
        y_top = wy + half_span
        if y_top > y_bot:
            draw_round_segment((wx + offset, y_bot), (wx + offset, y_top), width_units=w_grid, color=DARK)
    # Horizontal grid line at y = wy + offset
    if wy + offset > y_flat and abs(offset) < r_clip:
        half_span = math.sqrt(r_clip * r_clip - offset * offset)
        draw_round_segment((wx - half_span, wy + offset), (wx + half_span, wy + offset), width_units=w_grid, color=DARK)

# Outer wafer contour
draw_round_polyline(wafer_pts, width_units=w_outer, color=DARK, closed=True)

save()
