# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_logging (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(24.8, 52.1), (41.6, 52.1), (41.6, 43.7), (24.8, 43.7)], style=fill_style(GCP_TECH_MID))
polygon([(16.4, 22.7), (41.6, 22.7), (41.6, 14.3), (16.4, 14.3)], style=fill_style(GCP_TECH_MID))
polygon([(16.4, 22.7), (24.8, 22.7), (24.8, 73.1), (16.4, 73.1)], style=fill_style(GCP_TECH_MID))
polygon([(37.4, 68.9), (92.0, 68.9), (92.0, 85.7), (37.4, 85.7)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(37.4, 39.5), (92.0, 39.5), (92.0, 56.3), (37.4, 56.3)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(37.4, 10.1), (92.0, 10.1), (92.0, 26.9), (37.4, 26.9)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 64.7), (33.2, 64.7), (33.2, 89.9), (8.0, 89.9)], style=fill_style(GCP_TECH_LIGHT))
save()
# fmt: on
