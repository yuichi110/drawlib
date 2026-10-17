# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: flutter."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_border = 1.6

top_bar = [(17.69, 49.87), (57.69, 90.0), (82.31, 90.0), (30.06, 37.75)]
mid_top_arm = [(48.5, 43.81), (57.69, 53.06), (82.31, 53.06), (61.0, 31.32)]
mid_diamond = [(61.0, 31.32), (48.5, 43.81), (36.37, 31.56), (48.5, 19.32)]
bot_leg = [(82.31, 10.0), (61.0, 31.32), (48.5, 19.32), (57.69, 10.0)]
# fmt: on

# 1. Flat pastel light/medium/deep blue Flutter 'F' chevron facets
facets = [
    (top_bar, "#72C8F8"),
    (mid_top_arm, "#72C8F8"),
    (mid_diamond, "#4FA3E3"),
    (bot_leg, "#3A78B8"),
]
for pts, color in facets:
    polygon(pts, style=no_border_fill(color))

# 2. Crisp DARK facet and outer outlines
for pts, _ in facets:
    draw_round_polyline(pts, width_units=w_border, color=DARK, closed=True)

save()
