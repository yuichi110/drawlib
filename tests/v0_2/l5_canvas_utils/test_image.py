# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib.v0_2.private.l3_styles import SYSTEM_DEFAULT_IMAGE_STYLE, ImageStyle
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas_utils._image import ImageUtil


class TestImageUtil:
    """Unit tests for the ImageUtil static helper class."""

    def test_format_style(self) -> None:
        """Verifies format_style merges ImageStyle correctly and validates input types."""
        dtheme.apply_official_theme("default")

        # 1. Test None style (returns default style merged with system default)
        formatted_none = ImageUtil.format_style(None)
        assert isinstance(formatted_none, ImageStyle)
        assert formatted_none.lwidth == dtheme.imagestyles.get("").lwidth

        # 2. Test string style (resolves name in theme cache)
        formatted_str = ImageUtil.format_style("blue")
        assert formatted_str.lcolor == dtheme.imagestyles.get("blue").lcolor

        # 3. Test ImageStyle object (creates deep copy and merges)
        custom_style = ImageStyle(lwidth=10.0)
        formatted_obj = ImageUtil.format_style(custom_style)
        assert formatted_obj.lwidth == 10.0
        assert formatted_obj is not custom_style  # Verify different instance (copied)

        # 4. Test invalid style types raise ValueError
        with pytest.raises(ValueError):
            ImageUtil.format_style(123)  # type: ignore
