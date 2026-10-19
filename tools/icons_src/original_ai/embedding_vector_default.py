# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: embedding_vector."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

Icon.draw_round_polyline(
    [(30.0, 78.0), (16.0, 78.0), (16.0, 22.0), (30.0, 22.0)],
    corner_r=4.0,
    width_units=w,
    color=Icon.DARK,
)
Icon.draw_round_polyline(
    [(70.0, 78.0), (84.0, 78.0), (84.0, 22.0), (70.0, 22.0)],
    corner_r=4.0,
    width_units=w,
    color=Icon.DARK,
)

for y_pos, fill_col in (
    (68.0, Icon.PASTEL_BLUE),
    (50.0, Icon.PASTEL_GREEN),
    (32.0, Icon.PASTEL_BLUE),
):
    rectangle(
        (50.0, y_pos),
        width=36.0,
        height=11.0,
        style=Icon.fill_style(fill_col, border_color=Icon.DARK, border_units=2.0, shape_r=5.5),
    )

save()
