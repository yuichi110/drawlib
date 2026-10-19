# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_ingress (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon, K8s

# ruff: noqa: E501
# fmt: off
Icon.setup()
K8s.draw_heptagon()
polygon([(62.8, 31.03), (52.22, 31.03), (29.3, 59.7), (22.67, 59.7), (22.67, 69.09), (33.45, 69.09), (56.38, 40.42), (62.8, 40.42), (62.8, 47.84), (77.33, 35.73), (62.8, 23.61)], style=Icon.fill_style(Icon.WHITE))
polygon([(51.26, 53.18), (56.38, 59.58), (62.8, 59.58), (62.8, 52.16), (77.33, 64.27), (62.8, 76.39), (62.8, 68.97), (52.22, 68.97), (45.43, 60.47)], style=Icon.fill_style(Icon.WHITE))
polygon([(34.51, 46.82), (29.3, 40.3), (22.67, 40.3), (22.67, 30.91), (33.45, 30.91), (40.34, 39.53)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
