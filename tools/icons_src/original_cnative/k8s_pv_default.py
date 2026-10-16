# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_pv."""

from drawlib.canvas import save
from drawlib.utils import (
    DARK,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_original_k8s_heptagon,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# Lower storage cylinder tier in white
draw_cylinder_tier(
    50.0,
    35.0,
    40.0,
    11.0,
    6.5,
    body_color=WHITE,
    border_color=DARK,
    border_units=2.3,
    draw_top_cap=False,
)

# Upper storage cylinder tier in light blue with mint green top cap
draw_cylinder_tier(
    50.0,
    46.0,
    40.0,
    11.0,
    6.5,
    body_color=PASTEL_BLUE_LIGHT,
    top_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=2.3,
    draw_top_cap=True,
)

save()
