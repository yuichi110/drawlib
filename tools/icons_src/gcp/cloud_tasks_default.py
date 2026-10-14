# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_tasks (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(45.33, 82.67), (54.67, 82.67), (54.67, 50.0), (45.33, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(45.33, 50.0), (54.67, 50.0), (54.67, 17.33), (45.33, 17.33)], style=fill_style(GCP_TECH_MID))
polygon([(64.0, 82.67), (73.33, 82.67), (73.33, 50.0), (64.0, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(64.0, 50.0), (73.33, 50.0), (73.33, 17.33), (64.0, 17.33)], style=fill_style(GCP_TECH_MID))
polygon([(82.67, 82.67), (92.0, 82.67), (92.0, 50.0), (82.67, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(82.67, 50.0), (92.0, 50.0), (92.0, 17.33), (82.67, 17.33)], style=fill_style(GCP_TECH_MID))
polygon([(26.67, 82.67), (36.0, 82.67), (36.0, 50.0), (26.67, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(26.67, 50.0), (36.0, 50.0), (36.0, 17.33), (26.67, 17.33)], style=fill_style(GCP_TECH_MID))
polygon([(8.0, 82.67), (17.33, 82.67), (17.33, 50.0), (8.0, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 50.0), (17.33, 50.0), (17.33, 17.33), (8.0, 17.33)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
