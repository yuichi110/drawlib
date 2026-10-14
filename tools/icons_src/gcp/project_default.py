# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: project (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_DARK, GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(8.38, 72.41), (19.3, 91.62), (41.15, 91.62), (52.07, 72.41), (41.15, 53.58), (19.3, 53.58)], style=fill_style(GCP_TECH_LIGHT))
polygon([(48.3, 65.63), (37.38, 84.84), (41.15, 92.0), (52.07, 72.41)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(15.53, 59.61), (37.38, 59.61), (44.91, 72.41), (48.3, 65.63), (41.15, 53.58), (19.3, 53.2)], style=fill_style(GCP_TECH_DARK))
polygon([(47.55, 49.81), (58.85, 69.02), (80.7, 69.02), (91.62, 49.81), (80.7, 30.98), (58.85, 30.98)], style=fill_style(GCP_TECH_LIGHT))
polygon([(87.86, 43.03), (76.93, 62.24), (80.7, 69.4), (91.62, 49.81)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(55.09, 37.0), (76.93, 37.0), (84.47, 49.81), (87.86, 43.03), (80.7, 30.98), (58.85, 30.6)], style=fill_style(GCP_TECH_DARK))
polygon([(8.38, 27.21), (19.3, 46.42), (41.15, 46.42), (52.07, 27.21), (41.15, 8.38), (19.3, 8.38)], style=fill_style(GCP_TECH_LIGHT))
polygon([(48.3, 20.43), (37.38, 39.64), (41.15, 46.8), (52.07, 27.21)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(15.53, 14.4), (37.38, 14.4), (44.91, 27.21), (48.3, 20.43), (41.15, 8.38), (19.3, 8.0)], style=fill_style(GCP_TECH_DARK))
save()
# fmt: on
