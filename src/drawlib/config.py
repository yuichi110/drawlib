# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib default configuration.

This module provides default project configuration (such as default styles)
and serves as the target for user-provided configuration overlays during builds.
"""

from __future__ import annotations

import sys as _sys
from typing import Any as _Any

from drawlib.preset_styles import (
    BasePresetStyles,
    EssentialsStyles,
    essentials_styles,
)

# Default style preset for drawlib documentation and illustrations
styles: EssentialsStyles = essentials_styles

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
    "styles",
    "BasePresetStyles",
    "EssentialsStyles",
    "essentials_styles",
    "_sys",
    "_Any",
    "_ORIGINAL_KEYS",
    "_reset_config",
}


def _reset_config() -> None:
    """Reset drawlib.config to default attributes."""
    mod = _sys.modules.get(__name__)
    if mod is None:
        return

    # Delete any custom attributes added during previous configuration runs
    for key in list(vars(mod).keys()):
        if key not in _ORIGINAL_KEYS:
            delattr(mod, key)

    # Restore default styles
    setattr(mod, "styles", essentials_styles)


def __getattr__(name: str) -> _Any:  # noqa: ANN401
    """Raise AttributeError with a clear explanation if a config attribute is missing.

    Args:
        name (str): The name of the missing attribute.

    Raises:
        AttributeError: Always raised to indicate the attribute is not defined.
    """
    raise AttributeError(
        f"module 'drawlib.config' has no attribute '{name}'. "
        f"If this is a custom configuration variable, ensure it is defined in your config file "
        f"and passed via the '--config' option."
    )


__all__ = [
    "styles",
]
