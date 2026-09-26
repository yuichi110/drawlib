# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""External Python configuration script loader for doc_builder."""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional

import drawlib.config


def load_config(
    config_path: Optional[str] = None,
    shared_globals: Optional[Dict[str, Any]] = None,
) -> None:
    """Load an external Python config script and merge its attributes onto drawlib.config.

    If config_path is None or empty, drawlib.config is reset to its default attributes.
    When a config_path is provided, the script is executed in a namespace initialized with
    drawlib.config's existing attributes, and any newly defined or overridden attributes
    are applied to drawlib.config.

    Args:
        config_path (Optional[str]): Path to the Python config script, or None.
        shared_globals (Optional[Dict[str, Any]]): Optional shared execution globals dictionary.

    Raises:
        FileNotFoundError: If the specified config_path does not exist.
    """
    drawlib.config._reset_config()

    if not config_path:
        return

    config_abs_path = os.path.abspath(config_path)
    if not os.path.exists(config_abs_path):
        raise FileNotFoundError(f'Config file "{config_abs_path}" does not exist.')

    config_dir = os.path.dirname(config_abs_path)
    if config_dir not in sys.path:
        sys.path.insert(0, config_dir)

    # Initialize execution namespace with drawlib.config defaults
    user_globals: dict[str, Any] = {
        "__file__": config_abs_path,
        "__name__": "drawlib.config",
    }
    for key, val in vars(drawlib.config).items():
        if not key.startswith("_"):
            user_globals[key] = val

    current_cwd = os.getcwd()
    try:
        os.chdir(config_dir)
        with open(config_abs_path, "r", encoding="utf-8") as f:
            config_code = f.read()

        compiled_code = compile(config_code, filename=config_abs_path, mode="exec")
        exec(compiled_code, user_globals)
    finally:
        os.chdir(current_cwd)

    # Merge user attributes onto drawlib.config
    for key, val in user_globals.items():
        if not key.startswith("_"):
            setattr(drawlib.config, key, val)
