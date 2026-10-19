# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: data_catalog."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Catalog tabs on right
for yc, col in ((68.0, Icon.PASTEL_GREEN), (52.0, Icon.PASTEL_BLUE_LIGHT), (36.0, Icon.PASTEL_GREEN)):
    rectangle(
        (74.0, yc),
        width=14.0,
        height=11.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w, shape_r=2.5),
    )
# Main catalog book
rectangle(
    (46.0, 52.0),
    width=52.0,
    height=66.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)
rectangle(
    (26.0, 52.0),
    width=10.0,
    height=66.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w, shape_r=3.0),
)
# Magnifying glass on bottom-right
Icon.draw_round_segment((70.0, 32.0), (84.0, 18.0), width_units=w * 2.2, color=Icon.DARK)
circle((62.0, 40.0), radius=15.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
circle((62.0, 40.0), radius=8.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
save()
