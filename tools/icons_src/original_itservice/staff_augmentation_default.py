# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: staff_augmentation (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Core internal team (2 avatars on left)
circle((24, 62), radius=9.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
b1: list[tuple[float, float]] = [(10, 26), (14, 48), (34, 48), (38, 26)]
polygon(b1, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(b1, width_units=w_outer, color=Icon.DARK, closed=True)
circle((44, 66), radius=9.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
b2: list[tuple[float, float]] = [(30, 30), (34, 52), (54, 52), (58, 30)]
polygon(b2, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(b2, width_units=w_outer, color=Icon.DARK, closed=True)
# Augmented external specialist joining on right (highlighted PASTEL_GREEN)
circle((72, 62), radius=11.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer))
b3: list[tuple[float, float]] = [(56, 24), (60, 48), (84, 48), (88, 24)]
polygon(b3, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(b3, width_units=w_outer, color=Icon.DARK, closed=True)
# Plus badge at top right
circle((82, 80), radius=9.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer))
Icon.draw_round_segment((77, 80), (87, 80), width_units=2.2, color=Icon.DARK)
Icon.draw_round_segment((82, 75), (82, 85), width_units=2.2, color=Icon.DARK)
save()
# fmt: on
