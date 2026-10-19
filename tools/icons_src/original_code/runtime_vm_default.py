# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: runtime_vm."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

b = 2.0

# Outer PASTEL_BLUE engine/VM frame
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=66.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=b, shape_r=6.0),
)

# Top VM header status dots
for x_dot, col in ((23.0, Icon.PASTEL_GREEN), (31.0, Icon.WHITE)):
    circle(
        (x_dot, 76.5),
        radius=2.4,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=b),
    )

# Inner WHITE execution area
rectangle(
    (50.0, 47.0),
    width=62.0,
    height=46.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=b, shape_r=3.0),
)

# 3 stacked horizontal bytecode instruction bars
bars = [
    (55.0, 59.0, 38.0, Icon.PASTEL_GREEN),
    (52.0, 47.0, 32.0, Icon.PASTEL_BLUE_LIGHT),
    (54.0, 35.0, 36.0, Icon.PASTEL_BLUE),
]
for bx, by, bw, col in bars:
    rectangle(
        (bx, by),
        width=bw,
        height=7.5,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=b, shape_r=2.5),
    )

# Left DARK execution pointer triangle pointing at top instruction bar
ptr_pts = [(24.5, 62.5), (24.5, 55.5), (31.5, 59.0)]
polygon(ptr_pts, style=Icon.no_border_fill(Icon.DARK))
Icon.draw_round_polyline(ptr_pts, width_units=b, color=Icon.DARK, closed=True)

save()
