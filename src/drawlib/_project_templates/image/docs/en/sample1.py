# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Basic architecture diagram using Drawlib core primitives."""

from __future__ import annotations

from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# Setup canvas: 100 wide x 45 high
setup(width=100, height=45)

# Standard shapes drawn with primitive functions
rectangle(
    (25, 22.5),
    width=28,
    height=18,
    style=Styles.PrimaryFlat,
    text="Client App",
    textstyle=Styles.WhiteBold,
)
rectangle(
    (75, 22.5),
    width=28,
    height=18,
    style=Styles.AccentFlat,
    text="Backend API",
    textstyle=Styles.WhiteBold,
)

# Connecting line with arrow
line((39, 22.5), (61, 22.5), arrowhead="->", style=Styles.PrimaryBold)

# Save the rendered canvas image
save()
