# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k0s (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(60.57, 68.32), (60.57, 47.43), (39.17, 31.37), (39.17, 52.25)], style=Icon.fill_style("#000000"))
polygon([(91.47, 70.65), (91.47, 8.09), (8.27, 8.09), (8.27, 8.16), (30.41, 24.79), (74.76, 24.79), (74.77, 58.09), (91.47, 70.64)], style=Icon.fill_style("#13CEEC"))
polygon([(8.27, 91.46), (8.27, 29.05), (24.97, 41.6), (24.97, 74.76), (69.14, 74.76), (91.38, 91.46)], style=Icon.fill_style("#000000"))
save()
# fmt: on
