# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: prisma_cloud (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 91.0), (86.53, 65.65), (50.0, 47.02)], style=Icon.fill_style('#00C0E8'))
polygon([(50.0, 91.0), (13.47, 65.65), (50.0, 47.02)], style=Icon.fill_style('#38BDF8'))
polygon([(13.47, 65.65), (50.0, 47.02), (50.0, 9.0)], style=Icon.fill_style('#0284C7'))
polygon([(86.53, 65.65), (50.0, 47.02), (50.0, 9.0)], style=Icon.fill_style('#0369A1'))
polygon([(50.0, 74.6), (68.64, 61.18), (50.0, 28.38), (31.36, 61.18)], style=Icon.fill_style('#4993BB'))
save()
# fmt: on
