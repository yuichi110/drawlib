# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: message_broker."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
targets = [(82.0, 76.0, Icon.PASTEL_GREEN), (84.0, 50.0, Icon.PASTEL_BLUE_LIGHT), (82.0, 24.0, Icon.PASTEL_GREEN)]
for tx, ty, col in targets:
    Icon.draw_round_segment((42.0, 50.0), (tx, ty), width_units=w * 1.2, color=Icon.DARK)
    circle((tx, ty), radius=8.5, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w))
# Broker hub with message queue slots
rectangle(
    (34.0, 50.0),
    width=40.0,
    height=52.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)
for yc in (62.0, 50.0, 38.0):
    rectangle(
        (34.0, yc),
        width=26.0,
        height=7.5,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=2.0),
    )
save()
