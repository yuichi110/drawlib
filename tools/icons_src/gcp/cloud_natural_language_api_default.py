# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_natural_language_api (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(83.6, 83.6), (71.0, 83.6), (71.0, 75.2), (83.6, 75.2), (83.6, 24.8), (71.0, 24.8), (71.0, 16.4), (83.6, 16.4), (92.0, 16.4), (92.0, 24.8), (92.0, 75.2), (92.0, 83.6)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(83.6, 71.0), (92.0, 75.2), (83.6, 75.2)], style=fill_style(GCP_TECH_MID))
polygon([(92.0, 29.0), (83.6, 24.8), (92.0, 24.8)], style=fill_style(GCP_TECH_MID))
polygon([(16.4, 16.4), (29.0, 16.4), (29.0, 24.8), (16.4, 24.8), (16.4, 75.2), (29.0, 75.2), (29.0, 83.6), (16.4, 83.6), (8.0, 83.6), (8.0, 75.2), (8.0, 24.8), (8.0, 16.4)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 29.0), (16.4, 24.8), (8.0, 24.8)], style=fill_style(GCP_TECH_MID))
polygon([(16.4, 71.0), (8.0, 75.2), (16.4, 75.2)], style=fill_style(GCP_TECH_MID))
polygon([(29.0, 54.2), (71.0, 54.2), (71.0, 45.8), (29.0, 45.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(29.0, 41.6), (71.0, 41.6), (71.0, 33.2), (29.0, 33.2)], style=fill_style(GCP_TECH_LIGHT))
polygon([(29.0, 66.8), (71.0, 66.8), (71.0, 58.4), (29.0, 58.4)], style=fill_style(GCP_TECH_LIGHT))
save()
# fmt: on
