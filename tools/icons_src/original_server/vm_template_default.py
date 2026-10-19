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
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Rounded square VM container card (matching virtual_machine_default.py and vm_snapshot_default.py)
rectangle(
    (46.0, 52.0),
    width=68.0,
    height=68.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=10.0),
)

# Centered 3D isometric VM cube (right face in light blue to contrast with green badge)
Icon.draw_iso_cube(
    46.0,
    52.0,
    radius=21.5,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.PASTEL_BLUE_LIGHT,
    border_color=Icon.DARK,
    border_units=2.0,
)

# Overlapping bottom-right circular badge containing a folded-corner file icon
circle(
    (70.0, 28.0),
    radius=16.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)

file_pts = [
    (63.0, 19.0),
    (77.0, 19.0),
    (77.0, 32.0),
    (72.0, 37.0),
    (63.0, 37.0),
]
polygon(file_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(file_pts, width_units=2.0, color=Icon.DARK, closed=True)

# Top-right folded dog-ear flap inside the file icon
flap_pts = [
    (72.0, 37.0),
    (72.0, 32.0),
    (77.0, 32.0),
]
polygon(flap_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(flap_pts, width_units=1.8, color=Icon.DARK, closed=True)

# Document content lines inside the file icon
Icon.draw_round_segment((66.5, 28.0), (73.5, 28.0), width_units=1.8, color=Icon.DARK)
Icon.draw_round_segment((66.5, 23.8), (72.0, 23.8), width_units=1.8, color=Icon.DARK)

save()
