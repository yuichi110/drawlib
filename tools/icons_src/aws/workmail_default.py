# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AWS icon: workmail (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Aws, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
Aws.draw_service_plate(Aws.RED)
polygon([(78.35, 79.4), (21.65, 79.4), (21.44, 79.38), (21.24, 79.32), (21.06, 79.22), (20.91, 79.09), (20.78, 78.94), (20.68, 78.76), (20.62, 78.56), (20.6, 78.35), (20.6, 21.65), (20.62, 21.44), (20.68, 21.24), (20.78, 21.06), (20.91, 20.91), (21.06, 20.78), (21.24, 20.68), (21.44, 20.62), (21.65, 20.6), (78.35, 20.6), (78.56, 20.62), (78.76, 20.68), (78.94, 20.78), (79.09, 20.91), (79.22, 21.06), (79.32, 21.24), (79.38, 21.44), (79.4, 21.65), (79.4, 78.35), (79.38, 78.56), (79.32, 78.76), (79.22, 78.94), (79.09, 79.09), (78.94, 79.22), (78.76, 79.32), (78.56, 79.38)], holes=[[(22.7, 22.7), (22.7, 75.82), (49.26, 49.26), (49.34, 49.19), (49.42, 49.12), (49.51, 49.07), (49.6, 49.03), (49.7, 48.99), (49.8, 48.97), (49.9, 48.95), (50.0, 48.95), (50.1, 48.95), (50.2, 48.97), (50.3, 48.99), (50.4, 49.03), (50.49, 49.07), (50.58, 49.12), (50.66, 49.19), (50.74, 49.26), (77.3, 75.82), (77.3, 22.7)], [(75.82, 77.3), (50.0, 51.48), (24.18, 77.3)]], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
