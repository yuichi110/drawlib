# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for utility functions in _utils.py."""

import pytest

from drawlib.v0_2.private.l2_types_._utils import validate_literal


class TestValidateLiteral:
    """Test cases for validate_literal helper function."""

    def test_validate_literal_valid(self):
        """Test validate_literal with a valid supported value."""
        supported = {"red", "green", "blue"}
        assert validate_literal("red", supported, "color") == "red"

    def test_validate_literal_invalid(self):
        """Test validate_literal with an invalid unsupported value."""
        supported = {"red", "green", "blue"}
        with pytest.raises(ValueError) as exc_info:
            validate_literal("yellow", supported, "color")

        assert "Arg/Attr \"color\" must be one of ['blue', 'green', 'red']. But \"yellow\" is given." in str(
            exc_info.value
        )
