# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: vector_db."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
verts = Icon.draw_iso_cube(
    50.0,
    50.0,
    38.0,
    top_color=Icon.PASTEL_BLUE_LIGHT,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.WHITE,
    border_units=w,
)
# Vector arrows and embedding points inside cube space
pts = [(34.0, 58.0, Icon.PASTEL_GREEN), (66.0, 60.0, Icon.PASTEL_GREEN), (54.0, 32.0, Icon.PASTEL_BLUE)]
for px, py, col in pts:
    Icon.draw_round_segment((50.0, 50.0), (px, py), width_units=w * 1.2, color=Icon.DARK)
    circle((px, py), radius=5.5, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w))
circle((50.0, 50.0), radius=6.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
save()
