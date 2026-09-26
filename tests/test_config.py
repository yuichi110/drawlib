# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for drawlib.config module and config overlay loader."""

import os
import tempfile

import pytest

import drawlib.config
from drawlib._preset_styles import EssentialsStyles
from drawlib._tools.doc_builder.config import load_config


def test_default_config() -> None:
    """Verify default drawlib.config provides default styles."""
    load_config(None)
    assert isinstance(drawlib.config.styles, EssentialsStyles)


def test_missing_attribute_error() -> None:
    """Verify accessing an undefined attribute on drawlib.config raises AttributeError."""
    load_config(None)
    with pytest.raises(AttributeError, match="module 'drawlib.config' has no attribute 'nonexistent_var'"):
        _ = getattr(drawlib.config, "nonexistent_var")


def test_custom_config_overlay() -> None:
    """Verify custom config overlays attributes onto drawlib.config."""
    # Simulate default attrs on drawlib.config
    drawlib.config._ORIGINAL_KEYS.update({"a", "b", "c"})
    setattr(drawlib.config, "a", 1)
    setattr(drawlib.config, "b", 1)
    setattr(drawlib.config, "c", 1)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as f:
        f.write("b = 2\nd = 2\n")
        f.flush()
        cfg_file = f.name

    try:
        load_config(cfg_file)

        assert getattr(drawlib.config, "a") == 1
        assert getattr(drawlib.config, "b") == 2
        assert getattr(drawlib.config, "c") == 1
        assert getattr(drawlib.config, "d") == 2

        # Verify from drawlib.config import ... works
        from drawlib.config import a, b, c, d  # noqa: PLC0415
        assert a == 1
        assert b == 2
        assert c == 1
        assert d == 2
    finally:
        drawlib.config._ORIGINAL_KEYS.difference_update({"a", "b", "c"})
        if os.path.exists(cfg_file):
            os.remove(cfg_file)
        load_config(None)


def test_custom_config_styles_patch() -> None:
    """Verify custom config can patch or override styles."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as f:
        f.write(
            "from drawlib.preset_styles import monochrome_styles\n"
            "styles = monochrome_styles\n"
            "PROJECT_NAME = 'TestProject'\n"
        )
        f.flush()
        cfg_file = f.name

    try:
        load_config(cfg_file)

        assert drawlib.config.styles.__class__.__name__ == "MonochromeStyles"
        assert getattr(drawlib.config, "PROJECT_NAME") == "TestProject"
    finally:
        if os.path.exists(cfg_file):
            os.remove(cfg_file)
        load_config(None)

    # After reset, styles should be back to EssentialsStyles
    assert isinstance(drawlib.config.styles, EssentialsStyles)
    with pytest.raises(AttributeError):
        _ = getattr(drawlib.config, "PROJECT_NAME")


def test_load_config_file_not_found() -> None:
    """Verify load_config raises FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_config("/path/to/definitely/nonexistent_config.py")
