# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_endpoints (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(62.74, 58.42), (37.47, 58.42), (33.26, 50.0), (37.47, 41.58), (62.74, 41.58), (66.95, 50.0)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(66.95, 50.0), (62.74, 58.42), (39.62, 58.42), (37.47, 58.42), (33.26, 50.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(75.37, 75.26), (62.74, 75.26), (79.45, 50.0), (85.77, 59.47)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(92.0, 50.0), (85.77, 59.47), (79.45, 50.0), (62.74, 24.74), (75.37, 24.74)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(24.63, 24.74), (37.26, 24.74), (20.55, 50.0), (14.23, 40.53)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(8.0, 50.0), (14.23, 40.53), (20.55, 50.0), (37.26, 75.26), (24.63, 75.26)], style=Icon.fill_style(Gcp.TECH_LIGHT))
save()
# fmt: on
