# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: joint_venture (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Left & Right Partner Enterprise Towers
rectangle((26, 48), width=26, height=52, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0))
rectangle((74, 48), width=26, height=52, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0))
for wy in (36, 50, 64):
    rectangle((24, wy), width=10, height=6, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.0))
    rectangle((76, wy), width=10, height=6, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.4, shape_r=1.0))
# Central Interlocking Alliance Shield / Badge linking both companies
circle((50, 48), radius=16.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer))
circle((45, 48), radius=6.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8))
circle((55, 48), radius=6.5, style=Icon.stroke_style(width_units=1.8))
save()
# fmt: on
