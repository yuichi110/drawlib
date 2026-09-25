# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas_utils._image import ImageUtil


class TestImageUtil:
    """Unit tests for the ImageUtil static helper class."""

    def test_format_style(self) -> None:
        """Verifies format_style handles Style and validates input types."""
        # 1. Test None style (returns Style with image_border_width=0)
        formatted_none = ImageUtil.format_style(None)
        assert isinstance(formatted_none, Style)
        assert formatted_none.image_border_width == 0

        # 2. Test Style object
        custom_style = Style(image_border_width=10.0)
        formatted_obj = ImageUtil.format_style(custom_style)
        assert formatted_obj.image_border_width == 10.0

        # 3. Test invalid style types raise TypeError
        with pytest.raises(TypeError):
            ImageUtil.format_style(123)  # type: ignore
        with pytest.raises(TypeError):
            ImageUtil.format_style("primary")  # type: ignore
