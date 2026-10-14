# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: container_registries (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_LIGHT_BLUE, draw_compound_polygon, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(42.67, 53.84), (54.76, 61.18), (88.61, 48.43), (87.88, 50.83), (86.81, 53.1), (85.42, 55.19), (83.74, 57.05), (83.69, 57.28), (81.43, 59.16), (78.91, 60.68), (76.19, 61.8), (73.33, 62.51), (72.31, 68.39), (69.8, 73.81), (65.97, 78.39), (61.09, 81.83), (55.48, 83.9), (49.53, 84.44), (43.76, 83.83), (38.3, 81.83), (33.5, 78.57), (29.64, 74.23), (26.95, 69.09), (21.98, 67.87), (17.44, 65.52), (13.58, 62.16), (10.62, 57.99), (8.72, 53.24), (8.0, 48.18), (8.97, 42.52), (11.37, 37.3), (15.04, 32.88), (19.72, 29.55), (25.1, 27.54), (30.82, 26.99), (42.67, 26.99)], style=fill_style(AZURE_LIGHT_BLUE))
polygon([(54.99, 58.59), (55.04, 38.62), (91.95, 30.78), (91.95, 44.68)], style=fill_style("#767676"))
polygon([(54.99, 58.59), (45.01, 52.52), (45.01, 33.95), (55.04, 38.62)], style=fill_style("#999999"))
polygon([(71.84, 38.34), (75.2, 37.4), (75.2, 48.28), (71.84, 49.44)], style=fill_style("#A3A3A3"))
polygon([(68.48, 50.52), (65.12, 51.73), (65.12, 40.11), (68.48, 39.18)], style=fill_style("#A3A3A3"))
polygon([(78.56, 36.52), (81.83, 35.63), (81.92, 45.99), (78.56, 47.11)], style=fill_style("#A3A3A3"))
polygon([(58.45, 41.84), (61.81, 41.0), (61.81, 52.8), (58.45, 53.92)], style=fill_style("#A3A3A3"))
polygon([(88.59, 43.7), (85.23, 44.87), (85.23, 34.74), (88.59, 33.81)], style=fill_style("#A3A3A3"))
draw_compound_polygon([[(48.41, 38.94), (46.73, 37.96), (46.73, 51.17), (48.41, 52.06)], [(51.73, 53.97), (50.0, 52.85), (50.0, 40.02), (51.73, 40.95)]], color="#B3B3B3")
polygon([(91.95, 30.78), (81.87, 27.32), (45.01, 33.95), (55.04, 38.62)], style=fill_style("#333132"))
polygon([(91.95, 16.54), (54.85, 9.5), (55.04, 35.58), (91.95, 28.72)], style=fill_style("#767676"))
polygon([(58.45, 13.79), (58.45, 30.36), (61.81, 29.94), (61.81, 14.35)], style=fill_style("#A3A3A3"))
polygon([(68.48, 15.47), (65.12, 14.86), (65.12, 29.52), (68.48, 29.0)], style=fill_style("#A3A3A3"))
polygon([(71.84, 15.98), (71.84, 28.68), (75.2, 28.26), (75.2, 16.59)], style=fill_style("#A3A3A3"))
polygon([(81.87, 17.76), (78.56, 17.15), (78.56, 27.84), (81.87, 27.32)], style=fill_style("#A3A3A3"))
polygon([(88.69, 18.83), (85.23, 18.22), (85.23, 27.0), (88.45, 26.58)], style=fill_style("#A3A3A3"))
polygon([(45.01, 15.47), (45.01, 30.68), (55.09, 35.35), (55.09, 9.21)], style=fill_style("#999999"))
draw_compound_polygon([[(48.18, 15.52), (46.69, 16.26), (46.69, 29.14), (48.18, 29.84)], [(51.77, 31.62), (50.0, 30.73), (50.0, 14.49), (51.73, 13.6), (51.73, 31.62)]], color="#B3B3B3")
save()
# fmt: on
