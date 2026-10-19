# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data icon: planetscale (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(90.0, 49.99), (89.47, 43.5), (87.96, 37.35), (85.53, 31.61), (82.28, 26.37), (78.28, 21.72), (73.63, 17.72), (68.39, 14.47), (62.65, 12.04), (56.5, 10.53), (50.01, 10.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(50.0, 90.0), (54.8, 89.72), (59.43, 88.88), (63.86, 87.53), (68.06, 85.7), (71.99, 83.42), (75.62, 80.72), (78.91, 77.64), (81.85, 74.2), (84.38, 70.45), (86.49, 66.41), (33.59, 13.51), (32.91, 13.82), (32.24, 14.15), (31.58, 14.49), (30.92, 14.84), (30.27, 15.2), (29.63, 15.57), (29.0, 15.95), (28.37, 16.35), (27.75, 16.75), (27.14, 17.17), (59.97, 50.0), (50.0, 50.0), (21.72, 21.72), (19.63, 23.97), (17.72, 26.38), (15.99, 28.93), (14.46, 31.62), (13.14, 34.43), (12.04, 37.36), (11.16, 40.39), (10.52, 43.51), (10.13, 46.72), (10.0, 50.0), (10.52, 56.49), (12.04, 62.64), (14.46, 68.38), (17.72, 73.62), (21.72, 78.28), (26.38, 82.28), (31.62, 85.54), (37.36, 87.96), (43.51, 89.48)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
