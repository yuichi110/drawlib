# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: cicd_pipeline."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

circle((50.0, 50.0), radius=30.0, style=Icon.stroke_style(Icon.DARK, width_units=w))

circle(
    (50.0, 80.0),
    radius=11.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
circle(
    (24.0, 35.0),
    radius=11.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)
circle(
    (76.0, 35.0),
    radius=11.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)

polygon(
    [(45.0, 58.0), (45.0, 42.0), (59.0, 50.0)],
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=2.0, shape_r=1.5),
)

save()
