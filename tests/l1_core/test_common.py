# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for _common.py module."""

import os
from unittest.mock import patch

import pytest

from drawlib._core.l1_core._common import get_package_root_path, is_path_under


class TestGetPackageRootPath:
    """Test cases for get_package_root_path."""

    def test_get_package_root_path(self):
        """Test retrieving the package root path."""
        path = get_package_root_path()
        assert os.path.exists(path)
        assert os.path.isdir(path)
        assert path.endswith("drawlib") or "drawlib" in path


class TestIsPathUnder:
    """Test cases for is_path_under."""

    def test_child_inside_parent(self):
        """Test when the child path is nested under the parent path."""
        parent = "/usr/local"
        child = "/usr/local/bin/python"
        assert is_path_under(parent, child) is True

    def test_same_path(self):
        """Test when parent and child paths are identical."""
        parent = "/usr/local/bin"
        child = "/usr/local/bin"
        assert is_path_under(parent, child) is True

    def test_unrelated_path(self):
        """Test when parent and child paths are completely unrelated."""
        parent = "/usr/local"
        child = "/var/log"
        assert is_path_under(parent, child) is False

    def test_parent_deeper_than_child(self):
        """Test when the parent path is nested deeper than the child path."""
        parent = "/usr/local/bin"
        child = "/usr"
        assert is_path_under(parent, child) is False

    def test_exception_handling(self):
        """Test that any exception (e.g. comparing windows drives) returns False."""
        # Force os.path.commonpath to raise an exception (ValueError or generic Exception)
        with patch("os.path.commonpath", side_effect=ValueError("Invalid comparison")):
            assert is_path_under("/usr/local", "/var/log") is False
