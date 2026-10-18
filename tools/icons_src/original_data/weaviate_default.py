# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: weaviate."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = 2.0

# Key X coordinates (symmetric around x=50.0)
x_out_l = 9.0
x_in_l = 31.2
x_mid = 50.0
x_in_r = 68.8
x_out_r = 91.0

# 1. Left & right vertical wing pillars (Colors.Amber2)
left_pillar = [
    (x_out_l, 39.5),
    (x_out_l, 61.5),
    (28.0, 74.8),
    (x_in_l, 73.5),
    (x_in_l, 50.2),
]
right_pillar = [
    (x_out_r, 39.5),
    (x_out_r, 61.5),
    (72.0, 74.8),
    (x_in_r, 73.5),
    (x_in_r, 50.2),
]
polygon(
    left_pillar,
    style=fill_style(Colors.Amber2, shape_r=(2.0, 5.0, 4.0, 2.0, 0.0)),
)
polygon(
    right_pillar,
    style=fill_style(Colors.Amber2, shape_r=(2.0, 5.0, 4.0, 2.0, 0.0)),
)

# 2. Lower central inner chevron fold (Colors.Green4)
inner_chevron = [
    (x_in_l, 37.8),
    (x_mid, 47.5),
    (x_in_r, 37.8),
    (x_in_r, 26.2),
    (67.5, 25.2),
    (x_mid, 35.8),
    (32.5, 25.2),
    (x_in_l, 26.2),
]
polygon(
    inner_chevron,
    style=fill_style(
        Colors.Green4,
        shape_r=(0.0, 6.0, 0.0, 1.5, 5.5, 5.0, 5.5, 1.5),
    ),
)

# 3. Middle sweeping W-band across the whole crest (Colors.Green3)
middle_band = [
    (x_out_l, 39.5),
    (x_in_l, 50.2),
    (x_mid, 60.2),
    (x_in_r, 50.2),
    (x_out_r, 39.5),
    (67.5, 25.2),
    (x_in_r, 26.2),
    (x_in_r, 37.8),
    (x_mid, 47.5),
    (x_in_l, 37.8),
    (x_in_l, 26.2),
    (32.5, 25.2),
]
polygon(
    middle_band,
    style=fill_style(
        Colors.Green3,
        shape_r=(4.5, 0.0, 7.5, 0.0, 4.5, 5.5, 0.0, 0.0, 6.0, 0.0, 0.0, 5.5),
    ),
)

# 4. Internal origami fold seams
draw_round_polyline(
    [(x_out_l + 1.5, 39.2), (x_in_l, 50.2), (x_mid, 60.2), (x_in_r, 50.2), (x_out_r - 1.5, 39.2)],
    width_units=1.7,
    color=DARK,
    corner_r=6.5,
)
draw_round_polyline(
    [(x_in_l, 37.8), (x_mid, 47.5), (x_in_r, 37.8)],
    width_units=1.7,
    color=DARK,
    corner_r=5.0,
)
draw_round_polyline([(x_in_l, 50.2), (x_in_l, 26.8)], width_units=1.7, color=DARK)
draw_round_polyline([(x_in_r, 50.2), (x_in_r, 26.8)], width_units=1.7, color=DARK)

# 5. Full outer W silhouette border
outer_w = [
    (x_out_l, 61.5),
    (28.0, 74.8),
    (x_in_l, 73.5),
    (x_in_l, 50.2),
    (x_mid, 60.2),
    (x_in_r, 50.2),
    (x_in_r, 73.5),
    (72.0, 74.8),
    (x_out_r, 61.5),
    (x_out_r, 39.5),
    (67.5, 25.2),
    (x_mid, 35.8),
    (32.5, 25.2),
    (x_out_l, 39.5),
]
polygon(
    outer_w,
    style=fill_style(
        (0, 0, 0, 0),
        border_color=DARK,
        border_units=w,
        shape_r=(5.0, 4.0, 2.0, 0.0, 7.5, 0.0, 2.0, 4.0, 5.0, 4.5, 5.5, 5.0, 5.5, 4.5),
    ),
)

save()
