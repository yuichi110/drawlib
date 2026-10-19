# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: ai_hub (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(86.5, 48.19), (50.0, 29.92), (50.0, 8.0), (86.5, 26.27)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(71.92, 66.42), (71.92, 48.19), (86.5, 55.46), (86.5, 73.73)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(50.0, 37.23), (64.62, 44.5), (64.62, 62.77), (50.0, 55.46)], style=Icon.fill_style(Gcp.TECH_MID))
polygon([(28.08, 81.04), (13.5, 73.73), (28.08, 66.42), (42.69, 73.73)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(50.0, 92.0), (35.38, 84.69), (50.0, 77.38), (71.92, 66.42), (86.5, 73.73)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(50.0, 70.08), (35.38, 62.77), (50.0, 55.46), (64.62, 62.77)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(35.38, 37.4), (35.38, 15.48), (50.0, 8.0), (50.0, 29.92)], holes=[[(46.35, 15.48), (39.04, 19.13), (39.04, 29.92), (46.35, 26.27)]], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(13.5, 73.73), (13.5, 26.27), (28.08, 18.96), (28.08, 66.42)], holes=[[(24.46, 26.27), (17.11, 29.92), (17.11, 71.92), (24.46, 68.27)]], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(35.38, 62.6), (50.0, 55.46), (50.0, 37.4), (35.38, 44.5)], holes=[[(46.35, 44.33), (46.35, 56.93), (39.04, 60.71), (39.04, 48.11)]], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
save()
# fmt: on
