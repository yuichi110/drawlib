# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: projector."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Projected PASTEL_GREEN light beam cone
beam_pts = [
    (66.0, 55.0),
    (87.0, 71.0),
    (87.0, 25.0),
    (66.0, 41.0),
]
polygon(beam_pts, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(beam_pts, width_units=2.0, color=Icon.DARK, corner_r=2.0, closed=True)

# Protruding PASTEL_BLUE lens barrel
rectangle(
    (61.5, 48.0),
    width=12.0,
    height=22.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=3.0),
)

# Rubber feet under chassis
for fx in (23.0, 49.0):
    rectangle(
        (fx, 30.0),
        width=9.0,
        height=6.5,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
    )

# Main WHITE projector chassis
rectangle(
    (36.0, 48.0),
    width=46.0,
    height=32.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)

# Cooling louvers and adjustment dial on chassis
for vx in (23.5, 29.0, 34.5):
    Icon.draw_round_segment((vx, 41.0), (vx, 55.0), width_units=2.0, color=Icon.DARK)

circle(
    (48.5, 48.0),
    radius=4.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0),
)

save()
