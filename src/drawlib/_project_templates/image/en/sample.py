# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Sample Drawlib drawing script."""

from __future__ import annotations

from drawlib.canvas import save, setup
from drawlib.config import styles
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

# Setup canvas: 100 wide x 50 high
setup(width=100, height=50)

# Draw shapes
rectangle((25, 25), width=28, height=18, style=styles.blue_flat, text="Service A", textstyle=styles.white_bold)
rectangle((75, 25), width=28, height=18, style=styles.green_flat, text="Service B", textstyle=styles.white_bold)

# Draw connecting line with arrow
line((39, 25), (61, 25), arrowhead="->", style=styles.bold)
text((50, 28), "gRPC", style=styles.primary)

# Save the rendered canvas image
save()
