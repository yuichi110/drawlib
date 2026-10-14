# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_composer (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(41.73, 75.37), (19.26, 75.37), (19.26, 92.0), (80.7, 92.0), (80.7, 75.45), (58.44, 75.45), (58.44, 53.07), (41.73, 53.07)], style=fill_style(GCP_TECH_LIGHT))
polygon([(19.26, 69.45), (35.85, 69.45), (35.85, 47.19), (58.27, 47.19), (58.27, 8.0), (41.73, 8.0), (41.73, 30.47), (19.26, 30.47)], style=fill_style(GCP_TECH_MID))
polygon([(64.2, 69.49), (80.74, 69.49), (80.74, 8.0), (64.2, 8.0)], style=fill_style(GCP_TECH_MID))
polygon([(35.72, 8.0), (19.26, 8.0), (19.26, 24.55), (35.72, 24.55)], style=fill_style(GCP_TECH_LIGHT))
save()
# fmt: on
