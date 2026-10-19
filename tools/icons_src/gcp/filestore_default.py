# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: filestore (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(33.2, 50.0), (66.8, 50.0), (58.4, 41.6), (41.6, 41.6)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(29.0, 83.6), (71.0, 83.6), (75.2, 75.2), (24.8, 75.2)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(16.4, 71.0), (83.6, 71.0), (87.8, 62.6), (12.2, 62.6)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(92.0, 16.4), (92.0, 54.2), (66.8, 54.2), (58.4, 41.6), (41.6, 41.6), (33.2, 54.2), (8.0, 54.2), (8.0, 16.4)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
