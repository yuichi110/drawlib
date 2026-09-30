# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Advanced architecture diagram using reusable helpers and local assets."""

from __future__ import annotations

from drawlib.canvas import save, setup
from drawlib.images import image
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

# Setup canvas: 110 wide x 52 high
setup(width=110, height=52)

# Service nodes drawn using reusable helper from utils.py
service_card((20, 24), title="Web Client", subtitle="Browser / App")
service_card((55, 24), title="Linux Server", subtitle="Ubuntu / Nginx", style=Styles.accent_flat)
service_card((90, 24), title="Database", subtitle="PostgreSQL", style=Styles.secondary_flat)

# Connections with protocol labels
connect((32, 24), (43, 24), label="HTTPS")
connect((67, 24), (78, 24), label="SQL")

# Embedded local image asset from _assets/ directory
image((55, 41), width=8, image="_assets/linux.png")

# Save the rendered canvas image
save()
