# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the font module in l3_external."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from drawlib._core.l3_external._font import download_all_fonts, purge_font_cache


class TestDownloadAllFonts:
    """Test cases for download_all_fonts function."""

    def test_download_all_fonts_raises_not_implemented(self):
        """Test that download_all_fonts raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Not implemented yet"):
            download_all_fonts()


class TestPurgeFontCache:
    """Test cases for purge_font_cache function."""

    def test_purge_font_cache(self, tmp_path: Path):
        """Test purge_font_cache deletes files and directories inside caches except __init__.py."""
        font_dir = tmp_path / "font"
        font_icon_dir = tmp_path / "font_icon"
        font_dir.mkdir()
        font_icon_dir.mkdir()

        # Create files under font_dir
        (font_dir / "__init__.py").write_text("init")
        (font_dir / "some_font.ttf").write_text("font_data")
        (font_dir / "some_dir").mkdir()
        (font_dir / "some_dir" / "file.txt").write_text("hello")

        # Create files under font_icon_dir
        (font_icon_dir / "__init__.py").write_text("init")
        (font_icon_dir / "icon.ttf").write_text("icon_data")

        # Patch paths in _font.py to point to our temporary directories
        with (
            patch("drawlib._core.l3_external._font.FONT_DIR_PATH", str(font_dir)),
            patch("drawlib._core.l3_external._font.FONT_ICON_DIR_PATH", str(font_icon_dir)),
        ):
            purge_font_cache()

        # Assertions
        assert (font_dir / "__init__.py").exists()
        assert not (font_dir / "some_font.ttf").exists()
        assert not (font_dir / "some_dir").exists()

        assert (font_icon_dir / "__init__.py").exists()
        assert not (font_icon_dir / "icon.ttf").exists()
