# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_endpoint (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon, K8s

# ruff: noqa: E501
# fmt: off
Icon.setup()
K8s.draw_heptagon()
polygon([(24.74, 40.66), (38.29, 40.66), (38.29, 31.15), (24.74, 31.15)], style=Icon.fill_style(Icon.WHITE))
polygon([(43.23, 40.66), (56.77, 40.66), (56.77, 31.15), (43.23, 31.15)], style=Icon.fill_style(Icon.WHITE))
polygon([(61.71, 40.66), (75.26, 40.66), (75.26, 31.15), (61.71, 31.15)], style=Icon.fill_style(Icon.WHITE))
polygon([(39.27, 68.85), (60.73, 68.85), (60.73, 59.34), (39.27, 59.34)], style=Icon.fill_style(Icon.WHITE))
polygon([(41.91, 57.15), (44.05, 55.01), (34.47, 45.43), (32.32, 47.57)], style=Icon.fill_style(Icon.WHITE))
polygon([(30.61, 43.66), (31.82, 48.27), (33.03, 52.87), (36.41, 49.52), (39.79, 46.16), (35.2, 44.91)], style=Icon.fill_style(Icon.WHITE))
polygon([(56.05, 57.15), (53.91, 55.01), (63.49, 45.43), (65.64, 47.57)], style=Icon.fill_style(Icon.WHITE))
polygon([(67.35, 43.66), (66.14, 48.27), (64.93, 52.87), (61.55, 49.52), (58.17, 46.16), (62.76, 44.91)], style=Icon.fill_style(Icon.WHITE))
polygon([(51.12, 56.33), (48.09, 56.34), (48.0, 45.87), (51.04, 45.85)], style=Icon.fill_style(Icon.WHITE))
polygon([(49.46, 41.89), (51.88, 45.98), (54.31, 50.08), (49.55, 50.13), (44.79, 50.18), (47.13, 46.03)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
