# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_hpa (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon, K8s

# ruff: noqa: E501
# fmt: off
Icon.setup()
K8s.draw_heptagon()
polygon([(17.29, 50.0), (26.92, 59.31), (26.92, 54.66), (30.47, 54.66), (30.47, 68.63), (69.53, 68.63), (69.53, 54.66), (73.08, 54.66), (73.08, 59.31), (82.71, 50.0), (73.08, 40.69), (73.08, 45.34), (69.53, 45.34), (69.53, 31.37), (30.47, 31.37), (30.47, 45.34), (26.92, 45.34), (26.92, 40.69)], style=Icon.fill_style(Icon.WHITE))
polygon([(35.03, 60.14), (50.0, 64.34), (64.97, 60.14), (50.0, 55.94)], style=Icon.fill_style(K8s.BLUE))
polygon([(35.03, 58.53), (35.03, 43.13), (48.98, 35.66), (49.05, 54.5)], style=Icon.fill_style(K8s.BLUE))
polygon([(64.97, 58.53), (64.97, 43.13), (51.02, 35.66), (50.95, 54.5)], style=Icon.fill_style(K8s.BLUE))
save()
# fmt: on
