# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AWS icon: finspace (default variant)."""

from drawlib.canvas import save
from drawlib.utils import AWS_PURPLE, WHITE, draw_aws_service_plate, draw_layered_polygons, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_aws_service_plate(AWS_PURPLE)
draw_layered_polygons([[(33.2, 33.2), (37.4, 33.2), (37.4, 60.09), (33.2, 57.22)], [(44.75, 65.1), (39.5, 61.52), (39.5, 33.2), (44.75, 33.2)], [(46.85, 66.53), (46.85, 33.2), (53.15, 33.2), (53.15, 66.53), (50.0, 68.68)], [(60.5, 61.52), (55.25, 65.1), (55.25, 33.2), (60.5, 33.2)], [(66.8, 57.22), (62.6, 60.09), (62.6, 33.2), (66.8, 33.2)], [(74.15, 31.1), (25.85, 31.1), (25.85, 33.2), (31.1, 33.2), (31.1, 55.79), (27.49, 53.33), (26.31, 55.07), (49.41, 70.82), (49.55, 70.9), (49.69, 70.95), (49.85, 70.99), (50.0, 71.0), (50.15, 70.99), (50.31, 70.95), (50.45, 70.9), (50.59, 70.82), (73.69, 55.07), (72.51, 53.33), (68.9, 55.79), (68.9, 33.2), (74.15, 33.2)], [(23.75, 25.85), (34.25, 25.85), (34.25, 27.95), (23.75, 27.95)], [(38.45, 25.85), (61.55, 25.85), (61.55, 27.95), (38.45, 27.95)], [(65.75, 25.85), (76.25, 25.85), (76.25, 27.95), (65.75, 27.95)], [(20.6, 20.6), (46.85, 20.6), (46.85, 22.7), (20.6, 22.7)], [(53.15, 20.6), (79.4, 20.6), (79.4, 22.7), (53.15, 22.7)], [(22.23, 57.53), (21.07, 59.27), (49.42, 78.17), (49.55, 78.25), (49.7, 78.31), (49.85, 78.34), (50.0, 78.35), (50.15, 78.34), (50.3, 78.31), (50.45, 78.25), (50.58, 78.17), (78.93, 59.27), (77.77, 57.53), (50.0, 76.04)]], fg_color=WHITE, bg_color=AWS_PURPLE)
save()
# fmt: on
