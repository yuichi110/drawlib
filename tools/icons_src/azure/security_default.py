# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: security (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_BLUE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(80.33, 52.4), (79.29, 45.26), (76.49, 38.59), (72.44, 32.47), (67.64, 27.02), (62.59, 22.33), (57.81, 18.52), (53.78, 15.67), (51.02, 13.9), (50.64, 13.73), (50.23, 13.64), (49.81, 13.64), (49.4, 13.73), (49.02, 13.9), (46.25, 15.67), (42.22, 18.52), (37.42, 22.33), (32.37, 27.02), (27.57, 32.47), (23.51, 38.59), (20.71, 45.26), (19.67, 52.4), (19.67, 75.94), (19.73, 76.43), (19.92, 76.88), (20.21, 77.26), (20.6, 77.56), (21.05, 77.75), (21.53, 77.81), (27.56, 78.32), (31.91, 79.36), (35.08, 80.74), (37.53, 82.28), (39.77, 83.8), (42.27, 85.11), (45.52, 86.03), (50.0, 86.38), (54.48, 86.03), (57.73, 85.11), (60.23, 83.8), (62.47, 82.28), (64.92, 80.74), (68.09, 79.35), (72.44, 78.32), (78.47, 77.8), (78.88, 77.76), (79.28, 77.62), (79.63, 77.4), (79.93, 77.1), (80.15, 76.75), (80.29, 76.35), (80.33, 75.94)], style=fill_style(AZURE_BLUE))
save()
# fmt: on
