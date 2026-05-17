# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the fonts metadata module in l3_fonts."""

import pytest

from drawlib.v0_2.private.l2_models import FontBase
from drawlib.v0_2.private.l3_fonts._fonts import get_font_metadata
from drawlib.v0_2.private.l3_fonts._names import Font


class TestGetFontMetadata:
    """Test cases for get_font_metadata function."""

    def test_get_font_metadata_success(self):
        """Test get_font_metadata resolves correctly for standard fonts."""
        meta = get_font_metadata(Font.SANSSERIF_LIGHT)
        assert meta.path == "cjk_japanese_noto_sans/light.otf"
        assert meta.abs_path.endswith("cjk_japanese_noto_sans/light.otf")
        assert meta.url.startswith("https://raw.githubusercontent.com/")
        assert meta.md5 == "88ce9ab7e76fed605c822b52605ac2fd"

    def test_get_font_metadata_invalid_font(self):
        """Test get_font_metadata raises ValueError for an invalid/unmapped font."""

        class InvalidFont(FontBase):
            INVALID = "FontBase.INVALID"

        with pytest.raises(ValueError, match="Font InvalidFont.INVALID not found in FONT_RESOURCES."):
            get_font_metadata(InvalidFont.INVALID)
