# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: asset_inventory (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(42.31, 49.96), (50.13, 57.79), (57.96, 49.97), (50.14, 42.14)], style=fill_style(GCP_TECH_MID))
polygon([(75.29, 50.0), (74.98, 49.74), (58.74, 33.46), (54.18, 37.98), (66.24, 50.0), (41.64, 74.6), (41.64, 83.64), (41.94, 83.34)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(41.64, 74.6), (17.09, 50.0), (46.17, 20.88), (41.64, 16.36), (41.38, 16.66), (8.0, 50.0), (41.64, 83.64)], style=fill_style(GCP_TECH_LIGHT))
polygon([(58.36, 25.4), (58.36, 16.36), (58.1, 16.66), (24.71, 49.96), (41.26, 66.54), (45.82, 61.98), (33.76, 49.96)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(58.36, 25.4), (82.91, 49.96), (53.83, 79.08), (58.36, 83.64), (58.62, 83.34), (92.0, 49.96), (91.7, 49.7), (58.36, 16.36)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
