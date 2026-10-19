# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: quantum_engine (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(29.04, 92.0), (37.44, 92.0), (37.44, 79.4), (29.04, 79.4)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(45.84, 92.0), (54.24, 92.0), (54.24, 79.4), (45.84, 79.4)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(62.64, 92.0), (71.04, 92.0), (71.04, 79.4), (62.64, 79.4)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(29.04, 20.6), (37.44, 20.6), (37.44, 8.0), (29.04, 8.0)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(45.84, 20.6), (54.24, 20.6), (54.24, 8.0), (45.84, 8.0)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(62.64, 20.6), (71.04, 20.6), (71.04, 8.0), (62.64, 8.0)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(79.4, 37.4), (92.0, 37.4), (92.0, 29.0), (79.4, 29.0)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(79.4, 54.2), (92.0, 54.2), (92.0, 45.8), (79.4, 45.8)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(79.4, 71.0), (92.0, 71.0), (92.0, 62.6), (79.4, 62.6)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(8.0, 37.4), (20.6, 37.4), (20.6, 29.0), (8.0, 29.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(8.0, 54.2), (20.6, 54.2), (20.6, 45.8), (8.0, 45.8)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(8.0, 71.0), (20.6, 71.0), (20.6, 62.6), (8.0, 62.6)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(16.4, 16.4), (16.4, 83.6), (83.6, 83.6), (83.6, 16.4)], holes=[[(45.8, 45.8), (37.4, 45.8), (37.4, 71.0), (29.0, 71.0), (29.0, 37.4), (45.8, 37.4), (45.8, 24.8), (54.2, 24.8), (54.2, 37.4), (71.0, 37.4), (71.0, 71.0), (62.6, 71.0), (62.6, 45.8), (54.2, 45.8), (54.2, 75.2), (45.8, 75.2)]], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
