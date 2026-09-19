# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for Font models in _font.py."""

from enum import Enum
from unittest.mock import patch

import pytest

from drawlib._core.l2_models_._font import (
    FontBase,
    FontFile,
    FontMetadata,
    FontResource,
)


class TestFontMetadata:
    """Test cases for FontMetadata."""

    def test_fields(self):
        """Test that FontMetadata fields are correctly stored and retrieved."""
        meta = FontMetadata(
            path="foo/bar.ttf",
            abs_path="/abs/foo/bar.ttf",
            url="http://example.com/font.ttf",
            md5="abc",
        )
        assert meta.path == "foo/bar.ttf"
        assert meta.abs_path == "/abs/foo/bar.ttf"
        assert meta.url == "http://example.com/font.ttf"
        assert meta.md5 == "abc"


class TestFontResource:
    """Test cases for FontResource."""

    def test_fields(self):
        """Test that FontResource fields are correctly stored and retrieved."""
        res = FontResource(path="foo/bar.ttf", md5="xyz")
        assert res.path == "foo/bar.ttf"
        assert res.md5 == "xyz"


class TestFontBase:
    """Test cases for FontBase."""

    def test_inheritance(self):
        """Test that FontBase inherits from str and Enum."""
        assert issubclass(FontBase, Enum)
        assert issubclass(FontBase, str)


class TestFontFile:
    """Test cases for FontFile."""

    def test_validation_success(self):
        """Test that validating an existing file works."""
        with (
            patch("drawlib._core.l2_models_._font.get_script_relative_path", return_value="/dummy/font.ttf"),
            patch("os.path.exists", return_value=True),
        ):
            font = FontFile("dummy/font.ttf")
            assert font.file == "/dummy/font.ttf"

    def test_validation_failure(self):
        """Test that validating a non-existing file raises FileNotFoundError."""
        with (
            patch("drawlib._core.l2_models_._font.get_script_relative_path", return_value="/dummy/font.ttf"),
            patch("os.path.exists", return_value=False),
        ):
            with pytest.raises(FileNotFoundError, match='font file "/dummy/font.ttf" does not exist.'):
                FontFile("dummy/font.ttf")
