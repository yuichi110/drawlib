# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: truenas (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(91.0, 56.65), (91.0, 39.22), (53.59, 17.66), (53.59, 35.09)], style=Icon.fill_style('#31BEEC'))
polygon([(46.44, 35.09), (46.44, 17.66), (9.0, 39.22), (9.0, 56.65), (25.92, 46.92), (25.92, 46.91), (25.93, 46.91), (25.93, 46.9), (25.94, 46.9), (25.95, 46.89), (25.96, 46.89), (25.96, 46.88), (25.96, 46.88), (25.97, 46.88)], style=Icon.fill_style('#0095D5'))
polygon([(65.14, 49.99), (50.01, 41.27), (34.87, 49.99), (50.01, 58.72)], style=Icon.fill_style('#AEADAE'))
polygon([(87.44, 62.83), (72.29, 54.11), (53.59, 64.9), (53.59, 82.34)], style=Icon.fill_style('#0095D5'))
polygon([(46.44, 82.34), (46.44, 64.9), (27.71, 54.12), (12.56, 62.83)], style=Icon.fill_style('#31BEEC'))
save()
# fmt: on
