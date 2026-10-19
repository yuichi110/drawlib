# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: automl (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(18.5, 30.18), (39.5, 66.21), (46.51, 66.21), (53.49, 77.01), (46.43, 87.8), (29.0, 87.8), (8.0, 51.76)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(60.5, 77.01), (53.49, 66.21), (67.51, 66.21), (74.49, 77.01), (67.51, 87.8), (53.49, 87.8)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(81.5, 69.82), (60.5, 33.79), (53.49, 33.79), (46.51, 22.99), (53.57, 12.2), (71.0, 12.2), (92.0, 48.24)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(46.51, 12.2), (39.5, 22.99), (46.51, 33.79), (32.49, 33.79), (25.51, 22.99), (32.49, 12.2)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
