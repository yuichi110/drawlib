# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AWS icon: appflow (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Aws, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
Aws.draw_service_plate(Aws.PINK)
polygon([(51.74, 72.05), (35.26, 44.34), (34.17, 48.41), (32.14, 47.87), (34.2, 40.21), (41.85, 42.26), (41.31, 44.29), (36.98, 43.13), (52.93, 69.95), (68.7, 69.95), (76.58, 56.3), (68.7, 42.65), (60.46, 42.65), (60.46, 40.55), (69.91, 40.55), (79.01, 56.3), (69.91, 72.05)], style=Icon.fill_style(Icon.WHITE))
polygon([(56.87, 57.74), (57.41, 55.71), (61.79, 56.89), (46.66, 30.05), (30.91, 30.05), (23.02, 43.7), (30.91, 57.35), (37.36, 57.35), (37.36, 59.45), (29.69, 59.45), (20.6, 43.7), (29.69, 27.95), (47.88, 27.95), (63.48, 55.6), (64.55, 51.59), (66.58, 52.13), (64.53, 59.79)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
