# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: firestore (default variant)."""

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
draw_compound_polygon([[(87.8, 45.8), (50.0, 62.6), (50.0, 45.8), (87.8, 29.0)], [(87.8, 75.2), (50.0, 92.0), (50.0, 75.2), (87.8, 58.4)]], color=GCP_TECH_MED_LIGHT)
polygon([(12.2, 75.2), (50.0, 92.0), (50.0, 75.2), (12.2, 58.4)], style=fill_style(GCP_TECH_LIGHT))
polygon([(12.2, 45.8), (50.0, 62.6), (50.0, 45.8), (12.2, 29.0)], style=fill_style(GCP_TECH_LIGHT))
polygon([(50.0, 24.8), (64.15, 31.1), (83.1, 22.7), (50.0, 8.0)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
