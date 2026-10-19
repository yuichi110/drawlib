# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: mimir (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 91.0), (86.44, 70.12), (50.0, 49.24), (13.56, 70.12)], style=Icon.fill_style('#FBBF24'))
polygon([(13.56, 70.12), (50.0, 49.24), (50.0, 9.0), (13.56, 29.88)], style=Icon.fill_style('#F59E0B'))
polygon([(86.44, 70.12), (86.44, 29.88), (50.0, 9.0), (50.0, 49.24)], style=Icon.fill_style('#EA580C'))
Icon.draw_round_polyline([(25.7, 52.28), (37.85, 61.39), (50.0, 46.96), (62.15, 61.39), (74.3, 52.28)], width_units=5.16, color='#FFFFFF')
save()
# fmt: on
