# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_asset_inventory (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(58.47, 83.52), (54.41, 79.46), (83.95, 50.0), (58.47, 24.52), (33.0, 50.0), (45.17, 62.17), (41.15, 66.19), (24.96, 50.0), (58.47, 16.48), (92.0, 50.0)], style=fill_style(GCP_TECH_MID))
polygon([(50.18, 42.63), (42.81, 50.0), (50.18, 57.37), (57.54, 50.0)], style=fill_style(GCP_TECH_MID))
polygon([(41.52, 83.52), (8.0, 50.0), (41.52, 16.48), (45.54, 20.5), (16.05, 50.0), (41.52, 75.48), (66.99, 50.0), (54.83, 37.83), (58.85, 33.81), (75.04, 50.0)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
