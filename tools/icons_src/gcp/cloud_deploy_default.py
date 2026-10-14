# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_deploy (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(88.41, 21.39), (88.41, 68.49), (47.61, 92.0), (47.61, 70.56), (69.92, 57.82), (69.83, 32.11)], style=fill_style(GCP_TECH_MID))
polygon([(62.65, 13.93), (62.65, 53.63), (28.33, 73.46), (28.33, 54.97), (46.78, 44.43), (46.69, 23.18)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(39.51, 8.0), (39.51, 40.25), (11.59, 56.35), (11.59, 40.89), (26.17, 32.57), (26.08, 15.73)], style=fill_style(GCP_TECH_LIGHT))
save()
# fmt: on
