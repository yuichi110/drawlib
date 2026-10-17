# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: pandas (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(38.62, 86.15), (47.58, 86.15), (47.58, 67.55), (38.62, 67.55)], style=fill_style('#130754'))
polygon([(38.62, 47.93), (47.58, 47.93), (47.58, 29.32), (38.62, 29.32)], style=fill_style('#130754'))
polygon([(38.62, 62.11), (47.58, 62.11), (47.58, 53.33), (38.62, 53.33)], style=fill_style('#FFCA00'))
polygon([(24.22, 70.85), (33.18, 70.85), (33.18, 9.0), (24.22, 9.0)], style=fill_style('#130754'))
polygon([(52.72, 32.58), (61.68, 32.58), (61.68, 13.96), (52.72, 13.96)], style=fill_style('#130754'))
polygon([(52.72, 70.83), (61.68, 70.83), (61.68, 52.22), (52.72, 52.22)], style=fill_style('#130754'))
polygon([(52.72, 46.79), (61.68, 46.79), (61.68, 38.01), (52.72, 38.01)], style=fill_style('#E70488'))
polygon([(66.82, 91.0), (75.78, 91.0), (75.78, 29.15), (66.82, 29.15)], style=fill_style('#130754'))
save()
# fmt: on
