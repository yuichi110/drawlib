# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: vm_snapshot."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Rounded square VM container card (matching virtual_machine_default.py)
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

# Overlapping bottom-right snapshot clock badge
circle(
    (70.0, 28.0),
    radius=16.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle(
    (70.0, 28.0),
    radius=11.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
Icon.draw_round_polyline(
    [(70.0, 34.0), (70.0, 28.0), (75.0, 28.0)],
    width_units=2.0,
    color=Icon.DARK,
)
circle((70.0, 28.0), radius=1.5, style=Icon.fill_style(Icon.DARK))

save()
