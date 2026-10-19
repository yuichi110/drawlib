# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_cdn (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Gcp, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 92.0), (50.0, 81.88), (63.15, 68.35), (63.15, 78.52)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(81.5, 50.0), (68.4, 36.85), (78.9, 36.85), (92.0, 50.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(18.5, 50.0), (31.65, 36.85), (21.15, 36.85), (8.0, 50.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(50.0, 8.0), (50.0, 18.12), (63.15, 31.6), (63.15, 21.48)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(50.0, 92.0), (36.9, 78.52), (36.9, 68.35), (50.0, 81.88)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(78.9, 63.1), (68.4, 63.1), (81.5, 50.0), (92.0, 50.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(21.15, 63.1), (31.65, 63.1), (18.5, 50.0), (8.0, 50.0)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(50.0, 8.0), (36.9, 21.48), (36.9, 31.6), (50.0, 18.12)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(63.15, 36.85), (36.9, 36.85), (36.9, 63.1), (63.15, 63.1)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(63.15, 63.1), (63.15, 36.85), (36.9, 36.85)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(63.15, 63.1), (63.15, 36.85), (50.0, 50.0)], style=Icon.fill_style(Gcp.TECH_MID))
save()
# fmt: on
