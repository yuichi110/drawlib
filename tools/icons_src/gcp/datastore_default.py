# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: datastore (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, WHITE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(29.0, 75.2), (33.2, 79.4), (8.0, 79.4), (12.2, 75.2)], style=fill_style(GCP_TECH_LIGHT))
polygon([(29.0, 75.2), (29.0, 58.4), (33.2, 54.2), (33.2, 79.4)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(12.2, 75.2), (8.0, 79.4), (8.0, 54.2), (12.2, 58.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(12.2, 58.4), (8.0, 54.2), (33.2, 54.2), (29.0, 58.4)], style=fill_style(GCP_TECH_MID))
polygon([(12.2, 75.2), (29.0, 75.2), (29.0, 58.4), (12.2, 58.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(58.4, 75.2), (62.6, 79.4), (37.4, 79.4), (41.6, 75.2)], style=fill_style(GCP_TECH_MID))
polygon([(58.4, 75.2), (58.4, 58.4), (62.6, 54.2), (62.6, 79.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(41.6, 75.2), (37.4, 79.4), (37.4, 54.2), (41.6, 58.4)], style=fill_style(GCP_TECH_MID))
polygon([(41.6, 58.4), (37.4, 54.2), (62.6, 54.2), (58.4, 58.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(41.6, 75.2), (58.4, 75.2), (58.4, 58.4), (41.6, 58.4)], style=fill_style(WHITE))
polygon([(87.8, 75.2), (92.0, 79.4), (66.8, 79.4), (71.0, 75.2)], style=fill_style(GCP_TECH_MID))
polygon([(87.8, 75.2), (87.8, 58.4), (92.0, 54.2), (92.0, 79.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(71.0, 75.2), (66.8, 79.4), (66.8, 54.2), (71.0, 58.4)], style=fill_style(GCP_TECH_MID))
polygon([(71.0, 58.4), (66.8, 54.2), (92.0, 54.2), (87.8, 58.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(71.0, 75.2), (87.8, 75.2), (87.8, 58.4), (71.0, 58.4)], style=fill_style(WHITE))
polygon([(29.0, 41.6), (33.2, 45.8), (8.0, 45.8), (12.2, 41.6)], style=fill_style(GCP_TECH_MID))
polygon([(29.0, 41.6), (29.0, 24.8), (33.2, 20.6), (33.2, 45.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(12.2, 41.6), (8.0, 45.8), (8.0, 20.6), (12.2, 24.8)], style=fill_style(GCP_TECH_MID))
polygon([(12.2, 24.8), (8.0, 20.6), (33.2, 20.6), (29.0, 24.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(12.2, 41.6), (29.0, 41.6), (29.0, 24.8), (12.2, 24.8)], style=fill_style(WHITE))
polygon([(58.4, 41.6), (62.6, 45.8), (37.4, 45.8), (41.6, 41.6)], style=fill_style(GCP_TECH_LIGHT))
polygon([(58.4, 41.6), (58.4, 24.8), (62.6, 20.6), (62.6, 45.8)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(41.6, 41.6), (37.4, 45.8), (37.4, 20.6), (41.6, 24.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(41.6, 24.8), (37.4, 20.6), (62.6, 20.6), (58.4, 24.8)], style=fill_style(GCP_TECH_MID))
polygon([(41.6, 41.6), (58.4, 41.6), (58.4, 24.8), (41.6, 24.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(87.8, 41.6), (92.0, 45.8), (66.8, 45.8), (71.0, 41.6)], style=fill_style(GCP_TECH_LIGHT))
polygon([(87.8, 41.6), (87.8, 24.8), (92.0, 20.6), (92.0, 45.8)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(71.0, 41.6), (66.8, 45.8), (66.8, 20.6), (71.0, 24.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(71.0, 24.8), (66.8, 20.6), (92.0, 20.6), (87.8, 24.8)], style=fill_style(GCP_TECH_MID))
polygon([(71.0, 41.6), (87.8, 41.6), (87.8, 24.8), (71.0, 24.8)], style=fill_style(GCP_TECH_LIGHT))
save()
# fmt: on
