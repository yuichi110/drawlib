# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: ANN001, ANN201, ANN401

"""Utility module."""

import functools
import inspect
import math
import os
import os.path
import shutil
import sys
import traceback
from typing import Callable, List, ParamSpec, Tuple, TypeVar, Union

from pydantic import ConfigDict, InstanceOf, validate_call

import drawlib.assets.v0_2.fonticons
import drawlib.assets.v0_2.fonts
from drawlib.v0_2.private.l1_core._common import get_package_root_path, is_path_under
from drawlib.v0_2.private.l1_core._decorator import guarded
from drawlib.v0_2.private.l1_core._logging import logger
from drawlib.v0_2.private.l1_core._settings import dutil_settings


@guarded
def get_script_path() -> str:
    """Retrieve the absolute path of the user script that calls this function.

    Returns:
        str: Absolute path of the user script.

    Raises:
        FileNotFoundError: If the script path cannot be determined.

    """
    package_root = get_package_root_path()
    script_path = ""
    for frame in inspect.stack():
        file = frame.filename
        if not os.path.isfile(file):
            continue
        if "site-packages" in file:
            continue
        if is_path_under(package_root, file):
            continue
        script_path = file
        break

    if not script_path:
        message = "Critical Error. Unable to detect call script file"
        raise FileNotFoundError(message)

    return script_path


@guarded
def get_script_relative_path(path: str) -> str:
    """Construct the absolute file path from a script file path.

    Args:
        path: Relative path from the user script.

    Returns:
        str: Absolute file path.

    Raises:
        ValueError: If path is not a string.

    """
    if not isinstance(path, str):
        raise ValueError(f'Arg "path" must be str. But {path} is given.')

    if os.path.isabs(path):
        return path

    script_path = get_script_path()
    script_parent_dir = os.path.dirname(script_path)
    merged_path = os.path.join(script_parent_dir, path)
    return os.path.realpath(merged_path)


@guarded
def get_script_function_name() -> str:
    """Retrieve the name of the function in the user script that calls this function.

    Returns:
        str: Function name in the user script.

    Raises:
        RuntimeError: If the function name cannot be determined.

    """
    package_root = get_package_root_path()
    for frame in inspect.stack():
        file = frame.filename
        if not os.path.isfile(file):
            continue
        if is_path_under(package_root, file):
            continue
        return frame[3]

    msg = "Critical Error. Unable to get last called user function name"
    raise RuntimeError(msg)
