# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: key_access_justifications (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line, lines
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, setup_icon, stroke_style

# ruff: noqa: E501
# fmt: off
setup_icon()
line((52.2, 87.97), (52.2, 78.46), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
line((28.79, 78.26), (35.52, 71.57), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
line((19.12, 54.85), (28.59, 54.85), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
line((52.2, 21.74), (52.2, 31.21), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
line((75.64, 31.45), (68.92, 38.14), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
line((85.31, 54.85), (75.84, 54.85), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
line((75.64, 78.26), (68.92, 71.57), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
line((25.85, 27.82), (32.05, 21.62), style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
lines([(36.36, 41.48), (14.69, 19.8), (22.46, 12.03)], style=stroke_style(GCP_TECH_LIGHT, width_units=8.06))
polygon([(68.75, 38.3), (67.4, 37.05), (65.96, 35.91), (64.43, 34.89), (62.83, 33.99), (61.16, 33.22), (59.44, 32.58), (57.67, 32.08), (55.86, 31.72), (54.04, 31.5), (52.2, 31.43), (50.36, 31.5), (48.54, 31.71), (46.74, 32.07), (44.97, 32.57), (43.24, 33.21), (41.57, 33.97), (39.97, 34.87), (38.44, 35.89), (36.99, 37.03), (35.64, 38.28), (34.39, 39.63), (33.26, 41.07), (32.23, 42.6), (31.34, 44.2), (30.57, 45.87), (29.93, 47.6), (29.43, 49.37), (29.07, 51.17), (28.85, 53.0), (28.78, 54.83), (28.85, 56.67), (29.07, 58.5), (29.43, 60.3), (29.93, 62.07), (30.57, 63.79), (31.34, 65.46), (32.23, 67.07), (33.26, 68.6), (34.39, 70.04), (35.64, 71.39), (36.99, 72.64), (38.44, 73.78), (39.97, 74.8), (41.57, 75.69), (43.24, 76.46), (44.97, 77.1), (46.74, 77.6), (48.54, 77.96), (50.36, 78.17), (52.2, 78.24), (54.04, 78.17), (55.86, 77.95), (57.67, 77.59), (59.44, 77.09), (61.16, 76.45), (62.83, 75.68), (64.43, 74.78), (65.96, 73.76), (67.4, 72.62), (68.75, 71.37), (70.0, 70.02), (71.14, 68.58), (72.16, 67.06), (73.06, 65.45), (73.83, 63.79), (74.47, 62.06), (74.97, 60.3), (75.32, 58.49), (75.54, 56.67), (75.61, 54.83), (75.54, 53.0), (75.32, 51.17), (74.97, 49.37), (74.47, 47.61), (73.83, 45.88), (73.06, 44.21), (72.16, 42.61), (71.14, 41.09), (70.0, 39.64)], style=stroke_style(GCP_TECH_MED_LIGHT, width_units=8.06))
lines([(40.71, 54.09), (47.84, 46.68), (63.72, 63.03)], style=stroke_style(GCP_TECH_MID, width_units=4.03))
save()
# fmt: on
