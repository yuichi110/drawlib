# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for _settings.py module."""

import logging

import pytest
from pydantic import ValidationError

from drawlib.v0_2.private.l1_core._logging import logger
from drawlib.v0_2.private.l1_core._settings import dutil_settings


@pytest.fixture(autouse=True)
def preserve_dutil_settings():
    """Fixture to preserve and restore the global dutil_settings state between tests."""
    original_mode = dutil_settings.get_logging_mode()
    original_suppress = dutil_settings.get_suppress_warning()
    yield
    dutil_settings.set_logging_mode(original_mode)
    dutil_settings.set_suppress_warning(original_suppress)


class TestDrawlibSettings:
    """Test cases for the global DrawlibSettings singleton."""

    def test_default_values(self):
        """Test default values of the settings object."""
        # By default in pytest, developer mode is automatically set
        assert dutil_settings.get_logging_mode() in {"normal", "developer"}
        assert isinstance(dutil_settings.get_suppress_warning(), bool)

    def test_set_logging_mode_normal(self):
        """Test setting logging mode to normal."""
        dutil_settings.set_logging_mode("normal")
        assert dutil_settings.get_logging_mode() == "normal"
        assert logger.getEffectiveLevel() == logging.INFO
        assert dutil_settings.is_debug_mode() is False
        assert dutil_settings.is_developer_debug_mode() is False

    def test_set_logging_mode_quiet(self):
        """Test setting logging mode to quiet."""
        dutil_settings.set_logging_mode("quiet")
        assert dutil_settings.get_logging_mode() == "quiet"
        assert logger.getEffectiveLevel() == logging.CRITICAL
        assert dutil_settings.is_debug_mode() is False
        assert dutil_settings.is_developer_debug_mode() is False

    def test_set_logging_mode_verbose(self):
        """Test setting logging mode to verbose."""
        dutil_settings.set_logging_mode("verbose")
        assert dutil_settings.get_logging_mode() == "verbose"
        assert logger.getEffectiveLevel() == logging.DEBUG
        assert dutil_settings.is_debug_mode() is True
        assert dutil_settings.is_developer_debug_mode() is False

    def test_set_logging_mode_debug_alias(self):
        """Test setting logging mode to debug (alias of verbose)."""
        dutil_settings.set_logging_mode("debug")
        # should map to verbose internally
        assert dutil_settings.get_logging_mode() == "verbose"
        assert logger.getEffectiveLevel() == logging.DEBUG
        assert dutil_settings.is_debug_mode() is True
        assert dutil_settings.is_developer_debug_mode() is False

    def test_set_logging_mode_developer(self):
        """Test setting logging mode to developer."""
        dutil_settings.set_logging_mode("developer")
        assert dutil_settings.get_logging_mode() == "developer"
        assert logger.getEffectiveLevel() == logging.DEBUG
        assert dutil_settings.is_debug_mode() is True
        assert dutil_settings.is_developer_debug_mode() is True

    def test_set_logging_mode_invalid(self):
        """Test that an invalid logging mode raises a ValidationError."""
        with pytest.raises(ValidationError):
            # Type ignore to test dynamic runtime validation
            dutil_settings.set_logging_mode("invalid_mode")  # type: ignore

    def test_suppress_warning(self):
        """Test suppressing warnings enables warning filters correctly."""
        dutil_settings.set_suppress_warning(True)
        assert dutil_settings.get_suppress_warning() is True

        dutil_settings.set_suppress_warning(False)
        assert dutil_settings.get_suppress_warning() is False
