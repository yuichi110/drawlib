# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: dataproc_metastore (default variant)."""

from drawlib.canvas import save
from drawlib.utils import GCP_TECH_MID, draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(50.32, 50.0), (80.0, 32.32), (50.32, 14.63), (20.63, 32.32)], [(77.56, 59.04), (92.0, 50.04), (91.92, 50.0), (92.0, 49.96), (77.56, 40.96), (73.05, 43.33), (83.75, 50.0), (73.05, 56.67)], [(22.44, 59.04), (26.95, 56.67), (16.24, 50.0), (26.95, 43.33), (22.44, 40.96), (8.0, 49.96), (8.07, 50.0), (8.0, 50.04)], [(50.32, 85.37), (80.0, 67.68), (50.32, 50.0), (20.63, 67.68)]], color=GCP_TECH_MID)
save()
# fmt: on
