# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: vertex_ai (default 3-tone blue variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import GCP_TECH_LIGHT, GCP_TECH_MED_LIGHT, GCP_TECH_MID, WHITE, draw_capsule, fill_style, setup_icon

setup_icon()

col_w = 6.6
dot_r = 3.3

# 1. Bottom V-arms
draw_capsule((19.0, 40.0), (50.0, 17.0), width_units=6.8, color=GCP_TECH_LIGHT)
draw_capsule((81.0, 40.0), (50.0, 17.0), width_units=6.8, color=GCP_TECH_MED_LIGHT)

# 2. Bottom apex ring in GCP_TECH_MID with white center
circle((50.0, 17.0), radius=6.4, style=fill_style(GCP_TECH_MID))
circle((50.0, 17.0), radius=2.6, style=fill_style(WHITE))

# 3. Five vertical columns of dots and capsules
# Column 1 (x=25.0, GCP_TECH_LIGHT)
draw_capsule((25.0, 75.0), (25.0, 85.0), width_units=col_w, color=GCP_TECH_LIGHT)
for y in (65.0, 56.0, 47.0):
    circle((25.0, y), radius=dot_r, style=fill_style(GCP_TECH_LIGHT))

# Column 2 (x=37.5, GCP_TECH_LIGHT)
for y in (76.0, 67.0):
    circle((37.5, y), radius=dot_r, style=fill_style(GCP_TECH_LIGHT))
draw_capsule((37.5, 48.0), (37.5, 58.0), width_units=col_w, color=GCP_TECH_LIGHT)
circle((37.5, 39.0), radius=dot_r, style=fill_style(GCP_TECH_LIGHT))

# Column 3 (x=50.0, GCP_TECH_MED_LIGHT)
for y in (67.0, 58.0):
    circle((50.0, y), radius=dot_r, style=fill_style(GCP_TECH_MED_LIGHT))
draw_capsule((50.0, 39.0), (50.0, 49.0), width_units=col_w, color=GCP_TECH_MED_LIGHT)
circle((50.0, 30.0), radius=dot_r, style=fill_style(GCP_TECH_MED_LIGHT))

# Column 4 (x=62.5, GCP_TECH_MID)
circle((62.5, 76.0), radius=dot_r, style=fill_style(GCP_TECH_MID))
draw_capsule((62.5, 57.0), (62.5, 67.0), width_units=col_w, color=GCP_TECH_MID)
for y in (48.0, 39.0):
    circle((62.5, y), radius=dot_r, style=fill_style(GCP_TECH_MID))

# Column 5 (x=75.0, GCP_TECH_MID)
circle((75.0, 85.0), radius=dot_r, style=fill_style(GCP_TECH_MID))
draw_capsule((75.0, 66.0), (75.0, 76.0), width_units=col_w, color=GCP_TECH_MID)
for y in (56.0, 47.0):
    circle((75.0, y), radius=dot_r, style=fill_style(GCP_TECH_MID))

save()
