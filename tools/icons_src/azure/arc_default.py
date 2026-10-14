# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: arc (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    AZURE_BLUE,
    AZURE_CYAN,
    AZURE_DARK_BLUE,
    AZURE_LIGHT_BLUE,
    AZURE_LIGHT_CYAN,
    AZURE_TEAL,
    draw_compound_polygon,
    fill_style,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(41.28, 71.14), (24.65, 61.47), (8.0, 71.15), (24.65, 80.82)], style=fill_style(AZURE_LIGHT_BLUE))
polygon([(41.28, 27.63), (24.64, 37.24), (24.64, 17.95)], style=fill_style(AZURE_DARK_BLUE))
polygon([(24.65, 61.47), (24.64, 61.48), (24.64, 61.47), (8.0, 71.15), (8.0, 27.6), (24.64, 17.92), (41.28, 27.6), (41.28, 27.63), (24.64, 17.95), (24.64, 37.24), (41.28, 27.63), (41.28, 71.14)], style=fill_style(AZURE_BLUE))
polygon([(58.72, 71.14), (75.35, 61.47), (92.0, 71.15), (75.35, 80.82)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(58.72, 27.63), (75.36, 37.24), (75.36, 17.95)], style=fill_style(AZURE_TEAL))
polygon([(75.35, 61.5), (75.36, 61.5), (75.36, 37.27), (58.72, 27.63), (58.72, 71.18)], style=fill_style(AZURE_TEAL))
polygon([(58.72, 71.14), (75.35, 61.47), (92.0, 71.15), (75.35, 80.82)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(75.35, 61.47), (58.72, 71.14), (58.72, 27.63), (75.36, 37.24), (75.36, 17.95), (58.72, 27.63), (58.72, 27.6), (75.36, 17.92), (92.0, 27.6), (92.0, 71.15)], style=fill_style(AZURE_CYAN))
polygon([(58.72, 27.63), (75.36, 37.24), (75.36, 17.95)], style=fill_style(AZURE_TEAL))
polygon([(75.35, 61.5), (75.36, 61.5), (75.36, 37.27), (58.72, 27.63), (58.72, 71.18)], style=fill_style(AZURE_TEAL))
polygon([(24.65, 61.48), (24.64, 61.48), (24.64, 37.24), (41.28, 27.6), (41.28, 71.14)], style=fill_style(AZURE_DARK_BLUE))
draw_compound_polygon([[(75.31, 44.75), (73.84, 42.14), (71.68, 39.8), (68.94, 37.74), (65.73, 35.99), (62.16, 34.59), (58.33, 33.55), (54.36, 32.91), (50.35, 32.69), (49.97, 32.69), (49.6, 32.69), (45.59, 32.91), (41.62, 33.55), (37.79, 34.59), (34.22, 35.99), (31.01, 37.74), (28.27, 39.8), (26.11, 42.14), (24.64, 44.75), (24.64, 45.06), (24.62, 45.89), (24.61, 47.09), (24.6, 48.48), (24.59, 49.9), (24.59, 51.19), (24.61, 52.19), (24.64, 52.74), (25.84, 49.81), (27.78, 47.12), (30.36, 44.71), (33.48, 42.65), (37.04, 40.96), (40.94, 39.7), (45.07, 38.91), (49.34, 38.64), (49.97, 38.64), (50.61, 38.64), (54.87, 38.91), (59.0, 39.7), (62.9, 40.96), (66.46, 42.65), (69.58, 44.71), (72.17, 47.12), (74.11, 49.81), (75.31, 52.74), (75.34, 52.19), (75.36, 51.19), (75.36, 49.9), (75.35, 48.48), (75.34, 47.09), (75.32, 45.89), (75.31, 45.06)], [(70.53, 64.27), (66.08, 61.27), (61.17, 59.09), (55.96, 57.78), (50.61, 57.39), (49.97, 57.39), (49.34, 57.39), (43.99, 57.78), (38.79, 59.08), (33.88, 61.26), (29.43, 64.25), (25.43, 61.92), (27.16, 59.64), (29.43, 57.6), (32.15, 55.81), (35.25, 54.3), (38.62, 53.08), (42.2, 52.19), (45.88, 51.64), (49.6, 51.45), (50.35, 51.45), (54.07, 51.64), (57.76, 52.19), (61.33, 53.09), (64.71, 54.3), (67.81, 55.82), (70.53, 57.62), (72.8, 59.67), (74.53, 61.95)]], color=AZURE_DARK_BLUE)
save()
# fmt: on
