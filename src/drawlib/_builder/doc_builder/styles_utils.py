# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""External Python styles and utils loader for doc_builder and drawing blocks."""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional

import drawlib.styles
import drawlib.utils


def _inject_shared_globals(shared_globals: Dict[str, Any]) -> None:
    """Pre-populate shared globals with standard drawlib facades and wildcard imports."""
    exec(
        "from drawlib import (builder, canvas, charts, colors, diagrams, fonts, icons, "
        "images, lines, math, preset_styles, shapes, smartarts, styles, text, tools, types, utils)\n"
        "from drawlib.canvas import *\n"
        "from drawlib.shapes import *\n"
        "from drawlib.lines import *\n"
        "from drawlib.text import *\n"
        "from drawlib.icons import *\n"
        "from drawlib.images import *\n"
        "from drawlib.preset_styles import *\n"
        "from drawlib.smartarts import *\n"
        "from drawlib.fonts import *\n"
        "from drawlib.colors import *\n"
        "from drawlib.types import *\n"
        "from drawlib.math import *\n"
        "from drawlib.builder import *\n"
        "from drawlib.styles import styles, colors\n",
        shared_globals,
    )


def load_styles(
    styles_path: Optional[str] = None,
    shared_globals: Optional[Dict[str, Any]] = None,
) -> None:
    """Load an external Python styles script and apply it to drawlib.styles.

    If styles_path is None or empty, drawlib.styles is reset to its default theme.
    When a styles_path is provided, the script is executed in a namespace initialized with
    drawlib.styles.styles and drawlib.styles.colors, and any overridden `styles` or `colors`
    are applied to drawlib.styles.

    Args:
        styles_path (Optional[str]): Path to the Python styles script, or None.
        shared_globals (Optional[Dict[str, Any]]): Optional shared execution globals dictionary.

    Raises:
        FileNotFoundError: If the specified styles_path does not exist.
    """
    drawlib.styles._reset_styles()

    if shared_globals is not None:
        _inject_shared_globals(shared_globals)

    if not styles_path:
        return

    styles_abs_path = os.path.abspath(styles_path)
    if not os.path.exists(styles_abs_path):
        raise FileNotFoundError(f'Styles file "{styles_abs_path}" does not exist.')

    styles_dir = os.path.dirname(styles_abs_path)
    if styles_dir not in sys.path:
        sys.path.insert(0, styles_dir)

    user_globals: dict[str, Any] = {
        "__file__": styles_abs_path,
        "__name__": "drawlib_styles",
        "styles": drawlib.styles.styles,
    }

    current_cwd = os.getcwd()
    try:
        os.chdir(styles_dir)
        with open(styles_abs_path, "r", encoding="utf-8") as f:
            styles_code = f.read()

        compiled_code = compile(styles_code, filename=styles_abs_path, mode="exec")
        exec(compiled_code, user_globals)
    finally:
        os.chdir(current_cwd)

    custom_colors = user_globals["colors"] if "colors" in user_globals else None
    if "styles" in user_globals:
        drawlib.styles._set_active_styles(user_globals["styles"], custom_colors)
    elif custom_colors is not None:
        drawlib.styles._set_active_styles(drawlib.styles.styles, custom_colors)

    if shared_globals is not None:
        shared_globals["styles"] = drawlib.styles.styles
        shared_globals["colors"] = drawlib.styles.colors


def load_utils(
    utils_path: Optional[str] = None,
    shared_globals: Optional[Dict[str, Any]] = None,
) -> None:
    """Load an external Python utils script and attach its members to drawlib.utils.

    If utils_path is None or empty, drawlib.utils is reset to its default state.
    When a utils_path is provided, the script is executed, and all top-level attributes
    (excluding those starting with '_') are attached to drawlib.utils.

    Args:
        utils_path (Optional[str]): Path to the Python utils script, or None.
        shared_globals (Optional[Dict[str, Any]]): Optional shared execution globals dictionary.

    Raises:
        FileNotFoundError: If the specified utils_path does not exist.
    """
    drawlib.utils._reset_utils()

    if not utils_path:
        return

    utils_abs_path = os.path.abspath(utils_path)
    if not os.path.exists(utils_abs_path):
        raise FileNotFoundError(f'Utils file "{utils_abs_path}" does not exist.')

    utils_dir = os.path.dirname(utils_abs_path)
    if utils_dir not in sys.path:
        sys.path.insert(0, utils_dir)

    user_globals: dict[str, Any] = {
        "__file__": utils_abs_path,
        "__name__": "drawlib_utils",
    }

    current_cwd = os.getcwd()
    try:
        os.chdir(utils_dir)
        with open(utils_abs_path, "r", encoding="utf-8") as f:
            utils_code = f.read()

        compiled_code = compile(utils_code, filename=utils_abs_path, mode="exec")
        exec(compiled_code, user_globals)
    finally:
        os.chdir(current_cwd)

    for key, val in user_globals.items():
        if not key.startswith("_"):
            setattr(drawlib.utils, key, val)
            if shared_globals is not None:
                shared_globals[key] = val


def load_styles_and_utils(
    styles_path: Optional[str] = None,
    utils_path: Optional[str] = None,
    shared_globals: Optional[Dict[str, Any]] = None,
) -> None:
    """Load both external styles and utils scripts.

    Args:
        styles_path (Optional[str]): Path to the Python styles script, or None.
        utils_path (Optional[str]): Path to the Python utils script, or None.
        shared_globals (Optional[Dict[str, Any]]): Optional shared execution globals dictionary.
    """
    load_styles(styles_path=styles_path, shared_globals=shared_globals)
    load_utils(utils_path=utils_path, shared_globals=shared_globals)
