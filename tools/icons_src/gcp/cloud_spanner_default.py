# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_spanner (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(55.63, 46.81), (55.63, 65.12), (44.37, 65.12), (44.37, 46.81), (28.54, 37.65), (34.17, 27.91), (50.0, 37.06), (65.83, 27.91), (71.46, 37.65)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(55.63, 46.81), (55.63, 65.12), (50.0, 65.12), (50.0, 43.62), (31.35, 32.78), (34.17, 27.91), (50.0, 37.06), (65.83, 27.91), (71.46, 37.65)], style=fill_style(GCP_TECH_MID))
polygon([(44.33, 88.77), (35.8, 83.64), (35.8, 67.98), (50.0, 60.29), (50.0, 73.35), (44.33, 75.96)], style=fill_style(GCP_TECH_LIGHT))
polygon([(55.67, 75.96), (50.0, 73.35), (50.0, 60.29), (64.2, 67.98), (64.2, 83.64), (55.67, 88.77)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(75.79, 28.66), (75.45, 22.83), (86.79, 16.4), (77.64, 11.36), (64.03, 19.21), (64.49, 35.3), (78.22, 43.7), (92.0, 35.8), (92.0, 25.35), (80.7, 31.86)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(24.21, 28.66), (19.3, 31.86), (8.0, 25.35), (8.0, 35.8), (21.57, 43.66), (35.3, 35.26), (35.76, 19.17), (22.36, 11.23), (13.21, 16.4), (24.55, 22.95)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(92.0, 25.35), (91.79, 35.8), (78.22, 43.62), (64.49, 35.17), (75.79, 28.66), (80.66, 31.86)], style=fill_style(GCP_TECH_LIGHT))
polygon([(8.0, 25.35), (19.34, 31.86), (24.21, 28.66), (35.51, 35.17), (21.78, 43.62), (8.21, 35.8)], style=fill_style(GCP_TECH_LIGHT))
save()
# fmt: on
