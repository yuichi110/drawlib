# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_interconnect (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(8.0, 45.8), (24.8, 45.8), (24.8, 54.2), (8.0, 54.2)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(62.6, 29.0), (20.6, 29.0), (20.6, 71.0), (62.6, 71.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(72.39, 45.8), (92.0, 45.8), (92.0, 54.2), (72.39, 54.2)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(33.2, 87.8), (33.2, 79.4), (71.0, 79.4), (71.0, 20.6), (33.2, 20.6), (33.2, 12.2), (79.4, 12.2), (79.4, 20.6), (79.4, 79.4), (79.4, 87.8)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(62.6, 29.0), (41.6, 29.0), (41.6, 71.0), (62.6, 71.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
