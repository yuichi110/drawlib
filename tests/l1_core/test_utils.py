# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for _utils.py module."""

import os
import typing
from unittest.mock import patch

import pytest

from drawlib._core.l1_core._utils import (
    get_script_function_name,
    get_script_path,
    get_script_relative_path,
)


class TestGetScriptPath:
    """Test cases for get_script_path."""

    def test_get_script_path_success(self):
        """Test that get_script_path successfully identifies this test file as the caller script."""
        path = get_script_path()
        assert os.path.exists(path)
        assert os.path.isabs(path)
        assert path.endswith("test_utils.py")

    def test_get_script_path_failure(self):
        """Test that get_script_path raises FileNotFoundError when no calling frame is found outside drawlib."""
        with (
            patch(
                "drawlib._core.l1_core._utils.get_package_root_path",
                return_value="/Users/yuichi/GitHub/drawlib/src/drawlib",
            ),
            patch("inspect.stack", return_value=[]),
        ):
            with pytest.raises(FileNotFoundError, match="Unable to detect call script file"):
                get_script_path()


class TestGetScriptRelativePath:
    """Test cases for get_script_relative_path."""

    def test_absolute_path_returns_same(self):
        """Test that passing an absolute path returns it unchanged."""
        abs_path = os.path.abspath(__file__)
        assert get_script_relative_path(abs_path) == abs_path

    def test_relative_path_resolution(self):
        """Test that passing a relative path resolves relative to this test script's directory."""
        resolved = get_script_relative_path("some_file.png")
        expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), "some_file.png")
        assert resolved == os.path.realpath(expected)

    def test_invalid_type_raises_value_error(self):
        """Test that passing a non-string raises a ValueError."""
        with pytest.raises(ValueError, match='Arg "path" must be str'):
            # Type ignore to test dynamic runtime validation
            get_script_relative_path(typing.cast(str, 42))


class TestGetScriptFunctionName:
    """Test cases for get_script_function_name."""

    def test_get_script_function_name_success(self):
        """Test that get_script_function_name successfully detects this test method's name."""
        name = get_script_function_name()
        assert name == "test_get_script_function_name_success"

    def test_get_script_function_name_failure(self):
        """Test that get_script_function_name raises RuntimeError when no caller frame is found."""
        with (
            patch(
                "drawlib._core.l1_core._utils.get_package_root_path",
                return_value="/Users/yuichi/GitHub/drawlib/src/drawlib",
            ),
            patch("inspect.stack", return_value=[]),
        ):
            with pytest.raises(RuntimeError, match="Unable to get last called user function name"):
                get_script_function_name()
