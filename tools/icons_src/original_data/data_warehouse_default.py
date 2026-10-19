# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: data_warehouse."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Warehouse base and columns
rectangle(
    (50.0, 42.0),
    width=72.0,
    height=48.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=3.0),
)
roof = [(10.0, 66.0), (90.0, 66.0), (50.0, 88.0)]
polygon(roof, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w))
# 2 cylinder stacks inside warehouse
Icon.draw_cylinder_tier(
    36.0, 24.0, 22.0, 28.0, 4.5, body_color=Icon.PASTEL_BLUE_LIGHT, top_color=Icon.WHITE, border_units=w
)
Icon.draw_cylinder_tier(64.0, 24.0, 22.0, 28.0, 4.5, body_color=Icon.PASTEL_GREEN, top_color=Icon.WHITE, border_units=w)
rectangle(
    (50.0, 15.0),
    width=80.0,
    height=6.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=2.0),
)
save()
