# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_job (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon, K8s

# ruff: noqa: E501
# fmt: off
Icon.setup()
K8s.draw_heptagon()
polygon([(30.19, 40.47), (40.45, 40.47), (40.45, 30.49), (30.19, 30.49)], style=Icon.fill_style(Icon.WHITE))
polygon([(44.87, 40.47), (55.13, 40.47), (55.13, 30.49), (44.87, 30.49)], style=Icon.fill_style(Icon.WHITE))
polygon([(59.55, 40.47), (69.81, 40.47), (69.81, 30.49), (59.55, 30.49)], style=Icon.fill_style(Icon.WHITE))
polygon([(59.55, 55.14), (69.81, 55.14), (69.81, 45.16), (59.55, 45.16)], style=Icon.fill_style(Icon.WHITE))
polygon([(44.92, 54.99), (55.18, 54.99), (55.18, 45.01), (44.92, 45.01)], style=Icon.fill_style(Icon.WHITE))
polygon([(30.28, 54.99), (40.54, 54.99), (40.54, 45.01), (30.28, 45.01)], style=Icon.fill_style(Icon.WHITE))
polygon([(59.55, 69.51), (69.81, 69.51), (69.81, 59.53), (59.55, 59.53)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
