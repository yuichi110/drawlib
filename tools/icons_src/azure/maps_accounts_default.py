# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: maps_accounts (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_DARK_TEAL, AZURE_LIGHT_CYAN, AZURE_TEAL, WHITE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(89.67, 50.0), (88.9, 42.26), (86.65, 34.82), (82.98, 27.96), (78.05, 21.95), (72.04, 17.02), (65.18, 13.35), (57.74, 11.1), (50.0, 10.33), (42.26, 11.1), (34.82, 13.35), (27.96, 17.02), (21.95, 21.95), (17.02, 27.96), (13.35, 34.82), (11.1, 42.26), (10.33, 50.0), (11.1, 57.74), (13.35, 65.18), (17.02, 72.04), (21.95, 78.05), (27.96, 82.98), (34.82, 86.65), (42.26, 88.9), (50.0, 89.67), (57.74, 88.9), (65.18, 86.65), (72.04, 82.98), (78.05, 78.05), (82.98, 72.04), (86.65, 65.18), (88.9, 57.74)], style=fill_style(AZURE_DARK_TEAL))
polygon([(55.98, 79.13), (26.39, 32.17), (63.44, 46.54)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(50.0, 69.65), (68.36, 25.13), (55.98, 79.13)], style=fill_style(WHITE, alpha=0.7))
polygon([(48.94, 40.91), (60.07, 45.23), (68.36, 25.13)], style=fill_style(AZURE_TEAL))
save()
# fmt: on
