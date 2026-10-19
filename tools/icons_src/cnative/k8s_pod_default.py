# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_pod (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon, K8s

# ruff: noqa: E501
# fmt: off
Icon.setup()
K8s.draw_heptagon()
polygon([(33.14, 61.82), (50.0, 66.71), (66.86, 61.82), (50.0, 56.92)], style=Icon.fill_style(Icon.WHITE))
polygon([(33.14, 59.94), (33.14, 42.0), (48.85, 33.29), (48.93, 55.25)], style=Icon.fill_style(Icon.WHITE))
polygon([(66.86, 59.94), (66.86, 42.0), (51.15, 33.29), (51.07, 55.25)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
