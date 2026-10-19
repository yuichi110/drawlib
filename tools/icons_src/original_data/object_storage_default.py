# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: object_storage."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Bucket body
bucket_pts = [(20.0, 62.0), (80.0, 62.0), (70.0, 18.0), (30.0, 18.0)]
polygon(bucket_pts, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w))
ellipse(
    (50.0, 62.0),
    width=60.0,
    height=16.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w),
)
# Geometric objects inside/above bucket
circle((37.0, 67.0), radius=8.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
rectangle(
    (52.0, 71.0),
    width=14.0,
    height=14.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=2.0),
)
tri = [(64.0, 61.0), (75.0, 61.0), (69.5, 73.0)]
polygon(tri, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
save()
