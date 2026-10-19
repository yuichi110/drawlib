# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: cerbos (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 90.0), (83.15, 74.14), (83.15, 48.2), (82.71, 42.38), (81.43, 37.03), (79.4, 32.14), (76.67, 27.7), (73.33, 23.69), (69.45, 20.12), (65.11, 16.98), (60.37, 14.25), (55.31, 11.93), (50.0, 10.0), (44.69, 11.93), (39.63, 14.25), (34.89, 16.98), (30.55, 20.12), (26.67, 23.69), (23.33, 27.7), (20.6, 32.14), (18.57, 37.03), (17.29, 42.38), (16.85, 48.2), (16.85, 74.14)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
Icon.draw_round_polyline([(60.09, 64.05), (56.26, 66.03), (52.03, 66.9), (47.73, 66.6), (43.66, 65.15), (40.14, 62.66), (37.42, 59.31), (35.7, 55.35), (35.12, 51.08), (35.7, 46.81), (37.42, 42.85), (40.14, 39.5), (43.66, 37.01), (47.73, 35.56), (52.03, 35.26), (56.26, 36.13), (60.09, 38.11), (60.09, 64.05)], width_units=6.5, color=Icon.DARK)
polygon([(65.14, 51.08), (65.04, 50.1), (64.75, 49.15), (64.28, 48.28), (63.66, 47.51), (62.89, 46.89), (62.02, 46.42), (61.07, 46.13), (60.09, 46.04), (59.11, 46.13), (58.16, 46.42), (57.29, 46.89), (56.52, 47.51), (55.9, 48.28), (55.43, 49.15), (55.14, 50.1), (55.05, 51.08), (55.14, 52.07), (55.43, 53.01), (55.9, 53.88), (56.52, 54.65), (57.29, 55.28), (58.16, 55.74), (59.11, 56.03), (60.09, 56.13), (61.07, 56.03), (62.02, 55.74), (62.89, 55.28), (63.66, 54.65), (64.28, 53.88), (64.75, 53.01), (65.04, 52.07)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
