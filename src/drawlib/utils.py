# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public user utilities module for drawlib.

Provides a dynamic namespace for user-defined helper functions, reusable diagram
components, and project-specific constants defined in utils.py.
"""

from __future__ import annotations

import sys as _sys
from typing import Any as _Any

_ORIGINAL_KEYS: set[str] = {
    "__name__",
    "__doc__",
    "__package__",
    "__loader__",
    "__spec__",
    "__file__",
    "__cached__",
    "__builtins__",
    "__annotations__",
    "__getattr__",
    "__all__",
    "_sys",
    "_Any",
    "_ORIGINAL_KEYS",
    "_reset_utils",
}


def _reset_utils() -> None:
    """Reset drawlib.utils to default attributes."""
    mod = _sys.modules.get(__name__)
    if mod is None:
        return

    for key in list(vars(mod).keys()):
        if key not in _ORIGINAL_KEYS:
            delattr(mod, key)


def __getattr__(name: str) -> _Any:  # noqa: ANN401
    """Raise AttributeError with a clear explanation if a user utility attribute is missing.

    Args:
        name (str): The name of the missing attribute.

    Raises:
        AttributeError: Always raised to indicate the attribute is not defined.
    """
    raise AttributeError(
        f"module 'drawlib.utils' has no attribute '{name}'. "
        f"Ensure it is defined in your 'utils.py' file and passed via the '--utils' option "
        f"or placed in your docs directory."
    )


__all__: list[str] = []
