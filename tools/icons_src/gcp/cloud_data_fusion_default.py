# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_data_fusion (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(24.8, 66.8), (41.6, 66.8), (41.6, 83.6), (12.2, 83.6), (11.87, 83.59), (11.54, 83.55), (11.22, 83.48), (10.9, 83.39), (10.59, 83.28), (10.29, 83.14), (10.01, 82.98), (9.73, 82.8), (9.47, 82.59), (9.23, 82.37), (9.01, 82.13), (8.8, 81.87), (8.62, 81.59), (8.46, 81.31), (8.32, 81.01), (8.21, 80.7), (8.12, 80.38), (8.05, 80.06), (8.01, 79.73), (8.0, 79.4), (8.0, 12.2), (8.02, 11.85), (8.07, 11.5), (8.15, 11.16), (8.25, 10.82), (8.39, 10.5), (8.55, 10.19), (8.73, 9.89), (8.94, 9.61), (9.18, 9.34), (24.8, 24.8)], style=fill_style(GCP_TECH_LIGHT))
polygon([(66.8, 24.8), (82.42, 9.18), (82.65, 9.42), (82.85, 9.69), (83.03, 9.97), (83.18, 10.26), (83.32, 10.57), (83.42, 10.88), (83.51, 11.21), (83.56, 11.54), (83.6, 11.87), (83.6, 12.2), (83.6, 41.6), (66.8, 41.6)], style=fill_style(GCP_TECH_MID))
polygon([(90.78, 90.82), (75.2, 75.2), (75.2, 58.4), (92.0, 58.4), (92.0, 87.8), (91.99, 88.13), (91.96, 88.47), (91.9, 88.8), (91.81, 89.12), (91.7, 89.43), (91.56, 89.74), (91.4, 90.03), (91.21, 90.31), (91.01, 90.58)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(75.2, 75.2), (90.82, 90.82), (90.58, 91.05), (90.31, 91.25), (90.03, 91.43), (89.74, 91.58), (89.43, 91.72), (89.12, 91.82), (88.79, 91.91), (88.46, 91.96), (88.13, 92.0), (87.8, 92.0), (58.4, 92.0), (58.4, 75.2)], style=fill_style(GCP_TECH_LIGHT))
polygon([(8.0, 8.0), (24.8, 24.8), (66.8, 24.8), (83.6, 8.0)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
