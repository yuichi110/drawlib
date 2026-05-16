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
import os
import sys
import traceback
from typing import Callable, ParamSpec, TypeVar

from pydantic import ConfigDict, validate_call

from drawlib.v0_2.private.l1_core._common import get_package_root_path, is_path_under
from drawlib.v0_2.private.l1_core._logging import logger
from drawlib.v0_2.private.l1_core._settings import dutil_settings

R = TypeVar("R")
P = ParamSpec("P")


def guarded(caller: Callable[P, R]) -> Callable[P, R]:
    """Drawlib error handling decorator function.

    Decorates functions to handle errors gracefully. Depending on the logging mode:
    - quiet/normal: Shows minimal error information and exits with code 1.
    - verbose: Adds stack trace to the error information.
    - developer: Disables error handling for debugging purposes.

    Args:
        caller: Function to be decorated.

    Returns:
        Decorated function.

    Raises:
        SystemExit: Exits with code 1 on error.

    Note:
        Avoid applying this decorator to functions that raise and handle their own errors,
        or to the 'settings' module due to potential circular imports.

    """
    validated_caller = None
    pydantic_config = ConfigDict(arbitrary_types_allowed=True)

    @functools.wraps(caller)  # inherit name and docstring from caller
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # cache validate_call first time
        nonlocal validated_caller
        if validated_caller is None:
            validated_caller = validate_call(config=pydantic_config)(caller)

        # without error handling
        if dutil_settings.is_developer_debug_mode():
            return validated_caller(*args, **kwargs)

        # with error handling
        try:
            return validated_caller(*args, **kwargs)
        except Exception as e:
            package_root = get_package_root_path()
            for frame in inspect.stack():
                file = frame.filename
                if not os.path.isfile(file):
                    continue
                if is_path_under(package_root, file):
                    continue
                line = frame.lineno
                logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
                logger.critical(str(e))
                logger.debug("")
                logger.debug(traceback.format_exc())
                break
            sys.exit(1)

    return wrapper
