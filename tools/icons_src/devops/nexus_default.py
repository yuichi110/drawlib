# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: nexus (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(88.02, 57.36), (50.18, 35.28), (12.08, 57.36), (11.98, 47.2), (50.18, 25.12), (88.02, 46.71)], style=fill_style('#01BC6D', border_color='#01BC6D', border_units=0.35))
polygon([(58.94, 91.0), (54.73, 89.95), (51.23, 86.83), (51.23, 90.3), (44.92, 90.3), (44.92, 65.42), (51.23, 65.42), (51.23, 81.54), (55.08, 84.34), (58.94, 84.34)], style=fill_style('#01BC6D', border_color='#01BC6D', border_units=0.35))
polygon([(11.98, 41.24), (11.98, 31.15), (49.82, 9.0), (88.02, 31.43), (88.02, 41.45), (49.47, 19.16)], style=fill_style('#1D202B', border_color='#1D202B', border_units=0.35))
polygon([(11.98, 83.64), (11.98, 63.32), (49.82, 41.24), (88.02, 63.67), (88.02, 83.99), (79.26, 83.99), (78.91, 68.22), (49.82, 51.4), (20.74, 68.57), (20.74, 83.54)], style=fill_style('#1D202B', border_color='#1D202B', border_units=0.35))
save()
# fmt: on
