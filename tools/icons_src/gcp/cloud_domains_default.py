# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_domains (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(68.87, 76.84), (46.94, 23.21), (53.06, 76.84)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(53.06, 76.84), (46.94, 23.21), (31.13, 23.21)], style=fill_style(GCP_TECH_LIGHT))
polygon([(14.29, 38.58), (8.0, 23.21), (19.07, 23.21), (20.84, 38.58)], style=fill_style(GCP_TECH_LIGHT))
polygon([(23.42, 60.81), (21.66, 45.39), (17.05, 45.39)], style=fill_style(GCP_TECH_LIGHT))
polygon([(39.14, 60.81), (39.1, 60.68), (32.86, 45.39), (21.66, 45.39), (23.42, 60.81)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(92.0, 76.84), (70.03, 23.16), (76.19, 76.84)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(76.19, 76.84), (70.03, 23.16), (54.22, 23.16)], style=fill_style(GCP_TECH_LIGHT))
polygon([(30.1, 38.58), (23.77, 23.21), (19.07, 23.21), (20.84, 38.58)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
