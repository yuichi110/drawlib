"""write docstring later"""

# pylint: disable=global-statement
# pylint: disable=logging-fstring-interpolation

import typing
import warnings
import sys
import logging
from drawlib._logging import logger

__ARG_QUIET = "--drawlib_quiet"
__ARG_DEBUG = "--drawlib_debug"
__ARG_DEVDEBUG = "--drawlib_devdebug"
__ARG_SUPPRESS_WARNING = "--drawlib_suppress_warning"

_logging_mode: typing.Literal[
    "normal",
    "quiet",
    "verbose",
    "developer",
] = "normal"
_suppress_warning: bool = False


def get_logging_mode() -> (
    typing.Literal["normal", "quiet", "verbose", "developer"]
):
    """write docstring later"""
    return _logging_mode


def set_logging_mode(
    mode: typing.Literal["normal", "quiet", "verbose", "developer"]
):
    """write docstring later"""

    global _logging_mode
    _logging_mode = mode
    if mode == "normal":
        logger.setLevel(logging.INFO)
    elif mode in ["verbose", "developer"]:
        logger.setLevel(logging.DEBUG)
    elif mode == "quiet":
        logger.setLevel(logging.CRITICAL)
    else:
        logger.critical(f'logging mode "{mode}" is not supported.')
        sys.exit(1)
    logger.debug(f'set_log_mode(): "{mode}"')


def get_suppress_warning():
    """write docstring later"""

    return _suppress_warning


def set_suppress_warning(enable: bool):
    """write docstring later"""

    global _suppress_warning
    if enable:
        warnings.filterwarnings("ignore")
    else:
        warnings.filterwarnings("default")
    _suppress_warning = enable
    logger.debug(f'set_suppress_warning(): "{enable}"')


def is_debug_mode():
    """write docstring later"""

    if _logging_mode == "debug":
        return True
    if _logging_mode == "developer":
        return True
    return False


def is_developer_debug_mode():
    """write docstring later"""

    return _logging_mode == "developer"


# set logging mode normal first.
set_logging_mode("normal")

# set logging mode quiet if selected
if __ARG_QUIET in sys.argv:
    set_logging_mode("quiet")

# set logging mode debug if selected
if __ARG_DEBUG in sys.argv:
    if __ARG_QUIET in sys.argv:
        logger.critical(
            f"option {__ARG_QUIET} can not be used with option {__ARG_DEBUG}"
        )
        sys.exit(1)
    set_logging_mode("quiet")

# set logging mode developer if selected
if "pytest" in sys.argv or __ARG_DEVDEBUG in sys.argv:
    if __ARG_QUIET in sys.argv:
        logger.critical(
            f"option {__ARG_QUIET} can not be used with option {__ARG_DEVDEBUG}"
        )
        sys.exit(1)
    set_logging_mode("developer")

if __ARG_SUPPRESS_WARNING in sys.argv:
    set_suppress_warning(True)
