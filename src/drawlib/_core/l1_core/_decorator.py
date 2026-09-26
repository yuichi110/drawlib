# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib validation decorator module."""

import functools
from typing import Callable, ParamSpec, TypeVar

from pydantic import ConfigDict, validate_call

R = TypeVar("R")
P = ParamSpec("P")

VALIDATE_CONFIG = ConfigDict(arbitrary_types_allowed=True)


def guarded(caller: Callable[P, R]) -> Callable[P, R]:
    """Drawlib validation decorator function.

    Validates argument types and normalizes values using Pydantic.
    Exceptions (such as ValidationError) are propagated directly without suppression.

    Args:
        caller: Function to be decorated.

    Returns:
        Callable[P, R]: Decorated function with Pydantic validation.

    """
    validated_caller: Callable[P, R] | None = None

    @functools.wraps(caller)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        nonlocal validated_caller
        if validated_caller is None:
            validated_caller = validate_call(config=VALIDATE_CONFIG)(caller)
        return validated_caller(*args, **kwargs)

    return wrapper
