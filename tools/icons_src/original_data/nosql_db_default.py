# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: nosql_db."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
Icon.draw_cylinder_tier(
    50.0, 18.0, 68.0, 56.0, 12.0, body_color=Icon.PASTEL_BLUE, top_color=Icon.PASTEL_BLUE_LIGHT, border_units=w
)
rectangle(
    (50.0, 43.0),
    width=46.0,
    height=28.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)
# Curly braces { } inside card
Icon.draw_round_polyline(
    [(38.0, 51.0), (34.0, 51.0), (34.0, 45.0), (31.0, 43.0), (34.0, 41.0), (34.0, 35.0), (38.0, 35.0)],
    width_units=w,
    color=Icon.DARK,
)
Icon.draw_round_polyline(
    [(62.0, 51.0), (66.0, 51.0), (66.0, 45.0), (69.0, 43.0), (66.0, 41.0), (66.0, 35.0), (62.0, 35.0)],
    width_units=w,
    color=Icon.DARK,
)
circle((45.0, 43.0), radius=4.2, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
circle((55.0, 43.0), radius=4.2, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w))
save()
