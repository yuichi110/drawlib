# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: time_series_db."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
Icon.draw_cylinder_tier(
    38.0, 22.0, 48.0, 54.0, 9.5, body_color=Icon.PASTEL_BLUE, top_color=Icon.PASTEL_BLUE_LIGHT, border_units=w
)
# Chart panel on bottom-right
rectangle(
    (60.0, 38.0),
    width=52.0,
    height=40.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=5.0),
)
pts = [(39.0, 26.0), (51.0, 38.0), (61.0, 31.0), (74.0, 49.0), (81.0, 45.0)]
area_pts = [(39.0, 22.0), *pts, (81.0, 22.0)]
polygon(area_pts, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
Icon.draw_round_polyline(pts, width_units=w * 1.2, color=Icon.DARK)
for px, py in pts[1:-1]:
    circle((px, py), radius=3.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
save()
