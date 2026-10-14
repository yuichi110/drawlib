# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: dialogflow (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(50.0, 49.78), (16.12, 66.72), (16.12, 38.09), (16.13, 37.92), (16.15, 37.75), (16.18, 37.58), (16.23, 37.41), (16.3, 37.25), (16.37, 37.09), (16.46, 36.95), (16.56, 36.8), (16.67, 36.67), (16.8, 36.55), (16.93, 36.44), (36.58, 24.79), (36.67, 24.74), (36.76, 24.68), (36.84, 24.61), (36.92, 24.54), (36.99, 24.46), (37.05, 24.37), (37.11, 24.28), (37.16, 24.19), (37.2, 24.09), (37.24, 23.99), (37.27, 23.88), (37.28, 23.78), (37.29, 23.67), (37.3, 23.57), (37.3, 8.7), (37.3, 8.64), (37.31, 8.59), (37.32, 8.53), (37.34, 8.47), (37.36, 8.42), (37.39, 8.37), (37.42, 8.32), (37.45, 8.27), (37.49, 8.23), (37.53, 8.19), (37.58, 8.15), (37.62, 8.12), (37.67, 8.09), (37.73, 8.06), (37.78, 8.04), (37.84, 8.02), (37.89, 8.01), (37.95, 8.0), (38.01, 8.0), (38.07, 8.0), (38.13, 8.01), (38.18, 8.02), (38.24, 8.04), (38.29, 8.06), (38.35, 8.08), (38.4, 8.11), (82.9, 36.44), (83.05, 36.54), (83.18, 36.65), (83.31, 36.78), (83.42, 36.91), (83.53, 37.05), (83.62, 37.2), (83.69, 37.36), (83.76, 37.53), (83.81, 37.69), (83.85, 37.87), (83.87, 38.04), (83.88, 38.22), (83.88, 66.72)], style=fill_style(GCP_TECH_MID))
polygon([(50.0, 58.25), (83.88, 75.19), (50.51, 91.87), (50.43, 91.91), (50.35, 91.94), (50.26, 91.97), (50.18, 91.99), (50.09, 92.0), (50.0, 92.0), (49.91, 92.0), (49.82, 91.99), (49.74, 91.97), (49.65, 91.94), (49.57, 91.91), (49.49, 91.87), (16.12, 75.19)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
