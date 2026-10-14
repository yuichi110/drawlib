# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: batch (default variant)."""

from drawlib.canvas import save
from drawlib.utils import GCP_TECH_MID, draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(66.27, 78.09), (92.0, 50.03), (66.27, 21.98), (57.67, 31.36), (49.01, 21.91), (41.34, 30.27), (33.73, 21.98), (8.0, 50.03), (33.73, 78.09), (41.4, 69.73), (38.71, 66.8), (33.73, 72.22), (13.38, 50.03), (33.73, 27.85), (38.65, 33.21), (23.28, 49.97), (49.01, 78.02), (57.61, 68.65)], [(49.01, 72.15), (28.66, 49.97), (49.01, 27.78), (54.97, 34.29), (40.54, 50.03), (54.91, 65.72)]], color=GCP_TECH_MID)
save()
# fmt: on
