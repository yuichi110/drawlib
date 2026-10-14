# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: availability_sets (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    AZURE_BLUE,
    AZURE_CYAN,
    AZURE_LIGHT_CYAN,
    AZURE_LIGHT_GRAY,
    AZURE_PALE_CYAN,
    fill_style,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(17.89, 89.67), (27.09, 89.67), (27.09, 87.01), (17.89, 87.01)], style=fill_style(AZURE_BLUE))
polygon([(85.61, 87.01), (87.1, 87.01), (87.1, 85.56), (89.67, 85.56), (89.67, 89.67), (85.61, 89.67)], style=fill_style(AZURE_BLUE))
polygon([(14.58, 13.18), (13.27, 13.18), (13.27, 14.67), (10.33, 14.67), (10.33, 10.33), (14.58, 10.33)], style=fill_style(AZURE_BLUE))
polygon([(87.1, 14.53), (87.1, 13.18), (85.61, 13.18), (85.61, 10.33), (89.67, 10.33), (89.67, 14.53)], style=fill_style(AZURE_BLUE))
polygon([(13.27, 85.65), (13.27, 87.01), (14.58, 87.01), (14.58, 89.67), (10.33, 89.67), (10.33, 85.65)], style=fill_style(AZURE_BLUE))
polygon([(63.39, 75.43), (63.74, 75.39), (64.07, 75.25), (64.35, 75.04), (64.57, 74.76), (64.7, 74.43), (64.75, 74.08), (64.75, 49.35), (64.7, 49.0), (64.57, 48.67), (64.35, 48.39), (64.07, 48.17), (63.74, 48.04), (63.39, 47.99), (25.08, 47.99), (24.73, 48.04), (24.4, 48.17), (24.12, 48.39), (23.91, 48.67), (23.77, 49.0), (23.73, 49.35), (23.73, 74.08), (23.77, 74.43), (23.91, 74.76), (24.12, 75.04), (24.4, 75.25), (24.73, 75.39), (25.08, 75.43)], style=fill_style(AZURE_BLUE))
polygon([(51.07, 65.68), (51.07, 57.7), (44.26, 53.69), (44.26, 61.71)], style=fill_style(AZURE_CYAN))
polygon([(51.07, 65.68), (44.26, 61.67), (37.4, 65.68), (44.26, 69.69)], style=fill_style(AZURE_PALE_CYAN))
polygon([(44.26, 61.67), (44.26, 53.69), (37.4, 57.7), (37.4, 65.68)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(75.25, 60.13), (75.6, 60.08), (75.92, 59.95), (76.2, 59.73), (76.42, 59.45), (76.55, 59.12), (76.6, 58.77), (76.6, 34.04), (76.55, 33.69), (76.42, 33.36), (76.2, 33.08), (75.92, 32.87), (75.6, 32.73), (75.25, 32.69), (36.93, 32.69), (36.58, 32.73), (36.26, 32.87), (35.98, 33.08), (35.76, 33.36), (35.63, 33.69), (35.58, 34.04), (35.58, 58.77), (35.63, 59.12), (35.76, 59.45), (35.98, 59.73), (36.26, 59.95), (36.58, 60.08), (36.93, 60.13)], style=fill_style(AZURE_BLUE))
polygon([(62.93, 50.42), (62.93, 42.44), (56.11, 38.43), (56.11, 46.41)], style=fill_style(AZURE_CYAN))
polygon([(62.93, 50.42), (56.11, 46.41), (49.25, 50.42), (56.11, 54.43)], style=fill_style(AZURE_PALE_CYAN))
polygon([(56.11, 46.41), (56.11, 38.43), (49.25, 42.44), (49.25, 50.42)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(49.25, 42.44), (56.11, 46.41), (56.11, 38.43)], style=fill_style(AZURE_PALE_CYAN))
polygon([(62.93, 42.44), (56.11, 46.41), (56.11, 38.43)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(64.33, 24.43), (62.98, 24.78), (61.96, 25.34), (61.21, 26.1), (60.7, 27.06), (60.39, 28.21), (60.21, 29.54), (60.14, 31.05), (60.13, 32.73), (52.05, 32.73), (52.05, 31.06), (51.99, 29.56), (51.83, 28.23), (51.53, 27.07), (51.03, 26.11), (50.28, 25.34), (49.24, 24.78), (47.85, 24.43), (47.32, 24.28), (46.84, 24.01), (46.44, 23.65), (46.12, 23.19), (45.92, 22.68), (45.85, 22.14), (66.38, 22.14), (66.3, 22.69), (66.09, 23.21), (65.77, 23.66), (65.36, 24.03), (64.86, 24.29)], style=fill_style(AZURE_LIGHT_GRAY))
polygon([(31.66, 89.67), (40.85, 89.67), (40.85, 87.01), (31.66, 87.01)], style=fill_style(AZURE_BLUE))
polygon([(45.38, 89.67), (54.57, 89.67), (54.57, 87.01), (45.38, 87.01)], style=fill_style(AZURE_BLUE))
polygon([(59.15, 89.67), (68.34, 89.67), (68.34, 87.01), (59.15, 87.01)], style=fill_style(AZURE_BLUE))
polygon([(72.91, 89.67), (82.11, 89.67), (82.11, 87.01), (72.91, 87.01)], style=fill_style(AZURE_BLUE))
polygon([(17.99, 13.18), (27.18, 13.18), (27.18, 10.52), (17.99, 10.52)], style=fill_style(AZURE_BLUE))
polygon([(31.71, 13.18), (40.9, 13.18), (40.9, 10.52), (31.71, 10.52)], style=fill_style(AZURE_BLUE))
polygon([(45.47, 13.18), (54.67, 13.18), (54.67, 10.52), (45.47, 10.52)], style=fill_style(AZURE_BLUE))
polygon([(59.24, 13.18), (68.43, 13.18), (68.43, 10.52), (59.24, 10.52)], style=fill_style(AZURE_BLUE))
polygon([(72.96, 13.18), (82.15, 13.18), (82.15, 10.52), (72.96, 10.52)], style=fill_style(AZURE_BLUE))
polygon([(87.01, 82.43), (89.67, 82.43), (89.67, 73.24), (87.01, 73.24)], style=fill_style(AZURE_BLUE))
polygon([(87.01, 68.71), (89.67, 68.71), (89.67, 59.52), (87.01, 59.52)], style=fill_style(AZURE_BLUE))
polygon([(87.01, 54.95), (89.67, 54.95), (89.67, 45.75), (87.01, 45.75)], style=fill_style(AZURE_BLUE))
polygon([(87.01, 41.23), (89.67, 41.23), (89.67, 32.03), (87.01, 32.03)], style=fill_style(AZURE_BLUE))
polygon([(87.01, 27.46), (89.67, 27.46), (89.67, 18.27), (87.01, 18.27)], style=fill_style(AZURE_BLUE))
polygon([(10.33, 82.53), (12.99, 82.53), (12.99, 73.33), (10.33, 73.33)], style=fill_style(AZURE_BLUE))
polygon([(10.33, 68.76), (12.99, 68.76), (12.99, 59.57), (10.33, 59.57)], style=fill_style(AZURE_BLUE))
polygon([(10.33, 55.04), (12.99, 55.04), (12.99, 45.85), (10.33, 45.85)], style=fill_style(AZURE_BLUE))
polygon([(10.33, 41.27), (12.99, 41.27), (12.99, 32.08), (10.33, 32.08)], style=fill_style(AZURE_BLUE))
polygon([(10.33, 27.55), (12.99, 27.55), (12.99, 18.36), (10.33, 18.36)], style=fill_style(AZURE_BLUE))
save()
# fmt: on
