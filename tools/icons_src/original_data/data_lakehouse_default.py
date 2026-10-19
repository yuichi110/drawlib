# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: data_lakehouse."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Structured house upper half
rectangle(
    (50.0, 52.0), width=64.0, height=34.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w)
)
roof = [(12.0, 68.0), (88.0, 68.0), (50.0, 88.0)]
polygon(roof, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w))
# Table cells inside house
rectangle(
    (38.0, 54.0),
    width=16.0,
    height=14.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (62.0, 54.0),
    width=16.0,
    height=14.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
# Data lake wave base
lake = [(12.0, 36.0), (30.0, 40.0), (50.0, 34.0), (70.0, 40.0), (88.0, 36.0), (84.0, 14.0), (16.0, 14.0)]
polygon(lake, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
Icon.draw_round_polyline(
    [(22.0, 25.0), (38.0, 28.0), (52.0, 23.0), (68.0, 28.0), (78.0, 25.0)], width_units=w, color=Icon.WHITE
)
save()
