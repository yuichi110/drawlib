# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: debugger (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_DARK, GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(23.6, 47.2), (39.6, 47.2), (39.6, 52.8), (23.6, 52.8)], style=fill_style(GCP_TECH_DARK))
polygon([(20.4, 16.4), (46.8, 42.8), (43.2, 46.4), (16.8, 20.0)], style=fill_style(GCP_TECH_DARK))
polygon([(18.0, 78.4), (44.4, 52.0), (48.0, 55.6), (21.6, 82.0)], style=fill_style(GCP_TECH_DARK))
polygon([(60.4, 47.2), (76.4, 47.2), (76.4, 52.8), (60.4, 52.8)], style=fill_style(GCP_TECH_DARK))
polygon([(53.2, 42.8), (78.4, 18.0), (82.0, 21.6), (57.2, 46.8)], style=fill_style(GCP_TECH_DARK))
polygon([(60.0, 56.0), (83.2, 79.6), (79.6, 83.2), (56.0, 60.0)], style=fill_style(GCP_TECH_DARK))
polygon([(8.0, 8.0), (26.0, 8.0), (26.0, 26.0), (8.0, 26.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(74.0, 8.0), (92.0, 8.0), (92.0, 26.0), (74.0, 26.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 74.0), (26.0, 74.0), (26.0, 92.0), (8.0, 92.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(74.0, 74.0), (92.0, 74.0), (92.0, 92.0), (74.0, 92.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(34.8, 34.8), (65.2, 34.8), (65.2, 65.2), (34.8, 65.2)], style=fill_style(GCP_TECH_LIGHT))
polygon([(8.0, 41.2), (26.0, 41.2), (26.0, 58.8), (8.0, 58.8)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(74.0, 41.2), (92.0, 41.2), (92.0, 58.8), (74.0, 58.8)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
