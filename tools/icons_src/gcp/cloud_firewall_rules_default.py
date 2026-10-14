# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_firewall_rules (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import GCP_TECH_MID, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(8.0, 92.0), (45.34, 92.0), (45.34, 82.68), (8.0, 82.68)], style=fill_style(GCP_TECH_MID))
polygon([(8.0, 17.32), (45.34, 17.32), (45.34, 8.0), (8.0, 8.0)], style=fill_style(GCP_TECH_MID))
polygon([(8.0, 54.66), (45.34, 54.66), (45.34, 45.34), (8.0, 45.34)], style=fill_style(GCP_TECH_MID))
polygon([(54.66, 92.0), (92.0, 92.0), (92.0, 82.68), (54.66, 82.68)], style=fill_style(GCP_TECH_MID))
polygon([(54.66, 17.32), (92.0, 17.32), (92.0, 8.0), (54.66, 8.0)], style=fill_style(GCP_TECH_MID))
polygon([(54.66, 54.66), (92.0, 54.66), (92.0, 45.34), (54.66, 45.34)], style=fill_style(GCP_TECH_MID))
polygon([(31.31, 73.35), (68.65, 73.35), (68.65, 64.03), (31.31, 64.03)], style=fill_style(GCP_TECH_MID))
polygon([(31.31, 36.01), (68.65, 36.01), (68.65, 26.69), (31.31, 26.69)], style=fill_style(GCP_TECH_MID))
polygon([(8.0, 73.35), (21.99, 73.35), (21.99, 64.03), (8.0, 64.03)], style=fill_style(GCP_TECH_MID))
polygon([(8.0, 36.01), (21.99, 36.01), (21.99, 26.69), (8.0, 26.69)], style=fill_style(GCP_TECH_MID))
polygon([(78.01, 73.35), (92.0, 73.35), (92.0, 64.03), (78.01, 64.03)], style=fill_style(GCP_TECH_MID))
polygon([(78.01, 36.01), (92.0, 36.01), (92.0, 26.69), (78.01, 26.69)], style=fill_style(GCP_TECH_MID))
save()
# fmt: on
