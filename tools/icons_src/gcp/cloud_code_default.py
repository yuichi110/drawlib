# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_code (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(22.49, 64.59), (35.51, 77.66), (48.53, 64.59), (35.51, 51.49)], style=fill_style(GCP_TECH_LIGHT))
polygon([(8.0, 50.02), (21.02, 63.12), (34.04, 50.02), (21.02, 36.92)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(22.49, 35.45), (35.51, 48.55), (48.53, 35.45), (35.51, 22.34)], style=fill_style(GCP_TECH_MID))
polygon([(51.47, 64.59), (64.49, 77.66), (77.51, 64.59), (64.49, 51.49)], style=fill_style(GCP_TECH_LIGHT))
polygon([(65.96, 50.02), (78.98, 63.12), (92.0, 50.02), (78.98, 36.92)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(51.47, 35.45), (64.49, 48.55), (77.51, 35.45), (64.49, 22.34)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
