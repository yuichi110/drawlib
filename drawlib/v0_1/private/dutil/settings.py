# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""dutil_settings implementation module."""

import logging
import sys
import typing
import warnings

from drawlib.v0_1.private.logging import logger

__ARG_QUIET = "--drawlib_quiet"
__ARG_DEBUG = "--drawlib_debug"
__ARG_DEVDEBUG = "--drawlib_devdebug"
__ARG_SUPPRESS_WARNING = "--drawlib_suppress_warning"


class DrawlibSettings:
    """Class for managing drawlib settings.

    This class should not be used directly. Use its singleton instance ``dsettings`` instead.
    """

    def __init__(self) -> None:
        """
        Initialize DrawlibSettings.

        This class holds logging modes which determine error handling methods.

        """
        self._logging_mode: typing.Literal[
            "normal",
            "quiet",
            "verbose",
            "developer",
        ] = "normal"
        self._suppress_warning: bool = False

    def get_logging_mode(
        self,
    ) -> typing.Literal[
        "normal",
        "quiet",
        "verbose",
        "developer",
    ]:
        """
        Get the current logging mode.

        Returns the current logging mode, which can be one of the following:
        * "quiet": Only show error log. Logging level CRITICAL.
        * "normal": Normal logging. Logging level INFO.
        * "verbose": Show detailed logging. Logging level DEBUG.
        * "developer": Verbose + disable error handling. Logging level DEBUG.

        Returns:
            str: Current logging mode.
        """
        return self._logging_mode

    def set_logging_mode(
        self,
        mode: typing.Literal["normal", "quiet", "verbose", "debug", "developer"],
    ) -> None:
        """
        Set the logging mode.

        * "quiet" sets logging level to CRITICAL.
        * "normal" sets logging level to INFO.
        * "verbose" sets logging level to DEBUG.
        * "debug" sets logging level to DEBUG.
        * "developer" sets logging level to DEBUG.

        Setting "verbose" and "debug" enables debug mode.
        Setting "developer" enables debug mode and devdebug mode.
        Stacktrace is shown when errors occur in debug mode.
        Error handling is disabled in devdebug mode.

        Args:
            mode: One of "normal", "quiet", "verbose", "debug", "developer".

        Returns:
            None

        Note:
            If an unsupported mode string is selected, the program will call ``sys.exit(1)``.
        """
        # change debug to verbose since it is just input option.
        if mode == "debug":
            mode = "verbose"

        if mode == "normal":
            logger.setLevel(logging.INFO)

        elif mode in {"verbose", "developer"}:
            logger.setLevel(logging.DEBUG)

        elif mode == "quiet":
            logger.setLevel(logging.CRITICAL)

        else:
            logger.critical(f'logging mode "{mode}" is not supported.')
            sys.exit(1)

        self._logging_mode = mode

    def get_suppress_warning(self) -> bool:
        """
        Get whether suppressing warnings is enabled.

        Matplot warnings are shown when it detects small troubles,
        such as drawing non-ASCII text without specifying a font.
        If suppress warnings is enabled, these warnings will be suppressed.

        Returns:
            bool: Whether suppressing warnings is enabled.
        """
        return self._suppress_warning

    def set_suppress_warning(self, enable: bool) -> None:
        """
        Enable or disable suppressing warnings.

        Matplot warnings are shown when it detects small troubles,
        such as drawing non-ASCII text without specifying a font.
        If suppress warnings is enabled, these warnings will be suppressed.

        Args:
            enable: True to suppress warnings, False otherwise.

        Returns:
            None
        """
        self._set_suppress_warning(enable, no_message=False)

    def _set_suppress_warning(self, enable: bool, no_message: bool = True) -> None:
        """
        Set the suppress warning flag internally.

        For use in pytest to avoid useless logging messages at debug level.

        Args:
            enable: True to suppress warnings, False otherwise.
            no_message: True to avoid logging messages, False otherwise.

        Returns:
            None
        """
        if enable:
            warnings.filterwarnings("ignore")
        else:
            warnings.filterwarnings("default")

        if not no_message:
            logger.debug(f'set_suppress_warning(): "{enable}"')

        self._suppress_warning = enable

    def is_debug_mode(self) -> bool:
        """
        Check if debug mode is enabled.

        In debug mode, stacktraces are shown when errors occur.
        Debug mode can be set using ``set_logging_mode()``.
        Setting "verbose" or "developer" enables debug mode.

        Returns:
            bool: Whether debug mode is enabled.
        """
        if self._logging_mode == "verbose":
            return True
        if self._logging_mode == "developer":
            return True

        return False

    def is_developer_debug_mode(self) -> bool:
        """
        Check if developer debug mode is enabled.

        In developer debug mode, error handling is disabled, which is useful for
        development and testing. Developer debug mode can be set using
        ``set_logging_mode()``. Setting "developer" enables developer debug mode.
        When running pytest, developer debug mode is automatically enabled.

        Returns:
            bool: Whether developer debug mode is enabled.
        """
        return self._logging_mode == "developer"


dutil_settings = DrawlibSettings()
"""Managing drawlib's library settings.

This object provides utilities for setting and retrieving logging modes,
enabling or disabling warnings, and determining debug states.
"""

# set logging mode normal first.
dutil_settings.set_logging_mode("normal")

# set logging mode quiet if selected
if __ARG_QUIET in sys.argv:
    dutil_settings.set_logging_mode("quiet")

# set logging mode debug if selected
if __ARG_DEBUG in sys.argv:
    if __ARG_QUIET in sys.argv:
        logger.critical(f"option {__ARG_QUIET} can not be used with option {__ARG_DEBUG}")
        sys.exit(1)
    dutil_settings.set_logging_mode("quiet")

# set logging mode developer if selected
if __ARG_DEVDEBUG in sys.argv:
    if __ARG_QUIET in sys.argv:
        logger.critical(f"option {__ARG_QUIET} can not be used with option {__ARG_DEVDEBUG}")
        sys.exit(1)
    dutil_settings.set_logging_mode("developer")

# set logging mode developer on pytest
for arg in sys.argv:
    # command pytest can be abspath
    if arg.endswith("pytest"):
        if __ARG_QUIET in sys.argv:
            logger.critical(f"option {__ARG_QUIET} can not be used " f"with option {__ARG_DEVDEBUG}")
            sys.exit(1)
        dutil_settings.set_logging_mode("developer")
        break

if __ARG_SUPPRESS_WARNING in sys.argv:
    dutil_settings.set_suppress_warning(True)
