# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Official Drawlib wordmark for dark backgrounds (transparent)."""

from drawlib.canvas import save, setup
from drawlib.styles import Colors
from drawlib.utils import draw_logo_text

setup(width=210, height=66, dpi=200, color=Colors.Canvas, alpha=0.0)

draw_logo_text(canvas_width=210.0, is_dark=True)

save()
