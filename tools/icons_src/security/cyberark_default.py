# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: cyberark (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import draw_compound_polygon, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(32.77, 59.94), (50.0, 69.92), (50.0, 91.0), (14.45, 70.45)], style=fill_style('#5090CA'))
draw_compound_polygon([[(50.06, 9.0), (50.04, 30.07), (67.3, 40.02), (85.55, 50.57), (85.55, 29.5)], [(49.99, 69.92), (67.25, 59.95), (85.5, 70.5), (50.0, 91.0)]], color='#3374AE')
polygon([(50.04, 30.07), (32.77, 40.02), (14.53, 29.47), (50.08, 9.01)], style=fill_style('#5090CA'))
polygon([(32.77, 40.02), (32.77, 59.94), (14.45, 70.45), (14.52, 29.47)], style=fill_style('#3374AE'))
polygon([(50.0, 69.92), (67.26, 59.95), (67.26, 40.02), (50.0, 49.99)], style=fill_style('#808184'))
polygon([(50.0, 69.92), (50.0, 49.99), (32.77, 40.02), (32.77, 59.94), (50.0, 69.92)], style=fill_style('#58595B'))
save()
# fmt: on
