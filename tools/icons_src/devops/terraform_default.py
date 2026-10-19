# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: terraform (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(63.67, 37.73), (86.08, 50.66), (86.08, 76.55), (63.67, 63.6)], style=Icon.fill_style('#4040B2'))
polygon([(38.79, 76.55), (61.21, 63.6), (61.21, 37.73), (38.79, 50.67)], style=Icon.fill_style('#5C4EE5'))
polygon([(13.92, 65.12), (36.33, 52.17), (36.33, 78.06), (13.92, 91.0)], style=Icon.fill_style('#5C4EE5'))
polygon([(38.79, 21.94), (61.21, 9.0), (61.21, 34.88), (38.79, 47.83)], style=Icon.fill_style('#5C4EE5'))
save()
# fmt: on
