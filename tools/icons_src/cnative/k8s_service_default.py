# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: k8s_service (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import K8S_BLUE, WHITE, draw_k8s_heptagon, draw_round_polyline, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_k8s_heptagon()
polygon([(24.74, 40.66), (38.29, 40.66), (38.29, 31.15), (24.74, 31.15)], style=fill_style(WHITE))
polygon([(43.23, 40.66), (56.77, 40.66), (56.77, 31.15), (43.23, 31.15)], style=fill_style(WHITE))
polygon([(61.71, 40.66), (75.26, 40.66), (75.26, 31.15), (61.71, 31.15)], style=fill_style(WHITE))
polygon([(39.27, 68.85), (60.73, 68.85), (60.73, 59.34), (39.27, 59.34)], style=fill_style(WHITE))
draw_round_polyline([(50.0, 59.34), (50.0, 50.0), (31.53, 50.0), (31.53, 40.67)], width_units=2.46, color=WHITE, closed=False)
draw_round_polyline([(50.0, 59.34), (50.0, 50.0), (68.47, 50.0), (68.47, 40.67)], width_units=2.46, color=WHITE, closed=False)
draw_round_polyline([(49.96, 59.33), (49.96, 49.99), (50.04, 49.99), (50.04, 40.67)], width_units=2.46, color=WHITE, closed=False)
save()
# fmt: on
