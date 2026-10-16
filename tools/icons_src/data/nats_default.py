# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data icon: nats (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import WHITE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(50.0, 91.0), (89.6, 91.0), (89.6, 58.89), (50.0, 58.89)], style=fill_style("#34A574"))
polygon([(10.4, 91.0), (50.0, 91.0), (50.0, 58.89), (10.4, 58.89)], style=fill_style("#27AAE1"))
polygon([(89.6, 58.87), (89.6, 26.76), (63.55, 26.76), (63.55, 9.0), (44.18, 26.7), (50.0, 26.94), (50.0, 58.87)], style=fill_style("#8DC63F"))
polygon([(50.0, 58.87), (50.0, 21.53), (44.18, 26.7), (10.4, 26.7), (10.4, 58.87)], style=fill_style("#375C93"))
polygon([(66.4, 49.48), (66.4, 76.07), (75.87, 76.07), (75.87, 41.69), (61.53, 41.69), (32.57, 68.74), (32.57, 41.67), (23.07, 41.67), (23.07, 76.07), (37.91, 76.07)], style=fill_style(WHITE))
save()
# fmt: on
