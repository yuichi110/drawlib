# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Business icon: plaid (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(41.6, 91.0), (16.47, 84.42), (9.54, 59.15), (18.21, 50.26), (9.41, 41.51), (15.92, 16.13), (40.94, 9.14), (49.74, 17.89), (58.4, 9.0), (83.53, 15.58), (90.45, 40.85), (81.79, 49.74), (90.59, 58.49), (84.08, 83.87), (59.06, 90.86), (50.26, 82.11)], holes=[[(28.24, 50.18), (36.68, 58.57), (44.99, 50.04), (36.54, 41.65)], [(41.52, 36.55), (49.96, 44.93), (58.26, 36.41), (49.82, 28.02)], [(55.02, 49.96), (63.46, 58.35), (71.76, 49.82), (63.32, 41.43)], [(41.73, 63.59), (50.18, 71.98), (58.48, 63.45), (50.04, 55.07)], [(25.71, 20.83), (36.46, 31.52), (44.77, 23.0), (38.88, 17.15)], [(26.18, 79.56), (39.41, 83.03), (45.2, 77.08), (36.76, 68.7)], [(68.29, 36.33), (76.74, 44.71), (82.52, 38.77), (78.88, 25.46)], [(68.51, 63.37), (79.27, 74.06), (82.7, 60.69), (76.82, 54.85)], [(54.8, 22.92), (63.24, 31.3), (73.82, 20.44), (60.58, 16.97)], [(55.23, 77.01), (61.12, 82.85), (74.29, 79.17), (63.54, 68.48)], [(17.3, 39.31), (23.18, 45.15), (31.49, 36.63), (20.73, 25.94)], [(17.47, 61.22), (21.12, 74.53), (31.7, 63.67), (23.26, 55.28), (17.47, 61.23)]], style=Icon.fill_style('#111111'))
save()
# fmt: on
