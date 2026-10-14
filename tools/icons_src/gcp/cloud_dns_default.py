# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_dns (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, WHITE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(54.2, 24.8), (45.8, 24.8), (45.8, 66.8), (54.2, 66.8)], style=fill_style(GCP_TECH_MID))
polygon([(8.0, 12.2), (92.0, 12.2), (92.0, 20.6), (8.0, 20.6)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(41.6, 8.0), (58.4, 8.0), (58.4, 24.8), (41.6, 24.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(8.0, 92.0), (92.0, 92.0), (92.0, 66.8), (8.0, 66.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(50.0, 92.0), (92.0, 92.0), (92.0, 66.8), (50.0, 66.8)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(16.4, 83.6), (24.8, 83.6), (24.8, 75.2), (16.4, 75.2)], style=fill_style(WHITE))
polygon([(8.0, 58.4), (92.0, 58.4), (92.0, 33.2), (8.0, 33.2)], style=fill_style(GCP_TECH_LIGHT))
polygon([(50.0, 58.4), (92.0, 58.4), (92.0, 33.2), (50.0, 33.2)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(16.4, 50.0), (24.8, 50.0), (24.8, 41.6), (16.4, 41.6)], style=fill_style(WHITE))
save()
# fmt: on
