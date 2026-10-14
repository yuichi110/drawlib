# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: producer_portal (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_DARK, GCP_TECH_MED_LIGHT, draw_compound_polygon, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(12.5, 77.56), (87.5, 77.56), (87.5, 86.56), (12.5, 86.56)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(78.12, 13.44), (87.5, 13.44), (87.5, 41.19), (78.12, 41.19)], style=fill_style(GCP_TECH_DARK))
polygon([(50.0, 41.19), (50.0, 22.81), (21.88, 22.81), (21.88, 41.19), (12.5, 41.19), (12.5, 13.44), (59.38, 13.44), (59.38, 41.19)], style=fill_style(GCP_TECH_DARK))
draw_compound_polygon([[(12.5, 73.06), (8.0, 50.19), (8.0, 41.19), (12.5, 41.19), (59.38, 41.19), (78.12, 41.19), (87.5, 41.19), (92.0, 41.19), (92.0, 50.19), (87.5, 73.06)], [(20.38, 64.06), (80.0, 64.06), (82.62, 50.19), (17.38, 50.19)]], color=GCP_TECH_MED_LIGHT)
save()
# fmt: on
