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
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Lower storage cylinder tier in white
Icon.draw_cylinder_tier(
    50.0,
    35.0,
    40.0,
    11.0,
    6.5,
    body_color=Icon.WHITE,
    border_color=Icon.DARK,
    border_units=2.0,
    draw_top_cap=False,
)

# Upper storage cylinder tier in light blue with mint green top cap
Icon.draw_cylinder_tier(
    50.0,
    46.0,
    40.0,
    11.0,
    6.5,
    body_color=Icon.PASTEL_BLUE_LIGHT,
    top_color=Icon.PASTEL_GREEN,
    border_color=Icon.DARK,
    border_units=2.0,
    draw_top_cap=True,
)

save()
