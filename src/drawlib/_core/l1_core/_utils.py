# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Utility module."""

import inspect
import os
import os.path

from drawlib._core.l1_core._logging import logger
from drawlib._core.l1_core._settings import dutil_settings


def get_package_root_path() -> str:
    """Retrieve the root path of the package.

    Returns:
        str: Absolute path of the package root.

    """
    # Get the directory of the current file (_utils.py)
    current_file = inspect.stack()[0].filename
    package_root = os.path.dirname(os.path.abspath(current_file))

    # Go up as long as the parent directory also contains an __init__.py file.
    # This identifies the outermost package directory.
    while True:
        parent_dir = os.path.dirname(package_root)
        if parent_dir == package_root:  # Reached the file system root
            break
        if not os.path.exists(os.path.join(parent_dir, "__init__.py")):
            break
        package_root = parent_dir

    return package_root


def is_path_under(parent_path: str, child_path: str) -> bool:
    """Check if a child path is under a parent path.

    Args:
        parent_path: Parent directory path.
        child_path: Child directory or file path.

    Returns:
        bool: True if child path is under parent path, False otherwise.

    """
    try:
        common_parent = os.path.commonpath([parent_path, child_path])
    except Exception:
        # ValueError happens when compare windows N-Drive and M-Drive
        # But use Exception class for catch for handling unexpected situation.
        return False

    abs_parent_path = os.path.abspath(parent_path)
    abs_common_path = os.path.abspath(common_parent)
    return abs_parent_path == abs_common_path


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
