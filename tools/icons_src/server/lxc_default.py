# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: lxc (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import WHITE, draw_round_polyline, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(50.45, 88.31), (90.65, 65.11), (70.12, 53.99), (29.93, 77.2)], style=fill_style('#333333', border_color=WHITE, border_units=0.4))
polygon([(29.93, 77.2), (50.02, 65.59), (29.5, 54.48), (9.4, 66.08)], style=fill_style('#CDCDCD', border_color=WHITE, border_units=0.4))
polygon([(9.28, 65.88), (29.37, 54.28), (29.37, 46.62), (9.28, 58.22)], style=fill_style('#CDCDCD', border_color=WHITE, border_units=0.4))
polygon([(9.28, 58.04), (49.46, 34.84), (49.46, 27.18), (9.28, 50.39)], style=fill_style('#888888', border_color=WHITE, border_units=0.4))
polygon([(9.28, 50.23), (49.46, 27.03), (49.46, 11.72), (9.28, 34.92)], style=fill_style('#DD4814', border_color=WHITE, border_units=0.4))
polygon([(29.37, 54.33), (49.93, 65.46), (49.93, 57.8), (29.37, 46.67)], style=fill_style('#CDCDCD', border_color=WHITE, border_units=0.39))
polygon([(49.84, 57.58), (69.94, 45.98), (49.41, 34.87), (29.32, 46.47)], style=fill_style('#888888', border_color=WHITE, border_units=0.4))
polygon([(49.53, 34.63), (70.09, 45.75), (70.09, 38.1), (49.53, 26.97)], style=fill_style('#888888', border_color=WHITE, border_units=0.39))
polygon([(49.58, 26.99), (90.8, 49.31), (90.8, 34.01), (49.58, 11.68)], style=fill_style('#DD4814', border_color=WHITE, border_units=0.39))
polygon([(70.32, 53.84), (90.78, 64.92), (90.78, 49.61), (70.32, 38.53)], style=fill_style('#333333', border_color=WHITE, border_units=0.39))
polygon([(50.04, 65.37), (70.14, 53.77), (70.14, 46.11), (50.04, 57.72)], style=fill_style('#333333', border_color=WHITE, border_units=0.4))
draw_round_polyline([(30.15, 77.11), (30.15, 68.89)], width_units=0.4, color=WHITE, closed=False)
draw_round_polyline([(50.3, 57.49), (29.88, 68.89)], width_units=0.4, color=WHITE, closed=False)
draw_round_polyline([(29.88, 68.89), (9.2, 58.28)], width_units=0.4, color=WHITE, closed=False)
save()
# fmt: on
