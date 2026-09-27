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
from drawlib._preset_colors import (
    DefaultStyleColors,
    EssentialsStyleColors,
    GoogleStyleColors,
    MonochromeStyleColors,
)
from drawlib._preset_styles import (
    EssentialsStyles,
    default_styles,
    essentials_styles,
    google_styles,
    monochrome_styles,
)


def test_default_styles() -> None:
    """Verify default drawlib.styles provides default styles and colors."""
    load_styles(None)
    assert isinstance(drawlib.styles.styles, EssentialsStyles)
    assert drawlib.styles.colors is EssentialsStyleColors


def test_resolve_colors() -> None:
    """Verify _resolve_colors correctly maps style catalog classes to color classes."""
    assert drawlib.styles._resolve_colors(essentials_styles) is EssentialsStyleColors
    assert drawlib.styles._resolve_colors(default_styles) is DefaultStyleColors
    assert drawlib.styles._resolve_colors(monochrome_styles) is MonochromeStyleColors
    assert drawlib.styles._resolve_colors(google_styles) is GoogleStyleColors


def test_set_active_styles_and_reset() -> None:
    """Verify _set_active_styles updates styles and colors, and _reset_styles restores defaults."""
    drawlib.styles._set_active_styles(monochrome_styles)
    assert drawlib.styles.styles is monochrome_styles
    assert drawlib.styles.colors is MonochromeStyleColors

    drawlib.styles._reset_styles()
    assert isinstance(drawlib.styles.styles, EssentialsStyles)
    assert drawlib.styles.colors is EssentialsStyleColors


def test_load_styles_custom_styles() -> None:
    """Verify load_styles loads custom styles and auto-resolves colors."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as f:
        f.write("from drawlib.preset_styles import monochrome_styles\nstyles = monochrome_styles\n")
        f.flush()
        styles_file = f.name

    try:
        load_styles(styles_file)
        assert drawlib.styles.styles is monochrome_styles
        assert drawlib.styles.colors is MonochromeStyleColors
    finally:
        if os.path.exists(styles_file):
            os.remove(styles_file)
        load_styles(None)

    assert isinstance(drawlib.styles.styles, EssentialsStyles)
    assert drawlib.styles.colors is EssentialsStyleColors


def test_load_styles_custom_colors_explicit() -> None:
    """Verify load_styles respects explicitly defined colors in styles.py."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".py", delete=False) as f:
        f.write(
            "from drawlib.colors import DefaultStyleColors\n"
            "colors = DefaultStyleColors\n"
        )
        f.flush()
        styles_file = f.name

    try:
        load_styles(styles_file)
        assert drawlib.styles.colors is DefaultStyleColors
    finally:
        if os.path.exists(styles_file):
            os.remove(styles_file)
        load_styles(None)

    assert drawlib.styles.colors is EssentialsStyleColors


def test_load_styles_file_not_found() -> None:
    """Verify load_styles raises FileNotFoundError for non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_styles("/path/to/definitely/nonexistent_styles.py")
