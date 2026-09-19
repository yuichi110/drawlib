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
from drawlib._core.l3_styles import (
    SYSTEM_DEFAULT_IMAGE_STYLE,
    ImageStyle,
    Style,
)
from drawlib._core.l4_canvas_utils._utils import get_dict_value_none_keys_removed
from drawlib._theme import get_style


class ImageUtil(StaticContainer):
    """A utility class for handling image styles."""

    @staticmethod
    def format_style(style: ImageStyle | str | None) -> ImageStyle:
        if style is None or isinstance(style, (Style, str)):
            formatted_style = get_style(style).copy()
        else:
            raise ValueError(f'Arg "style" must be ImageStyle or None, but {type(style)} given.')

        formatted_style = SYSTEM_DEFAULT_IMAGE_STYLE.merge(formatted_style)
        return formatted_style
