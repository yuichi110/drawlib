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
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Single large crisp isometric container cube
Icon.draw_iso_cube(
    50.0,
    47.0,
    radius=21.0,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE_LIGHT,
    right_color=Icon.PASTEL_GREEN,
    border_color=Icon.DARK,
    border_units=2.0,
)

save()
