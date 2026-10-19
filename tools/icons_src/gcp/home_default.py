# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: home (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(55.6, 77.47), (44.4, 77.47), (18.5, 53.67), (18.5, 10.98), (39.5, 10.98), (39.5, 39.67), (60.5, 39.67), (60.5, 10.98), (81.5, 10.98), (81.5, 53.67)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(50.0, 77.47), (44.4, 77.47), (18.5, 53.67), (18.5, 10.98), (39.5, 10.98), (39.5, 39.67), (50.0, 39.67)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(53.85, 75.72), (18.5, 36.87), (18.5, 50.17), (51.75, 79.57)], style=Icon.fill_style(Gcp.TECH_DARK))
polygon([(50.0, 89.02), (8.0, 47.02), (14.3, 40.72), (50.0, 76.42), (85.7, 40.72), (92.0, 47.02)], style=Icon.fill_style(Gcp.TECH_LIGHT))
save()
# fmt: on
