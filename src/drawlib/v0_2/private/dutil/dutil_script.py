# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Script path related utilities."""

from drawlib.v0_2.private.util import (
    get_script_function_name as get_function_name,
)
from drawlib.v0_2.private.util import (
    get_script_path as get_script_path,
)
from drawlib.v0_2.private.util import (
    get_script_relative_path as get_relative_path,
)

__all__ = [
    "get_function_name",
    "get_script_path",
    "get_relative_path",
]
