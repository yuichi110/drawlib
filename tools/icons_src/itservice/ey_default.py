# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""IT Service icon: ey (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(22.5, 18.37), (43.05, 18.37), (43.05, 9.0), (10.18, 9.0), (10.18, 49.72), (33.48, 49.72), (38.93, 40.35), (22.51, 40.35), (22.51, 33.63), (37.37, 33.63), (37.37, 25.09), (22.51, 25.09)], style=Icon.fill_style('#161D23'))
polygon([(64.92, 49.72), (57.94, 36.43), (50.99, 49.72), (37.36, 49.72), (51.71, 25.09), (51.71, 9.0), (64.01, 9.0), (64.01, 25.09), (78.36, 49.72)], style=Icon.fill_style('#161D23'))
polygon([(90.62, 75.85), (90.62, 91.0), (9.38, 61.63)], style=Icon.fill_style('#FFE600'))
save()
# fmt: on
