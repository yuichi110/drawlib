# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: cerbos (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 91.0), (83.98, 74.75), (83.98, 48.15), (83.53, 42.19), (82.22, 36.71), (80.13, 31.69), (77.34, 27.14), (73.92, 23.04), (69.94, 19.38), (65.48, 16.15), (60.63, 13.36), (55.44, 10.97), (50.0, 9.0), (44.56, 10.97), (39.37, 13.36), (34.52, 16.15), (30.06, 19.38), (26.08, 23.04), (22.66, 27.14), (19.87, 31.69), (17.78, 36.71), (16.47, 42.19), (16.02, 48.15), (16.02, 74.75)], style=Icon.fill_style('#1D4ED8'))
Icon.draw_round_polyline([(60.34, 64.41), (56.41, 66.43), (52.08, 67.32), (47.67, 67.02), (43.51, 65.53), (39.9, 62.98), (37.11, 59.55), (35.35, 55.49), (34.75, 51.11), (35.35, 46.73), (37.11, 42.67), (39.9, 39.24), (43.51, 36.69), (47.67, 35.2), (52.08, 34.89), (56.41, 35.78), (60.34, 37.81), (60.34, 64.41)], width_units=6.91, color='#FFFFFF')
polygon([(65.51, 51.11), (65.41, 50.1), (65.12, 49.13), (64.64, 48.24), (64.0, 47.45), (63.22, 46.81), (62.32, 46.33), (61.35, 46.04), (60.34, 45.94), (59.33, 46.04), (58.36, 46.33), (57.47, 46.81), (56.69, 47.45), (56.04, 48.24), (55.56, 49.13), (55.27, 50.1), (55.17, 51.11), (55.27, 52.12), (55.56, 53.09), (56.04, 53.98), (56.69, 54.76), (57.47, 55.41), (58.36, 55.89), (59.33, 56.18), (60.34, 56.28), (61.35, 56.18), (62.32, 55.89), (63.22, 55.41), (64.0, 54.76), (64.64, 53.98), (65.12, 53.09), (65.41, 52.12)], style=Icon.fill_style('#38BDF8'))
save()
# fmt: on
