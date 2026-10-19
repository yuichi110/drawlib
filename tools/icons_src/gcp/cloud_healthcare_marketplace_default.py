# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_healthcare_marketplace (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(27.09, 57.64), (27.09, 19.45), (27.13, 18.67), (27.25, 17.92), (27.43, 17.18), (27.69, 16.48), (28.01, 15.81), (28.4, 15.18), (28.83, 14.6), (29.33, 14.05), (29.87, 13.56), (30.46, 13.12), (31.09, 12.74), (31.75, 12.42), (32.46, 12.16), (33.19, 11.97), (33.95, 11.86), (34.73, 11.82), (65.27, 11.82), (66.05, 11.86), (66.81, 11.97), (67.54, 12.16), (68.25, 12.42), (68.91, 12.74), (69.54, 13.12), (70.13, 13.56), (70.67, 14.05), (71.17, 14.6), (71.6, 15.18), (71.99, 15.81), (72.31, 16.48), (72.57, 17.18), (72.75, 17.92), (72.87, 18.67), (72.91, 19.45), (72.91, 57.64)], style=Icon.stroke_style(Gcp.TECH_MID, width_units=7.64))
polygon([(46.18, 50.0), (53.82, 50.0), (53.82, 19.45), (46.18, 19.45)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(34.73, 38.55), (65.27, 38.55), (65.27, 30.91), (34.73, 30.91)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(23.27, 92.0), (76.73, 92.0), (76.73, 84.36), (23.27, 84.36)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(23.27, 76.73), (76.73, 76.73), (76.73, 69.09), (23.27, 69.09)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
