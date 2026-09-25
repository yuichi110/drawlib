# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Image utility class for drawlib."""

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_styles import Style


class ImageUtil(StaticContainer):
    """A utility class for handling image styles."""

    @staticmethod
    def format_style(style: Style | None = None) -> Style:
        """Validate and format image style."""
        if style is None:
            return Style(image_border_width=0)
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style or None, but {type(style)} given.')
        return style
