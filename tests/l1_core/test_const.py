# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for _const.py module."""

import os

from drawlib._core.l1_core._const import (
    ASSETS_DIR_PATH,
    FONT_DIR_PATH,
    FONT_ICON_DIR_PATH,
    ICON_DIR_PATH,
)


class TestConst:
    """Test cases for constants in _const.py."""

    def test_assets_dir_path(self):
        """Test ASSETS_DIR_PATH is a valid existing directory path."""
        assert os.path.exists(ASSETS_DIR_PATH)
        assert os.path.isdir(ASSETS_DIR_PATH)

    def test_font_dir_path(self):
        """Test FONT_DIR_PATH points to the fonts directory under ASSETS_DIR_PATH."""
        assert FONT_DIR_PATH == os.path.join(ASSETS_DIR_PATH, "fonts")

    def test_font_icon_dir_path(self):
        """Test FONT_ICON_DIR_PATH points to the fonticons directory under ASSETS_DIR_PATH."""
        assert FONT_ICON_DIR_PATH == os.path.join(ASSETS_DIR_PATH, "fonticons")

    def test_icon_dir_path(self):
        """Test ICON_DIR_PATH points to the icons directory under ASSETS_DIR_PATH."""
        assert ICON_DIR_PATH == os.path.join(ASSETS_DIR_PATH, "icons")

