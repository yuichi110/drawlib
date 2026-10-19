# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: multi_agent."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Triangle coordination links between the 3 agents
Icon.draw_round_segment((42.0, 60.0), (31.0, 37.0), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((58.0, 60.0), (69.0, 37.0), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((39.0, 28.0), (61.0, 28.0), width_units=w, color=Icon.DARK)

# 2. Top orchestrator AI agent node
Icon.draw_round_segment((50.0, 80.0), (50.0, 85.0), width_units=2.0, color=Icon.DARK)
circle(
    (50.0, 85.5),
    radius=2.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
)
rectangle(
    (50.0, 70.0),
    width=28.0,
    height=20.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)
for ex in (44.0, 56.0):
    circle(
        (ex, 70.0),
        radius=2.8,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.9),
    )

# 3. Bottom peer AI agent nodes
for px in (26.0, 74.0):
    Icon.draw_round_segment((px, 37.0), (px, 41.5), width_units=2.0, color=Icon.DARK)
    circle(
        (px, 42.0),
        radius=2.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8),
    )
    rectangle(
        (px, 28.0),
        width=26.0,
        height=18.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=5.5),
    )
    for ex in (px - 5.5, px + 5.5):
        circle(
            (ex, 28.0),
            radius=2.6,
            style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8),
        )

save()
