# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: container_registry (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(27.61, 87.8), (8.0, 76.21), (8.0, 23.79), (27.61, 12.2), (27.61, 22.28), (16.4, 28.92), (16.4, 71.08), (27.61, 77.72)], style=fill_style(GCP_TECH_LIGHT))
polygon([(38.79, 62.01), (50.0, 55.42), (61.21, 62.01), (61.21, 75.28), (50.0, 81.88), (38.79, 75.28)], style=fill_style(GCP_TECH_LIGHT))
polygon([(38.79, 75.28), (38.79, 62.01), (50.0, 55.42), (61.21, 62.01), (61.21, 75.28), (50.0, 68.65)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(50.0, 55.42), (61.21, 62.01), (61.21, 75.28), (50.0, 68.65)], style=fill_style(GCP_TECH_MID))
polygon([(52.81, 34.75), (63.99, 28.16), (75.2, 34.75), (75.2, 48.03), (63.99, 54.66), (52.81, 48.03)], style=fill_style(GCP_TECH_LIGHT))
polygon([(52.81, 48.03), (52.81, 34.75), (63.99, 28.16), (75.2, 34.75), (75.2, 48.03), (63.99, 41.39)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(63.99, 28.16), (75.2, 34.75), (75.2, 48.03), (63.99, 41.39)], style=fill_style(GCP_TECH_MID))
polygon([(24.8, 34.75), (36.01, 28.16), (47.19, 34.75), (47.19, 48.03), (36.01, 54.66), (24.8, 48.03)], style=fill_style(GCP_TECH_LIGHT))
polygon([(24.8, 48.03), (24.8, 34.75), (36.01, 28.16), (47.19, 34.75), (47.19, 48.03), (36.01, 41.39)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(36.01, 28.16), (47.19, 34.75), (47.19, 48.03), (36.01, 41.39)], style=fill_style(GCP_TECH_MID))
polygon([(8.0, 66.09), (8.0, 33.87), (16.4, 28.92), (16.4, 71.08)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 66.09), (16.4, 68.02), (16.4, 71.08)], style=fill_style(GCP_TECH_MID))
polygon([(16.4, 28.92), (16.4, 31.35), (8.0, 33.87)], style=fill_style(GCP_TECH_MID))
polygon([(72.39, 87.8), (72.39, 77.72), (83.6, 71.08), (83.6, 28.92), (72.39, 22.28), (72.39, 12.2), (92.0, 23.79), (92.0, 76.21)], style=fill_style(GCP_TECH_LIGHT))
polygon([(83.6, 28.92), (92.0, 33.87), (92.0, 66.09), (83.6, 71.08)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(83.6, 68.02), (92.0, 66.09), (83.6, 71.08)], style=fill_style(GCP_TECH_MID))
polygon([(83.6, 31.35), (83.6, 28.92), (92.0, 33.87)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
