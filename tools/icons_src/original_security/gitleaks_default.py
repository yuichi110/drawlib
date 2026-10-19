# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: gitleaks (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(73.2, 90.0), (78.39, 89.18), (83.07, 86.79), (86.79, 83.07), (89.18, 78.39), (90.0, 73.2), (90.0, 26.8), (89.18, 21.61), (86.79, 16.93), (83.07, 13.21), (78.39, 10.82), (73.2, 10.0), (26.8, 10.0), (21.61, 10.82), (16.93, 13.21), (13.21, 16.93), (10.82, 21.61), (10.0, 26.8), (10.0, 73.2), (10.82, 78.39), (13.21, 83.07), (16.93, 86.79), (21.61, 89.18), (26.8, 90.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
Icon.draw_round_polyline([(55.6, 56.4), (55.32, 53.59), (54.5, 50.89), (53.17, 48.4), (51.38, 46.22), (49.2, 44.43), (46.71, 43.1), (44.01, 42.28), (41.2, 42.0), (38.39, 42.28), (35.69, 43.1), (33.2, 44.43), (31.02, 46.22), (29.23, 48.4), (27.9, 50.89), (27.08, 53.59), (26.8, 56.4), (27.08, 59.21), (27.9, 61.91), (29.23, 64.4), (31.02, 66.58), (33.2, 68.37), (35.69, 69.7), (38.39, 70.52), (41.2, 70.8), (44.01, 70.52), (46.71, 69.7), (49.2, 68.37), (51.38, 66.58), (53.17, 64.4), (54.5, 61.91), (55.32, 59.21), (55.6, 56.4)], width_units=6.12, color=Icon.DARK)
Icon.draw_round_polyline([(52.4, 46.8), (75.6, 23.6)], width_units=6.12, color=Icon.DARK)
Icon.draw_round_polyline([(67.6, 31.6), (74.8, 38.8)], width_units=6.12, color=Icon.DARK)
polygon([(41.2, 38.0), (40.95, 37.68), (40.28, 36.79), (39.3, 35.43), (38.1, 33.7), (36.8, 31.7), (35.5, 29.53), (34.3, 27.3), (33.32, 25.1), (32.65, 23.03), (32.4, 21.2), (32.57, 19.48), (33.07, 17.83), (33.88, 16.31), (34.98, 14.98), (36.31, 13.88), (37.83, 13.07), (39.48, 12.57), (41.2, 12.4), (42.92, 12.57), (44.57, 13.07), (46.09, 13.88), (47.42, 14.98), (48.52, 16.31), (49.33, 17.83), (49.83, 19.48), (50.0, 21.2), (49.75, 23.03), (49.08, 25.1), (48.1, 27.3), (46.9, 29.53), (45.6, 31.7), (44.3, 33.7), (43.1, 35.43), (42.12, 36.79), (41.45, 37.68)], style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
