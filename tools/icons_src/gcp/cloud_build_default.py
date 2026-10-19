# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_build (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(49.98, 31.73), (65.06, 40.43), (65.06, 57.82), (60.0, 60.77), (44.92, 34.64)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(34.9, 57.82), (34.9, 40.43), (39.96, 37.51), (55.08, 63.6), (49.98, 66.56)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(47.02, 26.55), (28.95, 37.0), (28.95, 57.82), (12.88, 67.11), (12.88, 27.7), (47.02, 8.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(31.9, 62.96), (49.98, 73.41), (68.06, 62.96), (84.16, 72.25), (49.98, 92.0), (15.8, 72.25)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(71.01, 37.0), (52.93, 26.55), (52.93, 8.0), (87.12, 27.7), (87.12, 67.11), (71.01, 57.82)], style=Icon.fill_style(Gcp.TECH_LIGHT))
save()
# fmt: on
