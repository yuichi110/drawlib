# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: data_catalog (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(8.0, 61.79), (18.88, 81.17), (32.86, 81.17), (32.86, 72.62), (23.77, 72.62), (17.73, 61.93), (21.44, 55.71), (14.17, 51.46)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(61.43, 44.88), (72.85, 51.46), (84.28, 44.88), (84.28, 31.67), (72.85, 25.09), (61.43, 31.67)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(15.72, 44.88), (27.15, 51.46), (38.57, 44.88), (38.57, 31.67), (27.15, 25.09), (15.72, 31.67)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(38.57, 83.64), (50.0, 90.22), (61.43, 83.64), (61.43, 70.47), (50.0, 63.85), (38.57, 70.47)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(72.85, 51.46), (84.28, 44.88), (84.28, 31.67), (72.85, 25.09)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(27.15, 51.46), (38.57, 44.88), (38.57, 31.67), (27.15, 25.09)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(50.0, 90.22), (61.43, 83.64), (61.43, 70.47), (50.0, 63.85)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(78.56, 55.71), (82.27, 61.88), (76.23, 72.62), (67.14, 72.62), (67.14, 81.17), (81.12, 81.17), (92.0, 61.79), (85.83, 51.46)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(39.08, 9.78), (32.31, 21.03), (39.63, 25.28), (43.88, 18.33), (55.99, 18.33), (60.28, 25.28), (67.6, 21.07), (60.79, 9.78)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
