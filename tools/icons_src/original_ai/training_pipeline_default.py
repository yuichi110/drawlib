# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: training_pipeline."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

left_nodes = [(24.0, 68.0), (24.0, 32.0)]
mid_nodes = [(50.0, 78.0), (50.0, 50.0), (50.0, 22.0)]
right_nodes = [(76.0, 68.0), (76.0, 32.0)]

for p_left in left_nodes:
    for p_mid in mid_nodes:
        Icon.draw_round_segment(p_left, p_mid, width_units=2.0, color=Icon.DARK)

for p_mid in mid_nodes:
    for p_right in right_nodes:
        Icon.draw_round_segment(p_mid, p_right, width_units=2.0, color=Icon.DARK)

for pt in left_nodes:
    circle(
        pt,
        radius=8.5,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
    )

for pt in mid_nodes:
    circle(
        pt,
        radius=9.5,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
    )

for pt in right_nodes:
    circle(
        pt,
        radius=9.5,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
    )

save()
