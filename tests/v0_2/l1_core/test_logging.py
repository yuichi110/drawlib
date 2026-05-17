# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for _logging.py module."""

import logging

import drawlib
from drawlib.v0_2.private.l1_core._logging import logger


class TestLogging:
    """Test cases for the global logger configured in _logging.py."""

    def test_logger_name(self):
        """Test that the global logger is named after drawlib's library name."""
        assert logger.name == drawlib.LIB_NAME

    def test_logger_has_handlers(self):
        """Test that the global logger has at least one handler configured."""
        assert len(logger.handlers) >= 1
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) >= 1
