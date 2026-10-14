# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: automl_video_intelligence (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(28.29, 18.67), (32.49, 11.74), (72.3, 11.74), (92.0, 46.26), (84.02, 60.08), (64.11, 25.6), (32.28, 25.6)], style=fill_style(GCP_TECH_MID))
polygon([(71.71, 81.33), (67.51, 88.26), (27.91, 88.26), (8.0, 53.74), (15.98, 39.92), (35.93, 74.4), (67.77, 74.4)], style=fill_style(GCP_TECH_MID))
polygon([(64.57, 58.44), (58.99, 54.28), (58.99, 45.55), (64.57, 41.35)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(44.92, 48.74), (43.32, 45.84), (39.5, 45.84), (41.89, 49.96), (39.5, 54.16), (43.32, 54.16), (44.92, 51.47), (55.42, 51.47), (55.42, 60.0), (46.89, 60.0), (48.7, 57.14), (51.85, 57.14), (51.85, 54.03), (46.72, 54.03), (42.9, 60.0), (35.43, 60.0), (35.43, 40.0), (42.9, 40.0), (46.72, 45.97), (51.85, 45.97), (51.85, 42.86), (48.7, 42.86), (46.89, 40.0), (55.42, 40.0), (55.42, 48.74)], style=fill_style(GCP_TECH_LIGHT))
save()
# fmt: on
