# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common util module."""

import inspect
import os


def get_package_root_path() -> str:
    """Retrieve the root path of the package.

    Returns:
        str: Absolute path of the package root.

    """
    first_module = inspect.stack()[0].filename
    module_path = os.path.abspath(first_module)
    package_root = module_path
    while not os.path.exists(os.path.join(package_root, "__init__.py")):
        package_root = os.path.dirname(package_root)
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
