# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AWS icon: command_line_interface (default variant)."""

from drawlib.canvas import save
from drawlib.utils import AWS_MAGENTA, WHITE, draw_aws_service_plate, draw_layered_polygons, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_aws_service_plate(AWS_MAGENTA)
draw_layered_polygons([[(20.6, 78.35), (20.6, 21.65), (56.3, 21.65), (56.3, 23.75), (22.7, 23.75), (22.7, 67.85), (77.3, 67.85), (77.3, 23.75), (69.95, 23.75), (69.95, 21.65), (79.4, 21.65), (79.4, 78.35)], [(22.7, 69.95), (77.3, 69.95), (77.3, 76.25), (22.7, 76.25)], [(34.25, 72.05), (36.35, 72.05), (36.35, 74.15), (34.25, 74.15)], [(30.05, 72.05), (32.15, 72.05), (32.15, 74.15), (30.05, 74.15)], [(25.85, 72.05), (27.95, 72.05), (27.95, 74.15), (25.85, 74.15)], [(32.49, 56.9), (43.08, 46.31), (32.49, 35.73), (33.98, 34.24), (46.05, 46.31), (33.98, 58.38)], [(47.9, 38.45), (65.75, 38.45), (65.75, 40.55), (47.9, 40.55)]], fg_color=WHITE, bg_color=AWS_MAGENTA)
save()
# fmt: on
