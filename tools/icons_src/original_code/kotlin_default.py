# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: kotlin."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_seam = 1.3

CORAL_PINK = "#F24D5E"
MAGENTA = "#DA51E6"
PURPLE = "#8057F2"

# Classic 3 diagonal Kotlin 'K' facets scaled inside [10.0, 90.0]
top_left = [(10.0, 50.0), (10.0, 90.0), (50.0, 90.0)]
middle = [(10.0, 10.0), (10.0, 50.0), (50.0, 90.0), (90.0, 90.0)]
bottom_right = [(10.0, 10.0), (50.0, 50.0), (90.0, 10.0)]
outer = [(10.0, 10.0), (10.0, 90.0), (90.0, 90.0), (50.0, 50.0), (90.0, 10.0)]

# 1. Flat pastel fills
polygon(top_left, style=Icon.no_border_fill(CORAL_PINK))
polygon(middle, style=Icon.no_border_fill(MAGENTA))
polygon(bottom_right, style=Icon.no_border_fill(PURPLE))

# 2. Inner diagonal facet seams (exact geometric capsules, no projecting cap overshoot)
Icon.draw_capsule((10.0, 50.0), (50.0, 90.0), width_units=w_seam, color=Icon.DARK)
Icon.draw_capsule((10.0, 10.0), (50.0, 50.0), width_units=w_seam, color=Icon.DARK)

# 3. Crisp outer silhouette outline (exact geometric capsules with round joins)
for i in range(len(outer)):
    Icon.draw_capsule(outer[i], outer[(i + 1) % len(outer)], width_units=w_outer, color=Icon.DARK)

save()
