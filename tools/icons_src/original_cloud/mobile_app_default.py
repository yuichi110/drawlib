# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: mobile_app."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Smartphone outer body
rectangle(
    (50.0, 50.0),
    width=46.0,
    height=76.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Top speaker and bottom home bar
Icon.draw_round_segment((44.0, 80.0), (56.0, 80.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((43.0, 20.0), (57.0, 20.0), width_units=2.0, color=Icon.DARK)

# 2x2 app tile grid
tiles = [
    (41.0, 60.0, Icon.PASTEL_BLUE),
    (59.0, 60.0, Icon.PASTEL_GREEN),
    (41.0, 42.0, Icon.PASTEL_BLUE),
    (59.0, 42.0, Icon.PASTEL_BLUE),
]
for tx, ty, col in tiles:
    rectangle(
        (tx, ty),
        width=12.5,
        height=12.5,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=2.0, shape_r=3.0),
    )

save()
