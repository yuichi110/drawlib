# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: tensorflow_enterprise (default variant)."""

from drawlib.canvas import save
from drawlib.utils import GCP_TECH_MID, draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(51.58, 92.0), (86.7, 71.51), (86.75, 52.92), (65.61, 65.39), (65.61, 56.0), (76.15, 49.85), (76.21, 33.69), (65.61, 39.95), (65.61, 16.32), (51.58, 8.0)], [(48.42, 92.0), (48.42, 8.0), (34.39, 16.32), (34.39, 65.39), (13.25, 52.92), (13.3, 71.51)]], color=GCP_TECH_MID)
save()
# fmt: on
