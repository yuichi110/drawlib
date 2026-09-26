# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for FilePath type in _path.py."""

import os
from pathlib import Path
from typing import Union

import pytest
from pydantic import TypeAdapter, ValidationError, validate_call

from drawlib._core.l2_types import FilePath, TypeFilePath


class TestFilePath:
    """Test cases for FilePath validation and resolution."""

    def test_absolute_path(self):
        """Test that an absolute path is returned as a normalized real path."""
        adapter: TypeAdapter[FilePath] = TypeAdapter(FilePath)
        abs_path = os.path.abspath(__file__)
        assert adapter.validate_python(abs_path) == os.path.realpath(abs_path)

    def test_relative_path(self):
        """Test that a relative path resolves relative to caller script directory."""
        adapter: TypeAdapter[FilePath] = TypeAdapter(FilePath)
        resolved = adapter.validate_python("my_asset.png")
        expected = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_asset.png"))
        assert resolved == expected

    def test_pathlib_path(self):
        """Test that a pathlib.Path object is converted to absolute string path."""
        adapter: TypeAdapter[FilePath] = TypeAdapter(FilePath)
        resolved = adapter.validate_python(Path("my_asset.png"))
        expected = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_asset.png"))
        assert resolved == expected

    def test_empty_string_fails(self):
        """Test that an empty string raises ValidationError."""
        adapter: TypeAdapter[FilePath] = TypeAdapter(FilePath)
        with pytest.raises(ValidationError):
            adapter.validate_python("")

        with pytest.raises(ValidationError):
            adapter.validate_python("   ")

    def test_invalid_type_fails(self):
        """Test that non-string non-PathLike types raise ValidationError."""
        adapter: TypeAdapter[FilePath] = TypeAdapter(FilePath)
        with pytest.raises(ValidationError):
            adapter.validate_python(123)

        with pytest.raises(ValidationError):
            adapter.validate_python(["file.png"])

    def test_validate_call_function(self):
        """Test FilePath within a function decorated with @validate_call."""

        @validate_call
        def load_asset(file: FilePath) -> str:
            return file

        result = load_asset("test_image.png")
        expected = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_image.png"))
        assert result == expected

    def test_union_with_other_types(self):
        """Test FilePath in a Union with another type."""

        @validate_call
        def flexible_loader(data: Union[FilePath, int]) -> tuple[type, object]:
            return type(data), data

        type_res, val_res = flexible_loader("image.png")
        assert type_res is str
        assert str(val_res).endswith("image.png")

        type_int, val_int = flexible_loader(42)
        assert type_int is int
        assert val_int == 42

    def test_backward_compat_alias(self):
        """Test that TypeFilePath is an alias of FilePath."""
        assert TypeFilePath == FilePath
