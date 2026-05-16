# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for icon() function and icon modules"""

from drawlib.v0_2.private.l6_icons import (
    _phosphor as icon_phosphor,
)
from drawlib.v0_2.private.l6_icons._icon import (
    icon,
)

__all__ = [
    "icon",
    "icon_phosphor",
]
