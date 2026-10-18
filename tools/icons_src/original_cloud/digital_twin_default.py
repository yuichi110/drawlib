# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: digital_twin."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Top and bottom bidirectional sync arrows linking physical cube and digital twin
draw_round_segment((34.0, 75.0), (64.0, 75.0), width_units=2.0, color=DARK)
draw_round_polyline([(59.5, 79.0), (64.5, 75.0), (59.5, 71.0)], width_units=2.0, color=DARK)

draw_round_segment((36.0, 25.0), (66.0, 25.0), width_units=2.0, color=DARK)
draw_round_polyline([(40.5, 29.0), (35.5, 25.0), (40.5, 21.0)], width_units=2.0, color=DARK)

# Vertical dashed symmetry axis at x=50 (y=14..86)
for y0, y1 in ((14.0, 20.0), (31.0, 39.0), (46.0, 54.0), (61.0, 69.0), (80.0, 86.0)):
    draw_round_segment((50.0, y0), (50.0, y1), width_units=w, color=DARK)

# Left physical 3D cube
draw_iso_cube(
    27.0,
    50.0,
    radius=17.0,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=2.0,
)

# Right mirrored digital twin 3D cube
twin_verts = draw_iso_cube(
    73.0,
    50.0,
    radius=17.0,
    top_color=WHITE,
    left_color=PASTEL_BLUE_LIGHT,
    right_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=2.0,
)

# Telemetry vertex nodes on the digital twin cube
for key in ("top", "tr", "br", "bottom"):
    vx, vy = twin_verts[key]
    circle(
        (vx, vy),
        radius=3.0,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

save()
