# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_daemonset."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Slight upward offset so the pods and node bar center visually inside the heptagon
dy = 3.0

# Vertical connectors binding each pod to the underlying node bar
for x_pod in (38.0, 62.0):
    Icon.draw_round_segment((x_pod, 33.0 + dy), (x_pod, 42.0 + dy), width_units=2.0, color=Icon.DARK)

# Bottom green horizontal node bar
rectangle(
    (50.0, 31.0 + dy),
    width=46.0,
    height=8.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=3.0),
)

# Two side-by-side white pod squares with light blue inner dots
for x_pod in (38.0, 62.0):
    rectangle(
        (x_pod, 51.5 + dy),
        width=19.0,
        height=19.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.0),
    )
    circle(
        (x_pod, 51.5 + dy),
        radius=4.2,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0),
    )

save()
