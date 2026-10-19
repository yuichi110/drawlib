# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: solidity (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(63.11, 91.0), (49.93, 67.57), (23.58, 67.57), (36.75, 91.0)], style=Icon.fill_style('#363636'))
polygon([(49.93, 67.57), (76.29, 67.57), (63.11, 91.0), (36.75, 91.0)], style=Icon.fill_style('#363636'))
polygon([(36.75, 44.15), (49.93, 67.57), (36.75, 91.0), (23.58, 67.57)], style=Icon.fill_style('#363636'))
polygon([(36.88, 9.0), (50.06, 32.43), (76.42, 32.43), (63.24, 9.0)], style=Icon.fill_style('#363636'))
polygon([(50.06, 32.43), (23.71, 32.43), (36.88, 9.0), (63.24, 9.0)], style=Icon.fill_style('#363636'))
polygon([(63.24, 55.85), (50.07, 32.43), (63.24, 9.0), (76.42, 32.43)], style=Icon.fill_style('#363636'))
save()
# fmt: on
