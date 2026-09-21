# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._core.l3_styles import SYSTEM_DEFAULT_IMAGE_STYLE, Style
from drawlib._core.l4_canvas_utils._image import ImageUtil
from drawlib._preset_styles import get_style


class TestImageUtil:
    """Unit tests for the ImageUtil static helper class."""

    def test_format_style(self) -> None:
        """Verifies format_style merges Style correctly and validates input types."""
        # 1. Test None style (returns default style merged with system default)
        formatted_none = ImageUtil.format_style(None)
        assert isinstance(formatted_none, Style)
        assert formatted_none.line_width == get_style().line_width

        # 2. Test string style
        formatted_str = ImageUtil.format_style("primary")
        assert formatted_str.line_color == get_style("primary").line_color

        # 3. Test Style object (creates deep copy and merges)
        custom_style = Style(line_width=10.0)
        formatted_obj = ImageUtil.format_style(custom_style)
        assert formatted_obj.line_width == 10.0
        assert formatted_obj is not custom_style  # Verify different instance (copied)

        # 4. Test invalid style types raise ValueError
        with pytest.raises(ValueError):
            ImageUtil.format_style(123)  # type: ignore
