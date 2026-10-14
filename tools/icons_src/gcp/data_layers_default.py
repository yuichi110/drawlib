# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: data_layers (default variant)."""

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
polygon([(46.77, 84.03), (53.23, 84.03), (53.23, 64.04), (46.77, 64.04)], style=fill_style(GCP_TECH_LIGHT))
draw_compound_polygon([[(50.0, 12.09), (8.0, 40.01), (50.0, 67.92), (92.0, 40.01)], [(19.85, 40.01), (50.0, 19.85), (80.15, 40.01), (50.0, 60.17)]], color=GCP_TECH_MED_LIGHT)
draw_compound_polygon([[(50.0, 32.08), (8.0, 59.99), (50.0, 87.91), (92.0, 59.99)], [(19.85, 59.99), (50.0, 39.83), (80.15, 59.99), (50.0, 80.15)]], color=GCP_TECH_LIGHT)
polygon([(76.97, 50.0), (50.0, 67.92), (23.03, 50.0), (50.0, 32.08)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
