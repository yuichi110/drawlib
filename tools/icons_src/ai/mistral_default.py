# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: mistral (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(20.71, 79.29), (32.43, 79.29), (32.43, 67.57), (20.71, 67.57)], style=Icon.fill_style('#FFD700'))
polygon([(67.57, 79.29), (79.29, 79.29), (79.29, 67.57), (67.57, 67.57)], style=Icon.fill_style('#FFD700'))
polygon([(20.71, 67.57), (44.14, 67.57), (44.14, 55.86), (20.72, 55.86), (20.72, 67.57)], style=Icon.fill_style('#FFAF00'))
polygon([(55.86, 67.57), (79.28, 67.57), (79.28, 55.86), (55.86, 55.86)], style=Icon.fill_style('#FFAF00'))
polygon([(20.71, 55.85), (79.29, 55.85), (79.29, 44.14), (20.71, 44.14)], style=Icon.fill_style('#FF8205'))
polygon([(20.71, 44.14), (32.43, 44.14), (32.43, 32.43), (20.71, 32.43)], style=Icon.fill_style('#FA500F'))
polygon([(44.14, 44.14), (55.86, 44.14), (55.86, 32.43), (44.14, 32.43)], style=Icon.fill_style('#FA500F'))
polygon([(67.57, 44.14), (79.29, 44.14), (79.29, 32.43), (67.57, 32.43)], style=Icon.fill_style('#FA500F'))
polygon([(9.0, 32.43), (44.14, 32.43), (44.14, 20.71), (9.0, 20.71)], style=Icon.fill_style('#E10500'))
polygon([(55.86, 32.43), (91.0, 32.43), (91.0, 20.71), (55.86, 20.71)], style=Icon.fill_style('#E10500'))
save()
# fmt: on
