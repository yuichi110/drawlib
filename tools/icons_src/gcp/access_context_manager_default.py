# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: access_context_manager (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(50.0, 19.47), (19.42, 50.0), (50.0, 80.58), (65.29, 65.29), (71.0, 71.0), (50.0, 92.0), (8.0, 50.0), (50.0, 8.0), (71.0, 29.0), (65.29, 34.71)], style=fill_style(GCP_TECH_LIGHT))
polygon([(76.71, 65.29), (92.0, 50.0), (76.71, 34.71)], style=fill_style(GCP_TECH_MID))
polygon([(50.0, 65.29), (65.29, 50.0), (50.0, 34.71)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
