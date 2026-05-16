# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Constants module."""

import os

import drawlib.assets.v0_2.fonticons
import drawlib.assets.v0_2.fonts

FONT_DIR_PATH = os.path.dirname(drawlib.assets.v0_2.fonts.__file__)
FONT_ICON_DIR_PATH = os.path.dirname(drawlib.assets.v0_2.fonticons.__file__)
