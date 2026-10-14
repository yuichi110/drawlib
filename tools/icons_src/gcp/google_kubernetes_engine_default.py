# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: google_kubernetes_engine (default variant)."""

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
polygon([(61.28, 45.55), (80.39, 34.5), (80.39, 30.34), (59.64, 42.31)], style=fill_style(GCP_TECH_MID))
polygon([(41.54, 43.07), (19.65, 30.43), (18.31, 33.79), (39.65, 46.14)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(48.13, 86.58), (51.74, 86.58), (51.74, 62.31), (48.13, 62.31)], style=fill_style(GCP_TECH_LIGHT))
draw_compound_polygon([[(13.27, 71.0), (13.27, 29.0), (50.02, 8.0), (86.73, 29.0), (86.73, 71.0), (50.02, 92.0)], [(78.92, 33.66), (50.02, 17.32), (21.12, 33.66), (21.12, 66.34), (50.02, 82.68), (78.88, 66.34), (78.88, 33.66)]], color=GCP_TECH_LIGHT)
polygon([(49.94, 52.1), (66.65, 61.72), (49.94, 71.38), (33.26, 61.72)], style=fill_style(GCP_TECH_LIGHT))
polygon([(48.0, 48.74), (31.79, 58.36), (31.79, 39.08), (48.0, 29.46)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(52.04, 48.74), (52.04, 29.46), (68.25, 39.08), (68.25, 58.36)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
