# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_routes (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(69.66, 20.85), (53.4, 20.85), (18.21, 64.91), (8.0, 64.91), (8.0, 79.32), (24.55, 79.32), (59.83, 35.26), (69.66, 35.26), (69.66, 46.68), (92.0, 28.08), (69.66, 9.47)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(51.93, 54.87), (59.83, 64.74), (69.66, 64.74), (69.66, 53.32), (92.0, 71.92), (69.66, 90.53), (69.66, 79.15), (53.4, 79.15), (42.99, 66.09)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(26.19, 45.13), (18.21, 35.09), (8.0, 35.09), (8.0, 20.68), (24.55, 20.68), (35.13, 33.91)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
