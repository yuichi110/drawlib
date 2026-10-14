# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: automl_translation (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(62.6, 57.06), (63.27, 57.06), (63.27, 57.73), (63.27, 60.54), (63.27, 61.26), (62.6, 61.26), (52.1, 61.26), (52.1, 65.37), (52.1, 66.04), (51.43, 66.04), (48.15, 66.04), (47.48, 66.04), (47.48, 65.37), (47.48, 61.26), (37.36, 61.26), (36.64, 61.26), (36.64, 60.54), (36.64, 57.73), (36.64, 57.06), (37.36, 57.06)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(63.99, 38.45), (62.07, 39.02), (60.21, 39.73), (58.39, 40.56), (56.64, 41.52), (54.96, 42.59), (53.36, 43.78), (54.42, 45.09), (55.4, 46.46), (56.29, 47.89), (57.09, 49.38), (57.79, 50.91), (58.4, 52.48), (53.4, 52.48), (52.96, 51.49), (52.46, 50.53), (51.91, 49.6), (51.32, 48.69), (50.68, 47.82), (50.0, 46.98), (49.31, 47.81), (48.67, 48.68), (48.08, 49.59), (47.53, 50.53), (47.04, 51.49), (46.6, 52.48), (41.6, 52.48), (42.31, 50.92), (43.09, 49.4), (43.95, 47.92), (44.88, 46.48), (45.87, 45.08), (46.93, 43.74), (45.31, 42.44), (43.6, 41.27), (41.8, 40.23), (39.93, 39.32), (38.0, 38.56), (36.01, 37.95), (38.53, 33.75), (40.61, 34.55), (42.63, 35.49), (44.59, 36.56), (46.47, 37.75), (48.28, 39.05), (50.0, 40.47), (51.69, 39.02), (53.49, 37.72), (55.39, 36.56), (57.38, 35.56), (59.43, 34.72), (61.55, 34.04)], style=fill_style(GCP_TECH_LIGHT))
polygon([(28.24, 18.67), (32.23, 11.74), (72.09, 11.74), (92.0, 46.26), (84.02, 60.08), (64.11, 25.6), (32.23, 25.6)], style=fill_style(GCP_TECH_MID))
polygon([(71.76, 81.33), (67.77, 88.26), (27.91, 88.26), (8.0, 53.74), (15.98, 39.92), (35.89, 74.4), (67.77, 74.4)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
