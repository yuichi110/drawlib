# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Constants module."""

from __future__ import annotations

import importlib.metadata
import os
from typing import Final

LIB_NAME: Final[str] = "drawlib"
LIB_VERSION: Final[str] = importlib.metadata.version(LIB_NAME)

ASSETS_DIR_PATH: Final[str] = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "_cached_assets"))
FONT_DIR_PATH: Final[str] = os.path.join(ASSETS_DIR_PATH, "fonts")
FONT_ICON_DIR_PATH: Final[str] = os.path.join(ASSETS_DIR_PATH, "fonticons")
ICON_DIR_PATH: Final[str] = os.path.join(ASSETS_DIR_PATH, "icons")
MAP_DIR_PATH: Final[str] = os.path.join(ASSETS_DIR_PATH, "maps")
RULES_DIR_PATH: Final[str] = os.path.join(ASSETS_DIR_PATH, "rules")
