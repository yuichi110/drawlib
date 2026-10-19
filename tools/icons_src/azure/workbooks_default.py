# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: workbooks (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Azure, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(44.27, 74.82), (8.0, 38.54), (8.0, 15.63), (8.26, 13.66), (9.02, 11.82), (10.24, 10.24), (11.82, 9.02), (13.66, 8.26), (15.63, 8.0), (84.37, 8.0), (86.34, 8.26), (88.18, 9.02), (89.76, 10.24), (90.98, 11.82), (91.74, 13.66), (92.0, 15.63), (92.0, 84.37), (91.74, 86.34), (90.98, 88.18), (89.76, 89.76), (88.18, 90.98), (86.34, 91.74), (84.37, 92.0), (80.54, 92.0), (53.82, 65.27)], style=Icon.fill_style(Azure.BLUE))
polygon([(44.27, 51.91), (10.73, 18.37), (9.73, 17.36), (9.01, 16.12), (8.63, 14.75), (8.61, 13.32), (8.96, 11.93), (9.89, 10.61), (11.08, 9.51), (12.48, 8.68), (14.02, 8.17), (15.63, 8.0), (84.37, 8.0), (86.34, 8.26), (88.18, 9.02), (89.76, 10.24), (90.98, 11.82), (91.74, 13.66), (92.0, 15.63), (92.0, 80.54), (53.82, 42.37)], style=Icon.fill_style("#00CCF9"))
polygon([(53.82, 65.27), (80.54, 92.0), (15.63, 92.0), (13.66, 91.74), (11.82, 90.98), (10.24, 89.76), (9.02, 88.18), (8.26, 86.34), (8.0, 84.37), (8.0, 38.54), (44.27, 74.82)], style=Icon.fill_style("#7CECFF"))
save()
# fmt: on
