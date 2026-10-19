# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: traffic_director (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(37.4, 37.4), (37.02, 39.54), (36.46, 41.64), (35.74, 43.69), (34.84, 45.66), (33.78, 47.56), (32.57, 49.37), (31.21, 51.06), (29.72, 52.64), (28.1, 54.09), (26.37, 55.4), (24.53, 56.56), (22.6, 57.56), (20.6, 58.4), (20.6, 66.8), (23.21, 65.97), (25.75, 64.94), (28.2, 63.71), (30.54, 62.29), (32.77, 60.69), (34.86, 58.92), (36.8, 56.99), (38.58, 54.91), (40.19, 52.69), (41.62, 50.36), (42.87, 47.91), (43.91, 45.38), (44.75, 42.77), (45.38, 40.11), (45.8, 37.4)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(20.6, 71.0), (20.6, 54.2), (8.0, 62.6)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(45.8, 35.76), (45.8, 24.8), (37.4, 24.8), (37.4, 35.8)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(37.4, 79.4), (33.2, 79.4), (41.6, 92.0), (50.0, 79.4), (45.8, 79.4), (45.8, 24.8), (37.4, 24.8)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(79.4, 29.0), (79.4, 45.8), (92.0, 37.4)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(54.2, 64.2), (54.2, 75.2), (62.6, 75.2), (62.6, 64.2)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(62.6, 20.6), (66.8, 20.6), (58.4, 8.0), (50.0, 20.6), (54.2, 20.6), (54.2, 75.2), (62.6, 75.2)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(54.2, 75.2), (62.6, 75.2), (62.6, 64.99), (62.74, 62.96), (63.04, 60.95), (63.5, 58.96), (64.11, 57.02), (64.88, 55.13), (65.79, 53.31), (66.84, 51.57), (68.03, 49.91), (69.35, 48.36), (70.78, 46.91), (72.33, 45.58), (73.97, 44.38), (75.71, 43.31), (77.52, 42.38), (79.4, 41.6), (79.4, 33.2), (76.81, 34.02), (74.29, 35.04), (71.87, 36.26), (69.54, 37.66), (67.34, 39.25), (65.27, 41.0), (63.34, 42.92), (61.57, 44.98), (59.97, 47.17), (58.55, 49.49), (57.32, 51.91), (56.28, 54.42), (55.44, 57.0), (54.82, 59.64), (54.4, 62.33), (54.2, 65.04)], style=Icon.fill_style(Gcp.TECH_LIGHT))
save()
# fmt: on
