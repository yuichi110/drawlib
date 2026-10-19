# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: database_migration_service (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(18.52, 68.53), (38.73, 80.21), (38.73, 91.94), (8.0, 74.22), (9.68, 72.15), (16.66, 68.36)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(38.73, 26.9), (8.0, 44.61), (8.0, 55.78), (38.73, 38.02)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(38.73, 19.27), (8.0, 37.07), (8.0, 25.86), (38.73, 8.11)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(38.73, 56.81), (18.52, 68.53), (8.0, 74.22), (8.0, 63.45), (38.73, 45.69)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(38.73, 8.06), (68.9, 25.3), (68.9, 36.64), (38.73, 19.4)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(38.73, 38.15), (68.9, 55.39), (77.86, 55.39), (77.86, 45.35), (70.62, 45.35), (38.73, 26.86)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(38.73, 45.78), (70.67, 64.22), (81.18, 64.22), (81.18, 58.36), (92.0, 69.18), (81.18, 79.95), (81.18, 74.26), (68.81, 74.26), (63.51, 71.16), (58.94, 68.53), (47.22, 61.77), (38.6, 56.81)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(38.73, 80.21), (52.35, 72.33), (62.52, 78.19), (38.73, 91.94)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
