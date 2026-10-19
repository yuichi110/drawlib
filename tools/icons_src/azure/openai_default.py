# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: openai (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Azure, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(8.0, 79.4), (8.0, 20.6), (8.26, 18.06), (8.99, 15.7), (10.15, 13.56), (11.69, 11.69), (13.56, 10.15), (15.7, 8.99), (18.06, 8.26), (20.6, 8.0), (79.4, 8.0), (81.94, 8.26), (84.3, 8.99), (86.44, 10.15), (88.31, 11.69), (89.85, 13.56), (91.01, 15.7), (91.74, 18.06), (92.0, 20.6), (92.0, 79.4), (91.74, 81.94), (91.01, 84.3), (89.85, 86.44), (88.31, 88.31), (86.44, 89.85), (84.3, 91.01), (81.94, 91.74), (79.4, 92.0), (20.6, 92.0), (18.06, 91.74), (15.7, 91.01), (13.56, 89.85), (11.69, 88.31), (10.15, 86.44), (8.99, 84.3), (8.26, 81.94)], holes=[[(58.4, 92.0), (58.4, 75.2), (59.08, 68.43), (61.04, 62.12), (64.14, 56.41), (68.24, 51.44), (73.21, 47.34), (78.92, 44.24), (85.23, 42.28), (92.0, 41.6), (75.2, 41.6), (68.43, 40.92), (62.12, 38.96), (56.42, 35.86), (51.44, 31.76), (47.34, 26.79), (44.24, 21.09), (42.28, 14.78), (41.6, 8.01), (41.6, 24.8), (40.92, 31.57), (38.96, 37.88), (35.86, 43.59), (31.76, 48.56), (26.79, 52.66), (21.08, 55.76), (14.77, 57.72), (8.0, 58.4), (24.8, 58.4), (31.57, 59.08), (37.88, 61.04), (43.59, 64.14), (48.56, 68.24), (52.66, 73.21), (55.76, 78.92), (57.72, 85.23)]], style=Icon.fill_style(Azure.PALE_BLUE))
save()
# fmt: on
