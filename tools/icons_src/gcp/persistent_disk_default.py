# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: persistent_disk (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(67.51, 42.99), (67.51, 23.75), (16.74, 23.75), (16.74, 8.0), (83.26, 8.0), (83.26, 42.99)], style=fill_style(GCP_TECH_MID))
polygon([(32.49, 57.01), (32.49, 76.25), (83.26, 76.25), (83.26, 92.0), (16.74, 92.0), (16.74, 57.01)], style=fill_style(GCP_TECH_LIGHT))
polygon([(41.26, 67.51), (41.26, 48.24), (16.74, 48.24), (16.74, 32.49), (58.74, 32.49), (58.74, 51.76), (83.26, 51.76), (83.26, 67.51)], style=fill_style(GCP_TECH_MED_LIGHT))
save()
# fmt: on
