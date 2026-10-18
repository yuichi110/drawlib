# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: asana."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import DARK, fill_style, setup_icon

setup_icon()
w = 2.0
r = 16.87
coral = "#F59898"

for center in ((71.93, 31.02), (28.07, 31.02), (50.0, 68.98)):
    circle(center, radius=r, style=fill_style(coral, border_color=DARK, border_units=w))

save()
