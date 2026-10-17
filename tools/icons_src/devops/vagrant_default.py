# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: vagrant (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(78.8, 91.0), (89.6, 84.69), (71.6, 74.22), (71.6, 74.2), (89.6, 84.69), (89.6, 77.18), (65.42, 17.91), (49.99, 9.0), (49.99, 9.0), (34.71, 17.84), (10.4, 76.95), (10.4, 84.69), (21.2, 91.0), (39.21, 80.44), (39.15, 80.4), (39.2, 80.38), (39.2, 73.25), (49.99, 48.0), (49.99, 39.57), (49.99, 48.0), (60.8, 73.25), (60.8, 80.45), (60.82, 80.45)], style=fill_style('#1159CC'))
polygon([(78.8, 91.0), (60.82, 80.45), (60.8, 80.45), (60.8, 73.25), (49.99, 48.0), (49.99, 39.57), (42.8, 35.39), (28.4, 67.86), (28.4, 74.22), (39.21, 80.44), (21.2, 91.0), (10.4, 84.69), (10.4, 76.95), (34.71, 17.84), (49.99, 9.0), (49.99, 31.21), (57.2, 35.39), (57.1, 35.44), (71.6, 67.86), (71.6, 74.22), (89.6, 84.69)], style=fill_style('#127EFF'))
save()
# fmt: on
