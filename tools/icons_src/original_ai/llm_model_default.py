# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: llm_model."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
pin_coords = [32.0, 50.0, 68.0]

for pos in pin_coords:
    Icon.draw_round_segment((12.0, pos), (22.0, pos), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((78.0, pos), (88.0, pos), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((pos, 12.0), (pos, 22.0), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((pos, 78.0), (pos, 88.0), width_units=w, color=Icon.DARK)

rectangle(
    (50.0, 50.0),
    width=58.0,
    height=58.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=9.0),
)

sparkle_pts = Icon.build_sparkle_4pt_polygon(50.0, 50.0, outer_r=20.0, inner_r=6.8)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(sparkle_pts, width_units=2.0, color=Icon.DARK, closed=True)

circle(
    (68.0, 68.0),
    radius=4.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
