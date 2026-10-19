# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: css3 (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(20.43, 17.2), (13.85, 91.0), (86.15, 91.0), (79.57, 17.21), (49.96, 9.0)], style=Icon.fill_style('#1572B6'))
polygon([(50.0, 15.27), (73.93, 21.91), (79.56, 84.97), (50.0, 84.97)], style=Icon.fill_style('#33A9DC'))
polygon([(50.0, 58.23), (61.98, 58.23), (62.81, 67.5), (50.0, 67.5), (50.0, 76.55), (72.7, 76.55), (72.48, 74.12), (70.26, 49.18), (50.0, 49.18)], style=Icon.fill_style('#FFFFFF'))
polygon([(50.05, 34.72), (50.01, 34.71), (39.93, 37.43), (39.29, 44.65), (30.2, 44.65), (31.47, 30.44), (50.01, 25.29), (50.05, 25.3)], style=Icon.fill_style('#EBEBEB'))
polygon([(61.21, 49.56), (60.12, 37.44), (50.02, 34.71), (50.02, 25.29), (68.58, 30.44), (68.72, 31.97), (70.29, 49.56)], style=Icon.fill_style('#FFFFFF'))
polygon([(50.03, 76.55), (50.03, 67.5), (28.17, 67.5), (27.99, 69.53), (27.57, 74.12), (27.36, 76.55)], style=Icon.fill_style('#EBEBEB'))
polygon([(50.0, 58.23), (50.0, 49.17), (40.05, 49.17), (39.87, 51.21), (39.45, 55.8), (39.24, 58.23)], style=Icon.fill_style('#EBEBEB'))
save()
# fmt: on
