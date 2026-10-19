# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_configmap."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Inner white configuration card
rectangle(
    (50.0, 48.0),
    width=44.0,
    height=38.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=6.0),
)

# Three horizontal slider tracks with alternating pastel knobs
sliders = [
    (58.5, 57.0, Icon.PASTEL_GREEN),
    (48.0, 42.0, Icon.PASTEL_BLUE_LIGHT),
    (37.5, 54.0, Icon.PASTEL_GREEN),
]
for y_pos, knob_x, knob_color in sliders:
    Icon.draw_round_segment((34.5, y_pos), (65.5, y_pos), width_units=2.0, color=Icon.DARK)
    circle(
        (knob_x, y_pos),
        radius=3.5,
        style=Icon.fill_style(knob_color, border_color=Icon.DARK, border_units=2.0),
    )

save()
