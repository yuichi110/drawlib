# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_cronjob."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Top alarm / schedule button stem and tab
Icon.draw_round_segment((50.0, 64.0), (50.0, 69.5), width_units=2.0, color=Icon.DARK)
rectangle(
    (50.0, 72.0),
    width=14.0,
    height=6.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
)

# White circular clock face
circle(
    (50.0, 44.0),
    radius=20.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# L-shaped dark clock hands
Icon.draw_round_polyline(
    [(50.0, 55.0), (50.0, 44.0), (58.5, 38.8)],
    width_units=2.0,
    color=Icon.DARK,
)

# Green center clock pivot dot
circle(
    (50.0, 44.0),
    radius=3.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
