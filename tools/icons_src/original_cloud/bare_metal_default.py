# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: bare_metal."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Vertical physical rack rails
for x_rail in (22.0, 78.0):
    Icon.draw_round_segment((x_rail, 13.0), (x_rail, 87.0), width_units=3.2, color=Icon.DARK)

# 3 stacked horizontal physical rackmount server blades
blades = [
    (74.0, Icon.PASTEL_BLUE),
    (50.0, Icon.WHITE),
    (26.0, Icon.PASTEL_BLUE),
]

for y_blade, bg_col in blades:
    rectangle(
        (50.0, y_blade),
        width=74.0,
        height=18.0,
        style=Icon.fill_style(bg_col, border_color=Icon.DARK, border_units=w, shape_r=4.0),
    )
    Icon.draw_round_segment((22.0, y_blade), (36.0, y_blade), width_units=2.0, color=Icon.DARK)
    Icon.draw_round_segment((43.0, y_blade), (57.0, y_blade), width_units=2.0, color=Icon.DARK)
    circle(
        (76.0, y_blade),
        radius=3.4,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
    )

save()
