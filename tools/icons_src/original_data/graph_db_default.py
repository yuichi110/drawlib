# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: graph_db."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
nodes = [
    (50.0, 50.0, 12.0, Icon.PASTEL_BLUE),
    (24.0, 74.0, 8.5, Icon.PASTEL_GREEN),
    (78.0, 72.0, 8.5, Icon.PASTEL_BLUE_LIGHT),
    (22.0, 26.0, 8.5, Icon.PASTEL_BLUE_LIGHT),
    (76.0, 24.0, 8.5, Icon.PASTEL_GREEN),
]
edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 4)]
for i, j in edges:
    Icon.draw_round_segment(
        (nodes[i][0], nodes[i][1]), (nodes[j][0], nodes[j][1]), width_units=w * 1.2, color=Icon.DARK
    )
for x, y, r, col in nodes:
    circle((x, y), radius=r, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w))
    circle((x, y), radius=r * 0.35, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
save()
