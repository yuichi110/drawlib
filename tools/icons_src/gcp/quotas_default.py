# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: quotas (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(24.8, 92.0), (16.4, 92.0), (16.4, 13.96), (16.38, 13.51), (16.39, 13.06), (16.45, 12.61), (16.54, 12.17), (16.67, 11.74), (16.83, 11.31), (17.03, 10.91), (17.26, 10.52), (17.52, 10.15), (17.81, 9.8), (18.12, 9.48), (18.47, 9.19), (18.83, 8.92), (19.22, 8.69), (19.62, 8.48), (20.04, 8.32), (20.47, 8.18), (20.92, 8.08), (21.36, 8.02), (21.81, 8.0), (78.26, 8.0), (78.69, 8.02), (79.12, 8.08), (79.53, 8.17), (79.95, 8.29), (80.35, 8.44), (80.73, 8.62), (81.1, 8.84), (81.46, 9.08), (81.79, 9.35), (82.1, 9.65), (82.38, 9.97), (82.64, 10.31), (82.88, 10.67), (83.08, 11.05), (83.25, 11.44), (83.39, 11.84), (83.5, 12.26), (83.57, 12.68), (83.62, 13.11), (83.62, 13.54), (83.6, 13.96), (83.6, 92.0), (75.2, 91.41), (75.2, 16.4), (24.8, 16.4)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(50.0, 8.0), (78.26, 8.0), (78.69, 8.02), (79.12, 8.08), (79.53, 8.17), (79.95, 8.29), (80.35, 8.44), (80.73, 8.62), (81.1, 8.84), (81.46, 9.08), (81.79, 9.35), (82.1, 9.65), (82.38, 9.97), (82.64, 10.31), (82.88, 10.67), (83.08, 11.05), (83.25, 11.44), (83.39, 11.84), (83.5, 12.26), (83.57, 12.68), (83.62, 13.11), (83.62, 13.54), (83.6, 13.96), (83.6, 92.0), (75.2, 92.0), (75.2, 16.4), (50.0, 16.4)], style=fill_style(GCP_TECH_MID))
polygon([(29.0, 50.0), (71.0, 50.0), (71.0, 20.6), (29.0, 20.6)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(50.0, 50.0), (71.0, 50.0), (71.0, 20.6), (50.0, 20.6)], style=fill_style(GCP_TECH_MID))
polygon([(29.0, 87.8), (33.2, 87.8), (33.2, 75.2), (29.0, 75.2)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(31.1, 87.8), (33.2, 87.8), (33.2, 75.2), (31.1, 75.2)], style=fill_style(GCP_TECH_MID))
polygon([(41.6, 87.8), (45.8, 87.8), (45.8, 75.2), (41.6, 75.2)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(54.2, 87.8), (58.4, 87.8), (58.4, 75.2), (54.2, 75.2)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(66.8, 87.8), (71.0, 87.8), (71.0, 75.2), (66.8, 75.2)], style=fill_style(GCP_TECH_MED_LIGHT))
polygon([(43.7, 87.8), (45.8, 87.8), (45.8, 75.2), (43.7, 75.2)], style=fill_style(GCP_TECH_MID))
polygon([(56.3, 87.8), (58.4, 87.8), (58.4, 75.2), (56.3, 75.2)], style=fill_style(GCP_TECH_MID))
polygon([(68.9, 87.8), (71.0, 87.8), (71.0, 75.2), (68.9, 75.2)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
