# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: flux."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Top isometric diamond badge (y=50..90)
top_diamond = [
    (50.0, 90.0),
    (83.0, 70.0),
    (50.0, 50.0),
    (17.0, 70.0),
]
polygon(
    top_diamond,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)

# 3 diagonal wave bars in lower diamond footprint (y=10..46)
# Bar 1 (upper diagonal wave)
bar1 = [
    (36.0, 41.5),
    (43.0, 45.8),
    (77.5, 25.0),
    (70.5, 20.7),
]
polygon(bar1, style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=1.8))

# Bar 2 (middle diagonal wave)
bar2 = [
    (25.5, 35.0),
    (32.5, 39.3),
    (67.0, 18.5),
    (60.0, 14.2),
]
polygon(bar2, style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=1.8))

# Bar 3 (lower-left diagonal wave)
bar3 = [
    (17.0, 29.8),
    (22.5, 33.2),
    (54.5, 13.8),
    (49.0, 10.5),
]
polygon(bar3, style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0, shape_r=1.8))

# Central upward deployment arrow rising from lower diamond into top diamond
arrow_pts = [
    (46.0, 25.0),
    (54.0, 25.0),
    (54.0, 64.0),
    (61.5, 64.0),
    (50.0, 80.5),
    (38.5, 64.0),
    (46.0, 64.0),
]
polygon(arrow_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(arrow_pts, width_units=2.0, color=DARK, closed=True)

save()
