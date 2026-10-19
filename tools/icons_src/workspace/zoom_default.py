# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Workspace icon: zoom (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
circle((50.0, 50.0), radius=41.0, style=Icon.fill_style('#2196F3'))
polygon([(33.06, 38.28), (60.17, 38.28), (60.17, 58.17), (60.16, 58.54), (60.12, 58.9), (60.06, 59.26), (59.98, 59.61), (59.87, 59.95), (59.74, 60.28), (59.59, 60.6), (59.43, 60.91), (59.24, 61.2), (59.04, 61.48), (58.82, 61.75), (58.58, 62.01), (58.32, 62.24), (58.06, 62.46), (57.77, 62.67), (57.48, 62.86), (57.17, 63.02), (56.85, 63.17), (56.52, 63.3), (56.18, 63.4), (55.83, 63.49), (55.48, 63.55), (55.11, 63.58), (54.74, 63.6), (27.64, 63.6), (27.64, 43.71), (27.66, 43.33), (27.69, 42.97), (27.75, 42.61), (27.84, 42.26), (27.94, 41.92), (28.07, 41.59), (28.21, 41.27), (28.38, 40.97), (28.56, 40.67), (28.77, 40.39), (28.99, 40.12), (29.23, 39.87), (29.48, 39.63), (29.75, 39.41), (30.03, 39.21), (30.32, 39.02), (30.63, 38.85), (30.95, 38.7), (31.28, 38.58), (31.61, 38.47), (31.96, 38.39), (32.32, 38.33), (32.68, 38.29)], style=Icon.fill_style(Icon.WHITE))
polygon([(63.79, 45.52), (74.63, 38.29), (74.63, 63.6), (63.79, 56.36)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
