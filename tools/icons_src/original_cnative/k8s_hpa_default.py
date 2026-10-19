# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_hpa."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Outward left and right horizontal scaling arrows
Icon.draw_round_segment((36.0, 48.0), (23.0, 48.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(
    [(28.5, 53.0), (23.0, 48.0), (28.5, 43.0)],
    width_units=2.0,
    color=Icon.DARK,
)

Icon.draw_round_segment((64.0, 48.0), (77.0, 48.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(
    [(71.5, 53.0), (77.0, 48.0), (71.5, 43.0)],
    width_units=2.0,
    color=Icon.DARK,
)

# Central white pod square
rectangle(
    (50.0, 48.0),
    width=23.0,
    height=23.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.0),
)

# Inner green workload square
rectangle(
    (50.0, 48.0),
    width=10.5,
    height=10.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
)

save()
