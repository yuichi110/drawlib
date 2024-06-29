# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Global logger implementation."""

import logging

import drawlib

logger = logging.getLogger(drawlib.LIB_NAME)
"""Global logger object which is shared on this library."""

# set default level
logger.setLevel(logging.INFO)

# set default log format
_formatter = logging.Formatter("%(message)s")
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
