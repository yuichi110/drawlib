# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""External Python configuration script loader for doc_builder."""

import os
import sys
from typing import Any, Dict, Optional


def load_config(config_path: Optional[str], shared_globals: Dict[str, Any]) -> None:
    """Load an external Python config script into shared_globals dictionary.

    Args:
        config_path (Optional[str]): Path to the Python config script, or None.
        shared_globals (Dict[str, Any]): Global namespace dictionary where symbols will be injected.

    Raises:
        FileNotFoundError: If the specified config_path does not exist.
    """
    # Always import drawlib domain module functions into shared_globals by default
    exec(
        "from drawlib import canvas, colors, doc_builder, fonts, icons, images, lines, math, "
        "preset_styles, shapes, smartarts, text, types\n"
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
        "from drawlib.doc_builder import *\n"
        "styles = get_styles('essentials')\n",
        shared_globals,
    )

    if not config_path:
        return

    config_abs_path = os.path.abspath(config_path)
    if not os.path.exists(config_abs_path):
        raise FileNotFoundError(f'Config file "{config_abs_path}" does not exist.')

    config_dir = os.path.dirname(config_abs_path)
    if config_dir not in sys.path:
        sys.path.insert(0, config_dir)

    shared_globals["__file__"] = config_abs_path
    shared_globals["__name__"] = "__main__"

    current_cwd = os.getcwd()
    try:
        os.chdir(config_dir)
        with open(config_abs_path, "r", encoding="utf-8") as f:
            config_code = f.read()

        # compile with filename to enable inspect.stack() path resolution in drawlib
        compiled_code = compile(config_code, filename=config_abs_path, mode="exec")
        exec(compiled_code, shared_globals)
    finally:
        os.chdir(current_cwd)
