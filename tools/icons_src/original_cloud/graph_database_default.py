# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: graph_database."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

hub = (48.0, 50.0)
n_tl = (24.0, 72.0)
n_tr = (76.0, 70.0)
n_bl = (24.0, 26.0)
n_br = (74.0, 26.0)

# 1. Graph edges
edges = [
    (hub, n_tl),
    (hub, n_tr),
    (hub, n_bl),
    (hub, n_br),
    (n_tl, n_tr),
    (n_tl, n_bl),
]
for p1, p2 in edges:
    draw_round_segment(p1, p2, width_units=w, color=DARK)

# 2. Center hub node
circle(
    hub,
    radius=12.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    hub,
    radius=4.0,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8),
)

# 3. Outer vertex nodes
circle(
    n_tl,
    radius=9.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
circle(
    n_tr,
    radius=9.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)
circle(
    n_bl,
    radius=9.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)
circle(
    n_br,
    radius=9.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

save()
