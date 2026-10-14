# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: error_reporting (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(29.0, 92.0), (8.0, 71.0), (8.0, 29.0), (29.0, 8.0), (50.0, 8.0), (39.5, 20.01), (34.25, 20.01), (20.01, 34.25), (20.01, 65.75), (34.25, 79.99), (39.5, 79.99), (50.0, 92.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(60.5, 92.0), (50.0, 79.99), (65.75, 79.99), (79.99, 65.75), (79.99, 34.25), (65.75, 20.01), (50.0, 20.01), (60.5, 8.0), (71.0, 8.0), (92.0, 29.0), (92.0, 71.0), (71.0, 92.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(50.0, 29.0), (39.5, 39.5), (50.0, 50.0), (39.5, 60.5), (50.0, 71.0), (39.5, 71.0), (29.0, 60.5), (29.0, 39.5), (39.5, 29.0)], style=fill_style(GCP_TECH_MID))
polygon([(60.5, 71.0), (50.0, 60.5), (60.5, 50.0), (50.0, 39.5), (60.5, 29.0), (71.0, 39.5), (71.0, 60.5)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
