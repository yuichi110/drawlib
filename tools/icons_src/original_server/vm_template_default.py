# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: vm_template."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Rounded square VM container card (matching virtual_machine_default.py and vm_snapshot_default.py)
rectangle(
    (46.0, 52.0),
    width=68.0,
    height=68.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=10.0),
)

# Centered 3D isometric VM cube (right face in light blue to contrast with green badge)
draw_iso_cube(
    46.0,
    52.0,
    radius=21.5,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=2.4,
)

# Overlapping bottom-right circular badge containing a folded-corner file icon
circle(
    (70.0, 28.0),
    radius=16.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

file_pts = [
    (63.0, 19.0),
    (77.0, 19.0),
    (77.0, 32.0),
    (72.0, 37.0),
    (63.0, 37.0),
]
polygon(file_pts, style=no_border_fill(WHITE))
draw_round_polyline(file_pts, width_units=2.0, color=DARK, closed=True)

# Top-right folded dog-ear flap inside the file icon
flap_pts = [
    (72.0, 37.0),
    (72.0, 32.0),
    (77.0, 32.0),
]
polygon(flap_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(flap_pts, width_units=1.8, color=DARK, closed=True)

# Document content lines inside the file icon
draw_round_segment((66.5, 28.0), (73.5, 28.0), width_units=1.8, color=DARK)
draw_round_segment((66.5, 23.8), (72.0, 23.8), width_units=1.8, color=DARK)

save()
