# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI icon: modal (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(26.3, 71.43), (10.0, 43.33), (18.4, 28.66), (35.24, 28.66), (49.89, 54.39), (64.93, 28.69), (81.58, 28.57), (90.0, 43.14), (73.81, 71.32), (56.9, 71.37), (49.98, 59.37), (43.13, 71.43)], holes=[[(29.09, 69.0), (41.71, 69.0), (47.86, 58.16), (35.24, 58.16)], [(59.72, 68.93), (72.4, 68.89), (86.49, 44.38), (74.04, 44.47)], [(26.99, 67.78), (33.13, 56.95), (19.1, 32.32), (12.8, 43.32)], [(57.61, 67.73), (71.93, 43.26), (65.63, 32.32), (51.29, 56.8)], [(35.23, 55.73), (47.87, 55.73), (33.83, 31.09), (21.2, 31.09)], [(74.03, 42.04), (86.5, 41.95), (80.19, 31.01), (67.72, 31.1)]], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
