# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: speech_to_text (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(45.8, 92.0), (54.2, 92.0), (54.2, 8.0), (45.8, 8.0)], style=fill_style(GCP_TECH_MID))
polygon([(29.0, 66.8), (37.4, 66.8), (37.4, 33.2), (29.0, 33.2)], style=fill_style(GCP_TECH_MID))
polygon([(62.6, 66.8), (71.0, 66.8), (71.0, 33.2), (62.6, 33.2)], style=fill_style(GCP_TECH_MID))
polygon([(12.2, 79.4), (20.6, 79.4), (20.6, 20.6), (12.2, 20.6)], style=fill_style(GCP_TECH_MID))
polygon([(79.4, 79.4), (87.8, 79.4), (87.8, 20.6), (79.4, 20.6)], style=fill_style(GCP_TECH_MID))
polygon([(45.8, 92.0), (54.2, 92.0), (54.2, 50.0), (45.8, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(29.0, 66.8), (37.4, 66.8), (37.4, 50.0), (29.0, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(62.6, 66.8), (71.0, 66.8), (71.0, 50.0), (62.6, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(12.2, 79.4), (20.6, 79.4), (20.6, 50.0), (12.2, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(79.4, 79.4), (87.8, 79.4), (87.8, 50.0), (79.4, 50.0)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
