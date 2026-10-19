# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AWS icon: forecast (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Aws, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
Aws.draw_service_plate(Aws.TEAL)
polygon([(58.4, 27.95), (68.9, 27.95), (68.9, 63.65), (58.4, 63.65)], holes=[[(60.5, 30.05), (66.8, 30.05), (66.8, 61.55), (60.5, 61.55)]], style=Icon.fill_style(Icon.WHITE))
polygon([(42.65, 27.95), (53.15, 27.95), (53.15, 55.25), (42.65, 55.25)], holes=[[(44.75, 30.05), (51.05, 30.05), (51.05, 53.15), (44.75, 53.15)]], style=Icon.fill_style(Icon.WHITE))
polygon([(26.9, 27.95), (37.4, 27.95), (37.4, 45.8), (26.9, 45.8)], holes=[[(29.0, 30.05), (35.3, 30.05), (35.3, 43.7), (29.0, 43.7)]], style=Icon.fill_style(Icon.WHITE))
polygon([(73.1, 76.25), (73.1, 74.15), (75.5, 74.15), (69.21, 68.9), (57.83, 68.9), (57.69, 68.89), (57.55, 68.86), (57.42, 68.82), (57.3, 68.76), (57.19, 68.68), (57.08, 68.59), (56.99, 68.48), (56.91, 68.36), (52.51, 60.5), (41.27, 60.5), (41.11, 60.49), (40.96, 60.45), (40.81, 60.39), (40.68, 60.31), (40.56, 60.22), (40.45, 60.1), (40.36, 59.97), (40.29, 59.82), (36.96, 51.05), (26.9, 51.05), (26.9, 48.95), (37.69, 48.95), (37.85, 48.96), (38.0, 49.0), (38.15, 49.06), (38.28, 49.14), (38.4, 49.23), (38.51, 49.35), (38.6, 49.48), (38.67, 49.63), (42.0, 58.4), (53.13, 58.4), (53.27, 58.41), (53.41, 58.44), (53.54, 58.48), (53.66, 58.54), (53.78, 58.62), (53.88, 58.71), (53.97, 58.82), (54.05, 58.94), (58.45, 66.8), (69.59, 66.8), (69.68, 66.8), (69.77, 66.82), (69.86, 66.84), (69.94, 66.86), (70.03, 66.9), (70.11, 66.94), (70.19, 66.99), (70.26, 67.04), (77.3, 72.92), (77.3, 69.95), (79.4, 69.95), (79.4, 76.25)], style=Icon.fill_style(Icon.WHITE))
polygon([(74.15, 64.7), (76.25, 64.7), (76.25, 22.7), (67.85, 22.7), (20.6, 22.7), (20.6, 75.2), (65.75, 75.2), (65.75, 73.1), (22.7, 73.1), (22.7, 24.8), (67.85, 24.8), (74.15, 24.8)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
