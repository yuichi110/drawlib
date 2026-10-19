# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: datapol (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(40.13, 84.15), (74.95, 84.15), (74.95, 76.29), (40.13, 76.29)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(18.71, 52.73), (53.53, 52.73), (53.53, 44.88), (18.71, 44.88)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(40.13, 23.92), (74.95, 23.92), (74.95, 16.06), (40.13, 16.06)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(27.19, 44.2), (40.84, 21.06), (33.87, 17.16), (20.22, 40.3)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(28.16, 54.58), (41.81, 77.72), (35.05, 81.54), (21.4, 58.4)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(31.02, 68.23), (24.04, 80.03), (31.02, 92.0), (44.92, 92.0), (51.85, 80.03), (44.92, 68.23)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(55.08, 36.81), (48.15, 48.57), (55.08, 60.58), (68.98, 60.58), (75.96, 48.57), (68.98, 36.81)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(14.93, 36.81), (8.0, 48.57), (14.93, 60.58), (28.83, 60.58), (35.76, 48.57), (28.83, 36.81)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(71.17, 68.23), (64.24, 80.03), (71.17, 92.0), (85.07, 92.0), (92.0, 80.03), (85.07, 68.23)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(71.17, 8.0), (64.24, 19.8), (71.17, 31.77), (85.07, 31.77), (92.0, 19.8), (85.07, 8.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(31.02, 8.0), (24.04, 19.8), (31.02, 31.77), (44.92, 31.77), (51.85, 19.8), (44.92, 8.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
save()
# fmt: on
