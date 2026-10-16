# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_daemonset (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import K8S_BLUE, WHITE, draw_k8s_heptagon, draw_round_polyline, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_k8s_heptagon()
polygon([(53.27, 70.72), (63.13, 70.72), (63.13, 68.26), (53.27, 68.26)], style=fill_style(WHITE))
polygon([(68.06, 70.72), (72.4, 70.72), (72.64, 70.7), (72.87, 70.63), (73.08, 70.51), (73.27, 70.36), (73.42, 70.17), (73.54, 69.96), (73.61, 69.73), (73.63, 69.49), (73.63, 63.97), (71.17, 63.97), (71.17, 68.26), (68.06, 68.26)], style=fill_style(WHITE))
polygon([(73.63, 59.04), (73.63, 49.18), (71.17, 49.18), (71.17, 59.04)], style=fill_style(WHITE))
polygon([(68.51, 46.91), (58.65, 46.91), (58.65, 49.37), (68.51, 49.37)], style=fill_style(WHITE))
polygon([(53.73, 46.91), (43.87, 46.91), (43.87, 49.37), (53.73, 49.37)], style=fill_style(WHITE))
polygon([(40.78, 51.21), (40.78, 61.07), (43.24, 61.07), (43.24, 51.21)], style=fill_style(WHITE))
polygon([(40.78, 66.0), (40.78, 69.49), (40.8, 69.73), (40.87, 69.96), (40.98, 70.17), (41.14, 70.36), (41.32, 70.51), (41.54, 70.63), (41.77, 70.7), (42.01, 70.72), (48.34, 70.72), (48.34, 68.26), (43.24, 68.26), (43.24, 66.0)], style=fill_style(WHITE))
polygon([(26.37, 29.28), (59.32, 29.28), (59.32, 32.16), (26.37, 32.16)], style=fill_style(WHITE))
polygon([(34.84, 62.92), (65.23, 62.92), (65.23, 41.57), (34.84, 41.57)], style=fill_style(K8S_BLUE))
polygon([(45.12, 64.15), (54.98, 64.15), (54.98, 61.68), (45.12, 61.68)], style=fill_style(WHITE))
polygon([(59.91, 64.15), (65.23, 64.15), (65.47, 64.12), (65.7, 64.05), (65.92, 63.94), (66.1, 63.79), (66.26, 63.6), (66.37, 63.39), (66.44, 63.16), (66.46, 62.92), (66.46, 58.38), (64.0, 58.38), (64.0, 61.68), (59.91, 61.68)], style=fill_style(WHITE))
polygon([(66.46, 53.45), (66.46, 43.6), (64.0, 43.6), (64.0, 53.45)], style=fill_style(WHITE))
polygon([(62.33, 40.34), (52.47, 40.34), (52.47, 42.8), (62.33, 42.8)], style=fill_style(WHITE))
polygon([(47.54, 40.34), (37.69, 40.34), (37.69, 42.8), (47.54, 42.8)], style=fill_style(WHITE))
polygon([(33.61, 43.65), (33.61, 53.51), (36.07, 53.51), (36.07, 43.65)], style=fill_style(WHITE))
polygon([(33.61, 58.44), (33.61, 62.92), (33.63, 63.16), (33.7, 63.39), (33.82, 63.6), (33.97, 63.79), (34.16, 63.94), (34.37, 64.05), (34.6, 64.12), (34.84, 64.15), (40.19, 64.15), (40.19, 61.68), (36.07, 61.68), (36.07, 58.44)], style=fill_style(WHITE))
draw_round_polyline([(27.68, 56.34), (58.07, 56.34), (58.07, 34.99), (27.68, 34.99)], width_units=2.46, color=WHITE, closed=True)
polygon([(27.47, 56.26), (57.86, 56.26), (57.86, 34.91), (27.47, 34.91)], style=fill_style(WHITE))
save()
# fmt: on
