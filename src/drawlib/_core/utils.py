# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Core utilities facade module."""

from drawlib._core.l1_core import (
    FONT_DIR_PATH,
    FONT_ICON_DIR_PATH,
    ICON_DIR_PATH,
    RULES_DIR_PATH,
    dutil_settings,
    get_script_function_name,
    get_script_path,
    get_script_relative_path,
    logger,
)
from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_external import (
    download_all_assets,
    download_all_fonts,
    download_all_icons,
    download_if_not_exist,
    purge_font_cache,
)
from drawlib._core.l4_canvas_utils import (
    ColorUtil,
    ImageUtil,
    LineUtil,
    ShapeUtil,
    TextUtil,
    get_angle,
    get_center_and_size,
    get_distance,
    get_rotated_path_points,
    get_rotated_points,
    minus_2points,
    plus_2points,
)

__all__ = [
    "ColorUtil",
    "FONT_DIR_PATH",
    "FONT_ICON_DIR_PATH",
    "ICON_DIR_PATH",
    "ImageUtil",
    "LineUtil",
    "RULES_DIR_PATH",
    "ShapeUtil",
    "StaticContainer",
    "TextUtil",
    "download_all_assets",
    "download_all_fonts",
    "download_all_icons",
    "download_if_not_exist",
    "dutil_settings",
    "get_angle",
    "get_center_and_size",
    "get_distance",
    "get_rotated_path_points",
    "get_rotated_points",
    "get_script_function_name",
    "get_script_path",
    "get_script_relative_path",
    "logger",
    "minus_2points",
    "plus_2points",
    "purge_font_cache",
]
