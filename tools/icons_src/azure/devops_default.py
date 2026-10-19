# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: devops (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Azure, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(87.33, 73.33), (87.33, 27.88), (68.67, 12.57), (39.73, 23.12), (39.73, 12.67), (23.35, 34.09), (71.09, 30.35), (71.09, 71.28)], style=Icon.fill_style(Azure.BLUE))
polygon([(71.42, 71.05), (44.63, 87.33), (44.63, 76.65), (20.04, 69.41), (12.67, 59.94), (12.67, 38.43), (23.21, 33.76), (23.21, 61.34)], style=Icon.fill_style(Azure.BLUE))
save()
# fmt: on
