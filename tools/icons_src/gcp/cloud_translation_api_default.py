# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_translation_api (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MED_LIGHT, GCP_TECH_MID, draw_compound_polygon, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(74.82, 57.56), (67.18, 57.56), (50.0, 12.2), (57.64, 12.2), (61.84, 23.54), (79.99, 23.54), (84.19, 12.2), (92.0, 12.2)], [(64.78, 31.1), (71.0, 47.48), (77.22, 31.1)]], color=GCP_TECH_MID)
polygon([(53.32, 38.37), (43.62, 47.86), (46.73, 51.52), (49.58, 55.4), (52.13, 59.48), (54.37, 63.74), (56.3, 68.14), (57.9, 72.68), (69.11, 72.68), (69.11, 80.24), (42.36, 80.24), (42.36, 87.8), (34.71, 87.8), (34.71, 80.24), (8.0, 80.24), (8.0, 72.72), (50.63, 72.72), (49.2, 69.03), (47.52, 65.45), (45.6, 61.99), (43.46, 58.66), (41.1, 55.49), (38.53, 52.48), (36.85, 54.42), (35.24, 56.43), (33.73, 58.5), (32.3, 60.64), (30.96, 62.83), (29.71, 65.08), (22.07, 65.08), (23.59, 61.98), (25.27, 58.96), (27.1, 56.03), (29.07, 53.2), (31.19, 50.47), (33.45, 47.86), (14.05, 29.0), (19.47, 23.54), (38.53, 42.44), (50.42, 30.68)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
