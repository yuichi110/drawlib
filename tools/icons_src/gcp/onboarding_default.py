# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: onboarding (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(84.3, 57.15), (84.3, 30.74), (92.0, 30.74), (92.0, 61.55)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(92.0, 61.55), (84.3, 57.15), (84.3, 53.48)], style=Icon.fill_style(Gcp.TECH_DARK))
polygon([(8.0, 61.55), (50.18, 38.45), (84.3, 57.15), (92.0, 61.55), (50.18, 84.3)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(8.0, 61.55), (50.18, 38.45), (50.18, 84.3)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(23.41, 45.41), (23.41, 30.38), (50.18, 15.7), (76.59, 30.38), (76.59, 45.41), (50.18, 30.74)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(23.41, 30.38), (50.18, 15.7), (50.18, 30.74), (23.41, 45.41)], style=Icon.fill_style(Gcp.TECH_LIGHT))
save()
# fmt: on
