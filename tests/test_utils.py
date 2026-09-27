# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for drawlib.utils module and utils loader."""

from __future__ import annotations

import os
import tempfile

import pytest

import drawlib.utils
from drawlib._builder.doc_builder.styles_utils import load_utils


def test_missing_attribute_error() -> None:
    """Verify accessing an undefined attribute on drawlib.utils raises AttributeError with actionable message."""
    load_utils(None)
    with pytest.raises(
        AttributeError,
        match=r"module 'drawlib\.utils' has no attribute 'nonexistent_func'\. Ensure it is defined in your 'utils\.py'",
    ):
        _ = getattr(drawlib.utils, "nonexistent_func")


def test_load_utils_custom_functions_and_constants() -> None:
    """Verify load_utils loads user functions and constants onto drawlib.utils."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as f:
        f.write(
            "COMPANY_NAME = 'Acme Corp'\n"
            "\n"
            "def double(x: int) -> int:\n"
            "    return x * 2\n"
        )
        f.flush()
        utils_file = f.name

    try:
        load_utils(utils_file)

        assert getattr(drawlib.utils, "COMPANY_NAME") == "Acme Corp"
        assert callable(getattr(drawlib.utils, "double"))
        assert getattr(drawlib.utils, "double")(21) == 42

        # Verify from drawlib.utils import ... works dynamically
        from drawlib.utils import COMPANY_NAME, double  # noqa: PLC0415

        assert COMPANY_NAME == "Acme Corp"
        assert double(5) == 10
    finally:
        if os.path.exists(utils_file):
            os.remove(utils_file)
        load_utils(None)

    # After reset, custom attributes should raise AttributeError
    with pytest.raises(AttributeError):
        _ = getattr(drawlib.utils, "COMPANY_NAME")
    with pytest.raises(AttributeError):
        _ = getattr(drawlib.utils, "double")


def test_load_utils_file_not_found() -> None:
    """Verify load_utils raises FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_utils("/path/to/definitely/nonexistent_utils.py")
