# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: windows."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w = 2.0
pane_color = "#4A94EA"

panes = [
    ([(11.0, 53.0), (47.0, 53.0), (47.0, 89.0), (11.0, 89.0)], pane_color),
    ([(53.0, 53.0), (89.0, 53.0), (89.0, 89.0), (53.0, 89.0)], pane_color),
    ([(11.0, 11.0), (47.0, 11.0), (47.0, 47.0), (11.0, 47.0)], pane_color),
    ([(53.0, 11.0), (89.0, 11.0), (89.0, 47.0), (53.0, 47.0)], pane_color),
]

for pts, fill_col in panes:
    polygon(pts, style=Icon.no_border_fill(fill_col))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)

save()
