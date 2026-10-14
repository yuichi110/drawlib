# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_apis (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    GCP_TECH_LIGHT,
    GCP_TECH_MED_LIGHT,
    GCP_TECH_MID,
    draw_compound_polygon,
    fill_style,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(68.86, 50.0), (50.0, 31.14), (31.14, 50.0), (50.0, 68.86)], [(50.0, 37.78), (62.22, 50.0), (50.0, 62.22), (37.78, 50.0)]], color=GCP_TECH_MID)
polygon([(68.19, 37.32), (79.32, 37.32), (92.0, 50.0), (80.87, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(68.19, 62.68), (80.87, 50.0), (92.0, 50.0), (79.32, 62.68)], style=fill_style(GCP_TECH_LIGHT))
polygon([(31.81, 62.68), (20.68, 62.68), (8.0, 50.0), (19.13, 50.0)], style=fill_style(GCP_TECH_LIGHT))
polygon([(8.0, 50.0), (20.68, 37.32), (31.81, 37.32), (19.13, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(37.32, 79.32), (37.32, 68.19), (50.0, 80.87), (50.0, 92.0)], style=fill_style(GCP_TECH_LIGHT))
polygon([(50.0, 92.0), (50.0, 80.87), (62.68, 68.19), (62.68, 79.32)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(37.32, 31.81), (37.32, 20.68), (50.0, 8.0), (50.0, 19.13)], style=fill_style(GCP_TECH_LIGHT))
polygon([(50.0, 19.13), (50.0, 8.0), (62.68, 20.68), (62.68, 31.81)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
