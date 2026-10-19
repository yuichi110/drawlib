# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: bare_metal_solutions (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 8.02), (8.0, 27.98), (29.0, 34.64), (50.0, 14.64), (71.0, 34.64), (92.0, 27.98)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(50.0, 91.98), (85.0, 58.64), (50.0, 25.31), (15.0, 58.64)], holes=[[(50.0, 85.31), (22.0, 58.64), (50.0, 31.98), (78.0, 58.64)]], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(81.92, 48.65), (85.0, 45.71), (50.0, 11.98), (15.0, 45.71), (18.07, 48.64), (21.0, 45.84), (20.71, 45.57), (50.0, 18.08), (79.29, 45.57), (78.99, 45.84)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
