# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: apisix."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_crease = 1.8

v_bl_out = (9.00, 15.54)
v_top = (50.66, 84.46)
v_br_out = (91.00, 15.54)
v_br_in = (71.05, 15.54)
v_crotch = (50.66, 47.67)
v_bl_in = (27.84, 15.54)
v_fold = (42.91, 59.20)

# 1. Inner fold (bottom-left darker coral)
inner_fold = [v_bl_out, v_fold, v_crotch, v_bl_in]
polygon(inner_fold, style=Icon.no_border_fill(Colors.Red4))

# 2. Left leg / center ribbon (light pastel coral)
left_leg = [v_bl_out, v_top, v_br_in, v_crotch, v_fold]
polygon(left_leg, style=Icon.no_border_fill(Colors.Red2))

# 3. Right leg (medium pastel red)
right_leg = [v_top, v_br_out, v_br_in]
polygon(right_leg, style=Icon.no_border_fill(Colors.Red3))

# 4. Internal ribbon crease lines
Icon.draw_round_polyline([v_bl_out, v_fold, v_crotch], width_units=w_crease, color=Icon.DARK)
Icon.draw_round_polyline([v_top, v_br_in], width_units=w_crease, color=Icon.DARK)

# 5. Outer chevron outline
chevron_outer = [v_bl_out, v_top, v_br_out, v_br_in, v_crotch, v_bl_in]
Icon.draw_round_polyline(chevron_outer, width_units=w, color=Icon.DARK, closed=True)

save()
