# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: cert_manager."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# White TLS certificate document card
rectangle(
    (46.0, 53.0),
    width=38.0,
    height=32.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.5),
)

# Certificate header bar and signature lines
rectangle(
    (41.0, 62.0),
    width=18.0,
    height=4.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=1.5),
)
Icon.draw_round_segment((33.0, 54.0), (57.0, 54.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((33.0, 47.5), (50.0, 47.5), width_units=2.0, color=Icon.DARK)

# Left and right ribbon tails with smooth round-joined notches
left_ribbon = [(56.5, 30.0), (54.5, 20.5), (57.8, 23.2), (60.8, 20.5), (60.8, 30.0)]
polygon(left_ribbon, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(left_ribbon, width_units=2.0, color=Icon.DARK, closed=True)

right_ribbon = [(62.2, 30.0), (62.2, 20.5), (65.2, 23.2), (68.5, 20.5), (66.5, 30.0)]
polygon(right_ribbon, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(right_ribbon, width_units=2.0, color=Icon.DARK, closed=True)

# Overlapping pastel green circular certificate seal
circle(
    (61.5, 37.0),
    radius=11.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

# Crisp checkmark inside the certificate seal
Icon.draw_round_polyline(
    [(57.5, 36.8), (60.5, 33.8), (65.8, 40.2)],
    width_units=2.0,
    color=Icon.DARK,
)

save()
