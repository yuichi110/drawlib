# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: trace (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(50.0, 41.6), (92.0, 41.6), (92.0, 58.4), (50.0, 58.4)], style=fill_style(GCP_TECH_MID))
polygon([(50.0, 8.0), (92.0, 8.0), (92.0, 24.8), (50.0, 24.8)], style=fill_style(GCP_TECH_MID))
polygon([(33.2, 8.0), (50.0, 8.0), (50.0, 24.8), (33.2, 24.8)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 92.0), (33.2, 92.0), (33.2, 75.2), (8.0, 75.2)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 58.4), (50.0, 58.4), (50.0, 41.6), (8.0, 41.6)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
