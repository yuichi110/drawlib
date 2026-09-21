# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public icons module for drawlib."""

import sys

from drawlib._icons import (
    icon,
    icon_phosphor,
    phosphor,
)

# Allow submodule style imports: `import drawlib.icons.phosphor`
sys.modules["drawlib.icons.phosphor"] = phosphor
sys.modules["drawlib.icons.icon_phosphor"] = icon_phosphor

__all__ = [
    "icon",
    "icon_phosphor",
    "phosphor",
]
