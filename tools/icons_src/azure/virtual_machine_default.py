# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: virtual_machine (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Azure, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(88.64, 91.02), (89.36, 90.92), (90.04, 90.64), (90.62, 90.2), (91.06, 89.62), (91.34, 88.94), (91.44, 88.22), (91.44, 37.82), (91.34, 37.1), (91.06, 36.42), (90.62, 35.84), (90.04, 35.4), (89.36, 35.12), (88.64, 35.02), (10.24, 35.02), (9.52, 35.12), (8.84, 35.4), (8.26, 35.84), (7.82, 36.42), (7.54, 37.1), (7.44, 37.82), (7.44, 88.22), (7.54, 88.94), (7.82, 89.62), (8.26, 90.2), (8.84, 90.64), (9.52, 90.92), (10.24, 91.02)], style=Icon.fill_style(Azure.BLUE))
polygon([(63.44, 71.19), (63.44, 54.9), (49.44, 46.69), (49.44, 63.02)], style=Icon.fill_style(Azure.CYAN))
polygon([(63.44, 71.19), (49.44, 62.97), (35.44, 71.19), (49.44, 79.35)], style=Icon.fill_style(Azure.PALE_CYAN))
polygon([(49.44, 62.97), (49.44, 46.69), (35.44, 54.9), (35.44, 71.19)], style=Icon.fill_style(Azure.LIGHT_CYAN))
polygon([(35.44, 54.9), (49.44, 63.02), (49.44, 46.69)], style=Icon.fill_style(Azure.PALE_CYAN))
polygon([(63.44, 54.9), (49.44, 63.02), (49.44, 46.69)], style=Icon.fill_style(Azure.LIGHT_CYAN))
polygon([(66.29, 18.08), (63.53, 18.79), (61.43, 19.92), (59.9, 21.47), (58.86, 23.42), (58.19, 25.76), (57.83, 28.48), (57.68, 31.57), (57.65, 35.02), (41.18, 35.02), (41.15, 31.57), (41.01, 28.48), (40.65, 25.76), (40.0, 23.42), (38.96, 21.47), (37.44, 19.92), (35.35, 18.79), (32.59, 18.08), (31.49, 17.82), (30.48, 17.3), (29.62, 16.54), (28.97, 15.61), (28.57, 14.54), (28.44, 13.41), (70.44, 13.41), (70.31, 14.54), (69.91, 15.61), (69.26, 16.54), (68.4, 17.3), (67.39, 17.82)], style=Icon.fill_style(Azure.LIGHT_GRAY))
save()
# fmt: on
