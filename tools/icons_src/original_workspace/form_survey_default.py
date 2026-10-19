# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: form_survey."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Top clipboard clip back loop
rectangle(
    (50.0, 84.5),
    width=14.0,
    height=6.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)

# 2. Main WHITE clipboard sheet (x=18.0..82.0, y=13.5..80.5)
rectangle(
    (50.0, 47.0),
    width=64.0,
    height=67.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=5.5),
)

# 3. Top PASTEL_BLUE clipboard clip plate
rectangle(
    (50.0, 79.5),
    width=32.0,
    height=8.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.8),
)

# 4. Three survey checklist rows (PASTEL_GREEN checked box + DARK lines)
for y_row in (61.5, 45.0, 28.5):
    rectangle(
        (31.5, y_row),
        width=11.0,
        height=11.0,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=2.2),
    )
    Icon.draw_round_polyline(
        [(28.7, y_row - 0.1), (30.8, y_row - 2.3), (34.6, y_row + 2.2)],
        width_units=w_inner,
        color=Icon.DARK,
    )
    Icon.draw_round_segment((43.0, y_row + 2.2), (71.5, y_row + 2.2), width_units=w_outer, color=Icon.DARK)
    Icon.draw_round_segment((43.0, y_row - 2.6), (61.5, y_row - 2.6), width_units=w_inner, color=Icon.DARK)

save()
