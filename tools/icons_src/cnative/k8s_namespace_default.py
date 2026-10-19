# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_namespace (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon, K8s

# ruff: noqa: E501
# fmt: off
Icon.setup()
K8s.draw_heptagon()
polygon([(32.88, 66.51), (36.6, 66.51), (36.6, 64.65), (32.88, 64.65)], style=Icon.fill_style(Icon.WHITE))
polygon([(38.46, 66.51), (42.19, 66.51), (42.19, 64.65), (38.46, 64.65)], style=Icon.fill_style(Icon.WHITE))
polygon([(44.05, 66.51), (47.78, 66.51), (47.78, 64.65), (44.05, 64.65)], style=Icon.fill_style(Icon.WHITE))
polygon([(49.64, 66.51), (53.37, 66.51), (53.37, 64.65), (49.64, 64.65)], style=Icon.fill_style(Icon.WHITE))
polygon([(55.23, 66.51), (58.96, 66.51), (58.96, 64.65), (55.23, 64.65)], style=Icon.fill_style(Icon.WHITE))
polygon([(60.82, 66.51), (64.55, 66.51), (64.55, 64.65), (60.82, 64.65)], style=Icon.fill_style(Icon.WHITE))
polygon([(66.41, 66.51), (67.87, 66.51), (68.05, 66.49), (68.23, 66.44), (68.39, 66.35), (68.53, 66.24), (68.64, 66.1), (68.73, 65.94), (68.78, 65.76), (68.8, 65.58), (68.8, 63.31), (66.94, 63.31), (66.94, 64.65), (66.41, 64.65)], style=Icon.fill_style(Icon.WHITE))
polygon([(68.8, 61.45), (68.8, 57.73), (66.94, 57.73), (66.94, 61.45)], style=Icon.fill_style(Icon.WHITE))
polygon([(68.8, 55.86), (68.8, 52.14), (66.94, 52.14), (66.94, 55.86)], style=Icon.fill_style(Icon.WHITE))
polygon([(68.8, 50.27), (68.8, 46.55), (66.94, 46.55), (66.94, 50.27)], style=Icon.fill_style(Icon.WHITE))
polygon([(68.8, 44.68), (68.8, 40.96), (66.94, 40.96), (66.94, 44.68)], style=Icon.fill_style(Icon.WHITE))
polygon([(68.8, 39.09), (68.8, 35.37), (66.94, 35.37), (66.94, 39.09)], style=Icon.fill_style(Icon.WHITE))
polygon([(66.96, 33.49), (63.23, 33.49), (63.23, 35.35), (66.96, 35.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(61.37, 33.49), (57.64, 33.49), (57.64, 35.35), (61.37, 35.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(55.78, 33.49), (52.05, 33.49), (52.05, 35.35), (55.78, 35.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(50.19, 33.49), (46.46, 33.49), (46.46, 35.35), (50.19, 35.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(44.6, 33.49), (40.87, 33.49), (40.87, 35.35), (44.6, 35.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(39.01, 33.49), (35.28, 33.49), (35.28, 35.35), (39.01, 35.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(33.42, 33.49), (32.13, 33.49), (31.95, 33.51), (31.77, 33.56), (31.61, 33.65), (31.47, 33.76), (31.36, 33.9), (31.27, 34.06), (31.22, 34.24), (31.2, 34.42), (31.2, 36.86), (33.06, 36.86), (33.06, 35.35), (33.42, 35.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(31.2, 38.72), (31.2, 42.44), (33.06, 42.44), (33.06, 38.72)], style=Icon.fill_style(Icon.WHITE))
polygon([(31.2, 44.31), (31.2, 48.03), (33.06, 48.03), (33.06, 44.31)], style=Icon.fill_style(Icon.WHITE))
polygon([(31.2, 49.9), (31.2, 53.62), (33.06, 53.62), (33.06, 49.9)], style=Icon.fill_style(Icon.WHITE))
polygon([(31.2, 55.49), (31.2, 59.21), (33.06, 59.21), (33.06, 55.49)], style=Icon.fill_style(Icon.WHITE))
polygon([(31.2, 61.07), (31.2, 64.8), (33.06, 64.8), (33.06, 61.07)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
