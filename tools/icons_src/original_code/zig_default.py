# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: zig (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(34.05, 75.1), (24.64, 63.59), (19.93, 70.91)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(34.05, 75.1), (27.26, 69.35), (24.64, 63.59), (21.5, 63.59), (21.5, 36.93), (26.21, 36.93), (20.46, 34.31), (16.27, 25.43), (10.0, 25.43), (10.0, 75.1)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(26.21, 36.93), (16.27, 25.43), (12.09, 31.18)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(39.28, 75.1), (42.42, 67.78), (29.35, 63.59)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(39.28, 75.1), (68.04, 75.1), (68.04, 63.59), (29.35, 63.59), (39.28, 69.87)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(70.65, 36.93), (60.72, 25.43), (57.06, 32.22)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(70.65, 36.93), (62.29, 32.22), (60.72, 25.42), (31.96, 25.42), (31.96, 36.93)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(88.43, 86.6), (37.19, 25.43), (11.57, 13.4), (62.81, 75.1)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(83.72, 75.1), (83.2, 65.69), (73.79, 63.07)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(90.0, 75.1), (90.0, 25.42), (65.43, 25.42), (72.75, 31.7), (75.36, 36.93), (78.5, 36.93), (78.5, 63.07), (73.79, 63.07), (79.02, 67.78), (83.73, 75.1)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(75.36, 36.93), (77.97, 29.08), (65.43, 25.42)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
