# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_pod."""

from drawlib.canvas import save
from drawlib.utils import (
    DARK,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_original_k8s_heptagon,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# Single large crisp isometric container cube
draw_iso_cube(
    50.0,
    47.0,
    radius=21.0,
    top_color=WHITE,
    left_color=PASTEL_BLUE_LIGHT,
    right_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=2.0,
)

save()
