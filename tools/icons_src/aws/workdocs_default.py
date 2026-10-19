# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AWS icon: workdocs (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Aws, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
Aws.draw_service_plate(Aws.RED)
polygon([(79.4, 50.0), (79.4, 50.1), (79.38, 50.2), (79.36, 50.3), (79.32, 50.4), (79.28, 50.49), (79.23, 50.58), (79.16, 50.66), (79.09, 50.74), (50.74, 79.09), (50.66, 79.16), (50.58, 79.23), (50.49, 79.28), (50.4, 79.32), (50.3, 79.36), (50.2, 79.38), (50.1, 79.4), (50.0, 79.4), (21.65, 79.4), (21.44, 79.38), (21.24, 79.32), (21.06, 79.22), (20.91, 79.09), (20.78, 78.94), (20.68, 78.76), (20.62, 78.56), (20.6, 78.35), (20.6, 21.65), (20.62, 21.44), (20.68, 21.24), (20.78, 21.06), (20.91, 20.91), (21.06, 20.78), (21.24, 20.68), (21.44, 20.62), (21.65, 20.6), (78.35, 20.6), (78.56, 20.62), (78.76, 20.68), (78.94, 20.78), (79.09, 20.91), (79.22, 21.06), (79.32, 21.24), (79.38, 21.44), (79.4, 21.65)], holes=[[(51.05, 22.7), (51.05, 25.85), (48.95, 25.85), (48.95, 22.7), (22.7, 22.7), (22.7, 48.95), (24.8, 48.95), (24.8, 51.05), (22.7, 51.05), (22.7, 77.3), (48.95, 77.3), (48.95, 51.05), (47.9, 51.05), (47.9, 48.95), (50.0, 48.95), (51.05, 48.95), (77.3, 48.95), (77.3, 22.7)], [(51.05, 75.82), (75.82, 51.05), (51.05, 51.05)]], style=Icon.fill_style(Icon.WHITE))
polygon([(42.65, 48.95), (45.8, 48.95), (45.8, 51.05), (42.65, 51.05)], style=Icon.fill_style(Icon.WHITE))
polygon([(48.95, 27.95), (51.05, 27.95), (51.05, 31.1), (48.95, 31.1)], style=Icon.fill_style(Icon.WHITE))
polygon([(48.95, 33.2), (51.05, 33.2), (51.05, 36.35), (48.95, 36.35)], style=Icon.fill_style(Icon.WHITE))
polygon([(48.95, 43.7), (51.05, 43.7), (51.05, 46.85), (48.95, 46.85)], style=Icon.fill_style(Icon.WHITE))
polygon([(48.95, 38.45), (51.05, 38.45), (51.05, 41.6), (48.95, 41.6)], style=Icon.fill_style(Icon.WHITE))
polygon([(37.4, 48.95), (40.55, 48.95), (40.55, 51.05), (37.4, 51.05)], style=Icon.fill_style(Icon.WHITE))
polygon([(32.15, 48.95), (35.3, 48.95), (35.3, 51.05), (32.15, 51.05)], style=Icon.fill_style(Icon.WHITE))
polygon([(26.9, 48.95), (30.05, 48.95), (30.05, 51.05), (26.9, 51.05)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
