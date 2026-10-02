# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for drawlib.styles module and styles loader."""

from __future__ import annotations

import os
import tempfile

import pytest

import drawlib.styles
from drawlib._builder.doc_builder.styles_utils import load_styles
from drawlib.preset_colors import (
    DefaultColors,
    GoogleColors,
    MonochromeColors,
)
from drawlib.preset_styles import (
    DefaultStyles,
    GoogleStyles,
    MonochromeStyles,
)


def test_default_styles() -> None:
    """Verify default drawlib.styles provides default styles and colors."""
    load_styles(None)
    assert drawlib.styles.Styles is DefaultStyles or isinstance(drawlib.styles.Styles, DefaultStyles)
    assert drawlib.styles.Colors is DefaultColors or isinstance(drawlib.styles.Colors, DefaultColors)


def test_load_styles_custom_styles() -> None:
    """Verify load_styles loads custom styles and auto-resolves colors."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as f:
        f.write("from drawlib.preset_styles import MonochromeStyles\nStyles = MonochromeStyles\n")
        f.flush()
        styles_file = f.name

    try:
        load_styles(styles_file)
        assert drawlib.styles.Styles is MonochromeStyles or isinstance(drawlib.styles.Styles, MonochromeStyles)
        assert drawlib.styles.Colors is MonochromeColors or isinstance(drawlib.styles.Colors, MonochromeColors)
    finally:
        if os.path.exists(styles_file):
            os.remove(styles_file)
        load_styles(None)

    assert drawlib.styles.Styles is DefaultStyles or isinstance(drawlib.styles.Styles, DefaultStyles)
    assert drawlib.styles.Colors is DefaultColors or isinstance(drawlib.styles.Colors, DefaultColors)


def test_load_styles_custom_colors_explicit() -> None:
    """Verify load_styles respects explicitly defined colors in styles.py."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as f:
        f.write("from drawlib.preset_colors import GoogleColors\nColors = GoogleColors\n")
        f.flush()
        styles_file = f.name

    try:
        load_styles(styles_file)
        assert drawlib.styles.Colors is GoogleColors or isinstance(drawlib.styles.Colors, GoogleColors)
    finally:
        if os.path.exists(styles_file):
            os.remove(styles_file)
        load_styles(None)

    assert drawlib.styles.Colors is DefaultColors or isinstance(drawlib.styles.Colors, DefaultColors)


def test_load_styles_file_not_found() -> None:
    """Verify load_styles raises FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_styles("/path/to/definitely/nonexistent_styles.py")
