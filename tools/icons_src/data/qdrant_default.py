# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data icon: qdrant (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(70.34, 15.63), (68.7, 60.71), (65.74, 72.59), (85.51, 70.5), (85.51, 15.97), (73.43, 9.0)], style=Icon.fill_style("#24386C"))
polygon([(85.51, 70.5), (73.43, 63.53), (48.52, 68.99), (19.35, 57.12), (14.49, 70.5), (32.24, 80.75), (50.0, 91.0), (67.75, 80.75)], style=Icon.fill_style("#7589BE"))
polygon([(14.49, 70.5), (26.57, 63.53), (33.57, 42.71), (57.2, 23.8), (50.0, 9.0), (32.24, 19.25), (14.49, 29.5)], style=Icon.fill_style("#B2BFE8"))
polygon([(58.01, 34.74), (50.0, 22.94), (50.0, 9.0), (61.36, 15.55), (67.21, 24.29)], style=Icon.fill_style("#24386C"))
polygon([(50.01, 36.88), (38.64, 56.55), (41.09, 63.07), (50.39, 67.58), (61.36, 56.55)], style=Icon.fill_style("#7589BE"))
polygon([(38.64, 56.55), (50.0, 50.0), (50.0, 36.88), (39.5, 36.43), (33.14, 44.55)], style=Icon.fill_style("#B2BFE8"))
polygon([(50.0, 50.0), (61.36, 56.55), (69.09, 43.68), (59.73, 35.95), (50.0, 36.88)], style=Icon.fill_style("#24386C"))
polygon([(61.36, 15.56), (73.43, 9.0), (73.43, 63.53), (61.71, 70.29), (50.0, 77.05), (38.28, 70.29), (26.57, 63.53), (26.57, 36.47), (38.28, 29.71), (50.0, 22.94), (61.36, 29.5)], holes=[[(61.36, 43.44), (50.0, 36.88), (38.64, 43.44), (38.64, 56.56), (50.0, 63.11), (61.36, 56.56), (61.36, 43.44)]], style=Icon.fill_style("#DC244C"))
polygon([(50.0, 22.94), (50.0, 36.88), (38.64, 43.44), (38.64, 29.5)], style=Icon.fill_style("#FF3364"))
save()
# fmt: on
