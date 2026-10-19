# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: gpu_node."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

pin_coords = [32.0, 50.0, 68.0]
w = Icon.ORIG_STROKE

for pos in pin_coords:
    Icon.draw_round_segment((11.0, pos), (24.0, pos), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((76.0, pos), (89.0, pos), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((pos, 11.0), (pos, 24.0), width_units=w, color=Icon.DARK)
    Icon.draw_round_segment((pos, 76.0), (pos, 89.0), width_units=w, color=Icon.DARK)

rectangle(
    (50.0, 50.0),
    width=56.0,
    height=56.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

cores = [
    (40.0, 60.0, Icon.PASTEL_BLUE),
    (60.0, 60.0, Icon.PASTEL_BLUE),
    (40.0, 40.0, Icon.PASTEL_BLUE),
    (60.0, 40.0, Icon.PASTEL_GREEN),
]
for cx, cy, col in cores:
    rectangle(
        (cx, cy),
        width=16.0,
        height=16.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=2.0, shape_r=3.0),
    )

save()
