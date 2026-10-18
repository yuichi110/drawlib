# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_namespace."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    PASTEL_GREEN,
    WHITE,
    draw_original_k8s_heptagon,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# White inner workspace card
rectangle(
    (50.0, 48.0),
    width=46.0,
    height=36.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=6.0),
)

# Four dark corner L-brackets framing the isolated namespace scope
brackets = [
    [(33.0, 54.0), (33.0, 60.0), (39.0, 60.0)],
    [(61.0, 60.0), (67.0, 60.0), (67.0, 54.0)],
    [(33.0, 42.0), (33.0, 36.0), (39.0, 36.0)],
    [(61.0, 36.0), (67.0, 36.0), (67.0, 42.0)],
]
for pts in brackets:
    draw_round_polyline(pts, width_units=2.0, color=DARK)

# Central green scoped resource block
rectangle(
    (50.0, 48.0),
    width=20.0,
    height=12.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=3.0),
)

save()
