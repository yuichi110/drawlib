# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: virtual_private_cloud (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(66.8, 92.0), (92.0, 92.0), (92.0, 66.8), (66.8, 66.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(79.4, 92.0), (92.0, 92.0), (92.0, 66.8), (79.4, 66.8)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(66.8, 33.2), (92.0, 33.2), (92.0, 8.0), (66.8, 8.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(79.4, 33.2), (92.0, 33.2), (92.0, 8.0), (79.4, 8.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(8.0, 92.0), (33.2, 92.0), (33.2, 66.8), (8.0, 66.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(20.6, 92.0), (33.2, 92.0), (33.2, 66.8), (20.6, 66.8)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(8.0, 33.2), (33.2, 33.2), (33.2, 8.0), (8.0, 8.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(20.6, 33.2), (33.2, 33.2), (33.2, 8.0), (20.6, 8.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(33.2, 83.6), (66.8, 83.6), (66.8, 75.2), (33.2, 75.2)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(33.2, 24.8), (66.8, 24.8), (66.8, 16.4), (33.2, 16.4)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(75.2, 66.8), (83.6, 66.8), (83.6, 33.2), (75.2, 33.2)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(16.4, 66.8), (24.8, 66.8), (24.8, 33.2), (16.4, 33.2)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(16.4, 66.8), (24.8, 66.8), (24.8, 58.4), (16.4, 58.4)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(75.2, 66.8), (83.6, 66.8), (83.6, 58.4), (75.2, 58.4)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(33.2, 83.6), (41.6, 83.6), (41.6, 75.2), (33.2, 75.2)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(33.2, 24.8), (41.6, 24.8), (41.6, 16.4), (33.2, 16.4)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
