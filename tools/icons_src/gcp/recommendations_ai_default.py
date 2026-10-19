# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: recommendations_ai (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 92.0), (92.0, 92.0), (92.0, 50.0), (50.0, 50.0)], holes=[[(68.73, 63.61), (80.66, 75.49), (77.3, 78.85), (68.9, 70.45), (64.7, 74.65), (61.34, 71.29)]], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(8.0, 41.6), (8.0, 8.0), (41.6, 8.0), (41.6, 41.6)], holes=[[(33.2, 16.4), (16.4, 16.4), (16.4, 33.2), (33.2, 33.2)]], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(50.0, 50.0), (92.0, 50.0), (92.0, 58.27), (58.4, 58.4)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(83.6, 83.6), (83.6, 58.32), (92.0, 50.0), (92.0, 92.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(41.6, 8.0), (33.2, 16.4), (33.2, 33.2), (41.6, 41.6)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(8.0, 8.0), (16.4, 16.4), (33.2, 16.4), (41.6, 8.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(8.0, 83.6), (8.0, 50.0), (41.6, 50.0), (41.6, 83.6)], holes=[[(33.2, 58.4), (16.4, 58.4), (16.4, 75.2), (33.2, 75.2)]], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(41.6, 50.0), (33.2, 58.4), (33.2, 75.2), (41.6, 83.6)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(8.0, 50.0), (16.4, 58.4), (33.2, 58.4), (41.6, 50.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(50.0, 41.6), (50.0, 8.0), (83.6, 8.0), (83.6, 41.6)], holes=[[(75.2, 16.4), (58.4, 16.4), (58.4, 33.2), (75.2, 33.2)]], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(83.6, 8.0), (75.2, 16.4), (75.2, 33.2), (83.6, 41.6)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(50.0, 8.0), (58.4, 16.4), (75.2, 16.4), (83.6, 8.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
