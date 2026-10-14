# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: administration (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    GCP_TECH_DARK,
    GCP_TECH_LIGHT,
    GCP_TECH_MED_LIGHT,
    draw_compound_polygon,
    fill_style,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(8.0, 92.0), (8.0, 8.0), (50.0, 8.0), (50.0, 92.0)], [(26.0, 68.0), (17.2, 68.0), (17.2, 77.2), (26.0, 77.2)], [(26.0, 53.2), (17.2, 53.2), (17.2, 62.0), (26.0, 62.0)], [(26.0, 38.0), (17.2, 38.0), (17.2, 46.8), (26.0, 46.8)], [(26.0, 22.8), (17.2, 22.8), (17.2, 31.6), (26.0, 31.6)], [(41.2, 68.0), (32.0, 68.0), (32.0, 77.2), (40.8, 77.2), (40.8, 68.0)], [(41.2, 53.2), (32.0, 53.2), (32.0, 62.0), (40.8, 62.0), (40.8, 53.2)], [(41.2, 38.0), (32.0, 38.0), (32.0, 46.8), (40.8, 46.8), (40.8, 38.0)], [(41.2, 22.8), (32.0, 22.8), (32.0, 31.6), (40.8, 31.6), (40.8, 22.8)]], color=GCP_TECH_LIGHT)
draw_compound_polygon([[(29.2, 92.0), (29.2, 8.0), (50.0, 8.0), (50.0, 92.0)], [(41.2, 68.0), (32.0, 68.0), (32.0, 77.2), (40.8, 77.2), (40.8, 68.0)], [(41.2, 53.2), (32.0, 53.2), (32.0, 62.0), (40.8, 62.0), (40.8, 53.2)], [(41.2, 38.0), (32.0, 38.0), (32.0, 46.8), (40.8, 46.8), (40.8, 38.0)], [(41.2, 22.8), (32.0, 22.8), (32.0, 31.6), (40.8, 31.6), (40.8, 22.8)]], color=GCP_TECH_MED_LIGHT)
draw_compound_polygon([[(50.0, 56.0), (50.0, 8.0), (92.0, 8.0), (92.0, 56.0)], [(68.0, 38.0), (59.2, 38.0), (59.2, 46.8), (68.0, 46.8)], [(68.0, 22.8), (59.2, 22.8), (59.2, 31.6), (68.0, 31.6)], [(82.8, 38.0), (74.0, 38.0), (74.0, 46.8), (82.8, 46.8)], [(82.8, 22.8), (74.0, 22.8), (74.0, 31.6), (82.8, 31.6)]], color=GCP_TECH_LIGHT)
draw_compound_polygon([[(70.8, 56.0), (70.8, 8.0), (91.6, 8.0), (91.6, 56.0)], [(82.8, 38.0), (74.0, 38.0), (74.0, 46.8), (82.8, 46.8)], [(82.8, 22.8), (74.0, 22.8), (74.0, 31.6), (82.8, 31.6)]], color=GCP_TECH_MED_LIGHT)
polygon([(50.0, 65.2), (92.0, 65.2), (92.0, 56.4), (50.0, 56.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(50.0, 56.0), (92.0, 56.0), (92.0, 52.8), (50.0, 52.8)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(50.0, 65.2), (53.2, 65.2), (53.2, 56.4), (50.0, 56.4)], style=fill_style(GCP_TECH_DARK))
polygon([(50.0, 56.0), (53.2, 56.0), (53.2, 8.0), (50.0, 8.0)], style=fill_style(GCP_TECH_DARK))
save()
# fmt: on
