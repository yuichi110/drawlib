# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the cache module in l3_external."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from drawlib._core.l3_external._cache import download_all_fonts, purge_font_cache


class TestDownloadAllFonts:
    """Test cases for download_all_fonts function."""

    def test_download_all_fonts(self):
        """Test that download_all_fonts calls download_and_extract on font packages."""
        with patch("drawlib._release_assets.ReleaseAssetPackage.download_and_extract") as mock_dl:
            download_all_fonts()
            assert mock_dl.call_count == 46


class TestPurgeFontCache:
    """Test cases for purge_font_cache function."""

    def test_purge_font_cache(self, tmp_path: Path):
        """Test purge_font_cache deletes files and directories inside caches except __init__.py."""
        font_dir = tmp_path / "font"
        font_icon_dir = tmp_path / "font_icon"
        icon_dir = tmp_path / "icon"
        map_dir = tmp_path / "map"
        rules_dir = tmp_path / "rules"
        for d in (font_dir, font_icon_dir, icon_dir, map_dir, rules_dir):
            d.mkdir()

        # Create files under font_dir
        (font_dir / "__init__.py").write_text("init")
        (font_dir / "some_font.ttf").write_text("font_data")
        (font_dir / "some_dir").mkdir()
        (font_dir / "some_dir" / "file.txt").write_text("hello")

        # Create files under font_icon_dir, icon_dir, map_dir, rules_dir
        (font_icon_dir / "__init__.py").write_text("init")
        (font_icon_dir / "icon.ttf").write_text("icon_data")
        (icon_dir / "gcp").mkdir()
        (icon_dir / "gcp" / "compute.png").write_text("png")
        (map_dir / "world").mkdir()
        (map_dir / "world" / "world.geojson").write_text("{}")
        (rules_dir / "overview.md").write_text("# Overview")

        # Patch all cache directory paths in _cache.py to point to temporary directories
        with (
            patch("drawlib._core.l3_external._cache.FONT_DIR_PATH", str(font_dir)),
            patch("drawlib._core.l3_external._cache.FONT_ICON_DIR_PATH", str(font_icon_dir)),
            patch("drawlib._core.l3_external._cache.ICON_DIR_PATH", str(icon_dir)),
            patch("drawlib._core.l3_external._cache.MAP_DIR_PATH", str(map_dir)),
            patch("drawlib._core.l3_external._cache.RULES_DIR_PATH", str(rules_dir)),
        ):
            purge_font_cache()

        # Assertions
        assert (font_dir / "__init__.py").exists()
        assert not (font_dir / "some_font.ttf").exists()
        assert not (font_dir / "some_dir").exists()

        assert (font_icon_dir / "__init__.py").exists()
        assert not (font_icon_dir / "icon.ttf").exists()

        assert not (icon_dir / "gcp").exists()
        assert not (map_dir / "world").exists()
        assert not (rules_dir / "overview.md").exists()
