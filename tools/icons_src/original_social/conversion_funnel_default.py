# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: conversion_funnel (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
polygon(
    [(14.0, 84.0), (86.0, 84.0), (74.0, 64.0), (26.0, 64.0)],
    style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w),
)
polygon(
    [(26.0, 64.0), (74.0, 64.0), (62.0, 44.0), (38.0, 44.0)],
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w),
)
polygon(
    [(38.0, 44.0), (62.0, 44.0), (56.0, 26.0), (44.0, 26.0)],
    style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w),
)
circle((50.0, 15.0), radius=7.5, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
save()
