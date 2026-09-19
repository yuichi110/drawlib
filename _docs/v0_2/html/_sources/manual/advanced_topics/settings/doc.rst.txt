===================
Library Settings
===================

Drawlib includes the ``dutil_settings`` object, which provides functions to manage library settings. 
Currently, these settings are focused on logging and debug modes:

- ``get_logging_mode()``: Retrieves the current logging mode.
- ``set_logging_mode()``: Sets the logging mode.
- ``get_suppress_warning()``: Checks if warnings are suppressed.
- ``set_suppress_warning()``: Enables or disables warning suppression.
- ``is_debug_mode()``: Checks if debug mode is enabled.
- ``is_developer_debug_mode()``: Checks if developer debug mode is enabled.

These functions allow users to control the behavior of logging and debug messages within the library.

Logging
==========

Drawlib provides functionality to adjust its logging level, which is distinct from the traditional syslog levels:

- ``quiet``: Shows only warnings and errors, equivalent to logging.ERROR.
- ``normal``: Default level, provides standard information, equivalent to logging.INFO.
- ``verbose``: Generates more detailed logs, equivalent to logging.DEBUG.
- ``debug``: Same to ``verbose``.
- ``developer``: Extensive logging including debug information, with error handling disabled.

You can set the logging level using ``set_logging_mode(mode)`` and retrieve the current level with ``get_logging_mode()``.
When you use ``drawlib`` command, logging level can be also configured at CLI options.

Suppressing Warnings
========================

Drawlib and its underlying libraries may generate warnings in certain situations. 
For instance, attempting to render Japanese text using an alphabet-only font could trigger a warning.

To control the display of these warnings, you can utilize the following functions from ``dutil_settings``:

- ``set_suppress_warning(enable: bool)``: Enables or disables the suppression of warnings.
- ``get_suppress_warning()``: Retrieves the current suppression setting.

Adjusting these settings allows users to manage how warnings are handled within Drawlib and its associated operations.

