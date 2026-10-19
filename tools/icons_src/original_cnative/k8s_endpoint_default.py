# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_endpoint."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Connecting dark lines from left source to right target endpoints
Icon.draw_round_segment((32.0, 48.0), (65.0, 59.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((32.0, 48.0), (65.0, 37.0), width_units=2.0, color=Icon.DARK)

# Left white source circle
circle(
    (32.0, 48.0),
    radius=7.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# Two right green target endpoint circles
for y_target in (59.0, 37.0):
    circle(
        (65.0, y_target),
        radius=7.5,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
    )

save()
