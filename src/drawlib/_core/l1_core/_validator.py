# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Lazy call-validation decorator wrapping Pydantic's validate_call."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar, overload

if TYPE_CHECKING:
    from pydantic import ConfigDict

P = ParamSpec("P")
R = TypeVar("R")


@overload
def validate_call(func: Callable[P, R], /) -> Callable[P, R]: ...


@overload
def validate_call(
    func: None = None,
    /,
    *,
    config: ConfigDict | None = None,
    validate_return: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def validate_call(
    func: Callable[P, R] | None = None,
    /,
    *,
    config: ConfigDict | None = None,
    validate_return: bool = False,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """Defer Pydantic's validate_call schema compilation until first invocation.

    Preserves the exact function signature via ParamSpec/TypeVar for static type
    checkers and IDE autocompletion while avoiding eager schema compilation at
    module import time.

    Args:
        func: Target callable when used as ``@validate_call`` without arguments.
        config: Optional Pydantic ``ConfigDict`` passed to ``pydantic.validate_call``.
        validate_return: Whether to also validate the return value.

    Returns:
        Wrapped callable or decorator preserving ``func``'s signature.
    """

    def decorator(target: Callable[P, R]) -> Callable[P, R]:
        validated: Callable[P, R] | None = None

        @wraps(target)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal validated
            if validated is None:
                from pydantic import validate_call as _pydantic_validate_call  # noqa: PLC0415

                validated = _pydantic_validate_call(
                    config=config,
                    validate_return=validate_return,
                )(target)
            return validated(*args, **kwargs)

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


__all__ = ["validate_call"]
