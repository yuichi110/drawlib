# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: memorystore (default variant)."""

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
polygon([(8.0, 83.85), (21.99, 83.85), (21.99, 73.02), (8.0, 73.02)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 64.91), (21.99, 64.91), (21.99, 54.07), (8.0, 54.07)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 45.93), (21.99, 45.93), (21.99, 35.09), (8.0, 35.09)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(8.0, 26.98), (21.99, 26.98), (21.99, 16.15), (8.0, 16.15)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(78.01, 83.85), (92.0, 83.85), (92.0, 73.02), (78.01, 73.02)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(78.01, 64.91), (92.0, 64.91), (92.0, 54.07), (78.01, 54.07)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(78.01, 45.93), (92.0, 45.93), (92.0, 35.09), (78.01, 35.09)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(78.01, 26.98), (92.0, 26.98), (92.0, 16.15), (78.01, 16.15)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(89.19, 73.02), (78.01, 73.02), (78.01, 83.85)], style=fill_style(GCP_TECH_MID))
polygon([(89.19, 54.07), (78.01, 54.07), (78.01, 64.91)], style=fill_style(GCP_TECH_MID))
polygon([(89.19, 35.09), (78.01, 35.09), (78.01, 45.93)], style=fill_style(GCP_TECH_MID))
polygon([(89.19, 16.11), (78.01, 16.11), (78.01, 26.98)], style=fill_style(GCP_TECH_MID))
draw_compound_polygon([[(21.99, 8.0), (78.01, 8.0), (78.01, 92.0), (21.99, 92.0)], [(47.19, 45.8), (33.2, 45.8), (52.81, 78.31), (52.81, 54.2), (66.8, 54.2), (47.19, 21.69)]], color=GCP_TECH_LIGHT)
polygon([(47.19, 8.0), (47.19, 21.57), (66.8, 54.07), (52.81, 54.07), (52.81, 92.0), (78.01, 92.0), (78.01, 8.0)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
