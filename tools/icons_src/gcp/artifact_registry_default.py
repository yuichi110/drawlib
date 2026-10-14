# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: artifact_registry (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_DARK, GCP_TECH_MED_LIGHT, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(27.5, 86.94), (8.0, 75.69), (8.0, 24.31), (27.5, 13.06), (27.5, 22.81), (16.25, 29.19), (16.25, 70.81), (27.5, 77.19)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 65.94), (8.0, 34.06), (16.25, 29.19), (16.25, 70.81)], style=fill_style(GCP_TECH_DARK))
polygon([(8.0, 65.94), (16.25, 67.81), (16.25, 70.81)], style=fill_style(GCP_TECH_DARK))
polygon([(72.5, 86.94), (72.5, 77.19), (83.75, 70.81), (83.75, 29.19), (72.5, 22.81), (72.5, 13.06), (92.0, 24.31), (92.0, 75.69)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(83.75, 29.19), (92.0, 34.06), (92.0, 65.94), (83.75, 70.81)], style=fill_style(GCP_TECH_DARK))
polygon([(83.75, 67.81), (92.0, 65.94), (83.75, 70.81)], style=fill_style(GCP_TECH_DARK))
polygon([(83.75, 31.81), (83.75, 29.19), (92.0, 34.06)], style=fill_style(GCP_TECH_DARK))
polygon([(50.0, 75.31), (38.75, 69.31), (50.0, 63.31), (61.25, 69.31)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(51.5, 49.44), (62.38, 55.44), (62.38, 67.06), (51.5, 61.06)], style=fill_style(GCP_TECH_DARK))
polygon([(48.88, 61.06), (37.62, 67.06), (37.62, 55.44), (48.88, 49.44)], style=fill_style(GCP_TECH_DARK))
polygon([(37.1, 53.28), (26.22, 47.28), (37.1, 41.28), (47.6, 47.28)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(37.85, 27.4), (48.73, 33.4), (48.73, 45.4), (37.85, 39.4)], style=fill_style(GCP_TECH_DARK))
polygon([(35.97, 39.4), (25.1, 45.4), (25.1, 33.4), (35.97, 27.4)], style=fill_style(GCP_TECH_DARK))
polygon([(63.2, 53.28), (52.32, 47.28), (63.2, 41.28), (74.07, 47.28)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(64.32, 27.4), (75.2, 33.4), (75.2, 45.4), (64.32, 39.4)], style=fill_style(GCP_TECH_DARK))
polygon([(62.07, 39.4), (51.2, 45.4), (51.2, 33.4), (62.07, 27.4)], style=fill_style(GCP_TECH_DARK))
save()
# fmt: on
