# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_configmap (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon, K8s

# ruff: noqa: E501
# fmt: off
Icon.setup()
K8s.draw_heptagon()
polygon([(42.29, 62.94), (69.42, 62.94), (69.42, 66.64), (42.29, 66.64)], style=Icon.fill_style(Icon.WHITE))
polygon([(30.58, 62.94), (37.37, 62.94), (37.37, 66.64), (30.58, 66.64)], style=Icon.fill_style(Icon.WHITE))
polygon([(52.15, 53.08), (69.42, 53.08), (69.42, 56.78), (52.15, 56.78)], style=Icon.fill_style(Icon.WHITE))
polygon([(40.44, 53.08), (47.23, 53.08), (47.23, 56.78), (40.44, 56.78)], style=Icon.fill_style(Icon.WHITE))
polygon([(52.15, 43.22), (69.42, 43.22), (69.42, 46.92), (52.15, 46.92)], style=Icon.fill_style(Icon.WHITE))
polygon([(40.44, 43.22), (47.23, 43.22), (47.23, 46.92), (40.44, 46.92)], style=Icon.fill_style(Icon.WHITE))
polygon([(42.29, 33.36), (69.42, 33.36), (69.42, 37.06), (42.29, 37.06)], style=Icon.fill_style(Icon.WHITE))
polygon([(30.58, 33.36), (37.37, 33.36), (37.37, 37.06), (30.58, 37.06)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
