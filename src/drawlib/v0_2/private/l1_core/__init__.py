# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for core drawing action modules."""

from drawlib.v0_2.private.l1_core._const import (
    FONT_DIR_PATH,
    FONT_ICON_DIR_PATH,
)
from drawlib.v0_2.private.l1_core._decorator import guarded
from drawlib.v0_2.private.l1_core._logging import logger
from drawlib.v0_2.private.l1_core._settings import dutil_settings
from drawlib.v0_2.private.l1_core._utils import (
    get_script_function_name,
    get_script_path,
    get_script_relative_path,
)

__all__ = [
    # _const.py
    "FONT_DIR_PATH",
    "FONT_ICON_DIR_PATH",
    # _decorator.py
    "guarded",
    # _logging.py
    "logger",
    # _settings.py
    "dutil_settings",
    # _utils.py
    "get_script_function_name",
    "get_script_path",
    "get_script_relative_path",
]
