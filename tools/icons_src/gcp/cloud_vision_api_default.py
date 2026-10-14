# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_vision_api (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(24.8, 50.0), (50.0, 29.04), (50.0, 16.4), (8.0, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(50.0, 29.04), (75.2, 50.0), (92.0, 50.0), (50.0, 16.4)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 50.0), (50.0, 83.6), (50.0, 70.96), (24.8, 50.0)], style=fill_style(GCP_TECH_LIGHT))
polygon([(50.0, 70.96), (75.2, 50.0), (92.0, 50.0), (50.0, 83.6)], style=fill_style(GCP_TECH_LIGHT))
polygon([(58.4, 50.0), (58.27, 48.54), (57.89, 47.13), (57.27, 45.8), (56.43, 44.6), (55.4, 43.57), (54.2, 42.73), (52.87, 42.11), (51.46, 41.73), (50.0, 41.6), (48.54, 41.73), (47.13, 42.11), (45.8, 42.73), (44.6, 43.57), (43.57, 44.6), (42.73, 45.8), (42.11, 47.13), (41.73, 48.54), (41.6, 50.0), (41.73, 51.46), (42.11, 52.87), (42.73, 54.2), (43.57, 55.4), (44.6, 56.43), (45.8, 57.27), (47.13, 57.89), (48.54, 58.27), (50.0, 58.4), (51.46, 58.27), (52.87, 57.89), (54.2, 57.27), (55.4, 56.43), (56.43, 55.4), (57.27, 54.2), (57.89, 52.87), (58.27, 51.46)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
