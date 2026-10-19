# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: workload_identity_pool (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
# Outer rounded card frame
polygon([(15.5, 79.4), (84.5, 79.4), (86.14, 79.24), (87.72, 78.76), (89.16, 77.98), (90.44, 76.94), (91.48, 75.66), (92.26, 74.22), (92.74, 72.64), (92.9, 71.0), (92.9, 29.0), (92.74, 27.36), (92.26, 25.78), (91.48, 24.34), (90.44, 23.06), (89.16, 22.02), (87.72, 21.24), (86.14, 20.76), (84.5, 20.6), (15.5, 20.6), (13.86, 20.76), (12.28, 21.24), (10.84, 22.02), (9.56, 23.06), (8.52, 24.34), (7.74, 25.78), (7.26, 27.36), (7.1, 29.0), (7.1, 71.0), (7.26, 72.64), (7.74, 74.22), (8.52, 75.66), (9.56, 76.94), (10.84, 77.98), (12.28, 78.76), (13.86, 79.24)], holes=[[(14.6, 71.9), (85.4, 71.9), (85.4, 28.1), (14.6, 28.1)]], style=Icon.fill_style(Gcp.TECH_MID))
# 4 right-side horizontal bars
polygon([(59.4, 66.2), (78.6, 66.2), (78.6, 63.0), (59.4, 63.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(59.4, 56.4), (78.6, 56.4), (78.6, 53.2), (59.4, 53.2)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(59.4, 46.8), (78.6, 46.8), (78.6, 43.6), (59.4, 43.6)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(59.4, 37.0), (78.6, 37.0), (78.6, 33.8), (59.4, 33.8)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
# Light-blue chip outer ring + 8 pins (2 per side)
polygon([(24.2, 62.8), (50.0, 62.8), (50.0, 37.2), (24.2, 37.2)], holes=[[(27.4, 59.6), (46.8, 59.6), (46.8, 40.4), (27.4, 40.4)]], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(30.7, 66.2), (33.9, 66.2), (33.9, 62.8), (30.7, 62.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(40.3, 66.2), (43.5, 66.2), (43.5, 62.8), (40.3, 62.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(30.7, 37.2), (33.9, 37.2), (33.9, 33.8), (30.7, 33.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(40.3, 37.2), (43.5, 37.2), (43.5, 33.8), (40.3, 33.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(20.8, 56.4), (24.2, 56.4), (24.2, 53.2), (20.8, 53.2)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(20.8, 46.8), (24.2, 46.8), (24.2, 43.6), (20.8, 43.6)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(50.0, 56.4), (53.4, 56.4), (53.4, 53.2), (50.0, 53.2)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(50.0, 46.8), (53.4, 46.8), (53.4, 43.6), (50.0, 43.6)], style=Icon.fill_style(Gcp.TECH_LIGHT))
# Inner hollow blue core square
polygon([(30.7, 56.4), (43.5, 56.4), (43.5, 43.6), (30.7, 43.6)], holes=[[(33.9, 53.2), (40.3, 53.2), (40.3, 46.8), (33.9, 46.8)]], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
