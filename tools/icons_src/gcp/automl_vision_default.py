# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: automl_vision (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(56.05, 42.57), (35.85, 42.44), (44.16, 57.31), (64.32, 57.43)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(28.24, 18.67), (32.23, 11.74), (72.09, 11.74), (92.0, 46.26), (84.02, 60.08), (64.11, 25.6), (32.23, 25.6)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(71.76, 81.33), (67.77, 88.26), (27.91, 88.26), (8.0, 53.74), (15.98, 39.92), (35.89, 74.4), (67.77, 74.4)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
