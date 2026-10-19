# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: ray (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(84.0, 48.8), (51.2, 16.0), (48.8, 18.4), (81.6, 51.2)], style=Icon.fill_style('#02A0CF'))
polygon([(82.79, 48.06), (17.28, 48.06), (17.28, 51.46), (82.79, 51.46)], style=Icon.fill_style('#02A0CF'))
polygon([(48.8, 81.6), (81.6, 48.8), (84.0, 51.2), (51.2, 84.0)], style=Icon.fill_style('#02A0CF'))
polygon([(9.0, 58.2), (25.4, 58.2), (25.4, 41.8), (9.0, 41.8)], style=Icon.fill_style('#02A0CF'))
polygon([(41.8, 58.2), (58.2, 58.2), (58.2, 41.8), (41.8, 41.8)], style=Icon.fill_style('#02A0CF'))
polygon([(41.8, 91.0), (58.2, 91.0), (58.2, 74.6), (41.8, 74.6)], style=Icon.fill_style('#02A0CF'))
polygon([(41.8, 25.4), (58.2, 25.4), (58.2, 9.0), (41.8, 9.0)], style=Icon.fill_style('#02A0CF'))
polygon([(74.6, 58.2), (91.0, 58.2), (91.0, 41.8), (74.6, 41.8)], style=Icon.fill_style('#02A0CF'))
save()
# fmt: on
