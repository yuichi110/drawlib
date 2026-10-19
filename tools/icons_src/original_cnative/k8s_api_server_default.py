# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_api_server."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Inner white API gateway card
rectangle(
    (50.0, 48.0),
    width=46.0,
    height=34.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=6.0),
)

# Left and right horizontal bidirectional routing arrows
Icon.draw_round_segment((33.0, 48.0), (67.0, 48.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(
    [(37.5, 52.2), (32.5, 48.0), (37.5, 43.8)],
    width_units=2.0,
    color=Icon.DARK,
)
Icon.draw_round_polyline(
    [(62.5, 52.2), (67.5, 48.0), (62.5, 43.8)],
    width_units=2.0,
    color=Icon.DARK,
)

# Central green routing hub
circle(
    (50.0, 48.0),
    radius=6.8,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
