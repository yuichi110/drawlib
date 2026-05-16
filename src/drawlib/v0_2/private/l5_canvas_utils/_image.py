# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Image utility class for drawlib."""

from drawlib.v0_2.private.l2_models import StaticContainer
from drawlib.v0_2.private.l3_styles import (
    SYSTEM_DEFAULT_IMAGE_STYLE,
    ImageStyle,
)
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas_utils._utils import get_dict_value_none_keys_removed


class ImageUtil(StaticContainer):
    """A utility class for handling image styles."""

    @staticmethod
    def format_style(style: ImageStyle | str | None) -> ImageStyle:
        """Format and retrieve an ImageStyle object based on input parameters.

        Args:
            style (ImageStyle | str | None):
                The style to format. Can be an ImageStyle object, a style name (str),
                or None. If None, the default image style from dtheme.imagestyles is used.

        Returns:
            ImageStyle: The formatted ImageStyle object.

        Raises:
            ValueError: If the input style parameter is invalid or cannot be formatted.

        Notes:
            - The returned style is a merged result of the input style, dtheme.imagestyles.get(),
              and SYSTEM_DEFAULT_IMAGE_STYLE.
            - If style is a string, it is treated as the name of the style to fetch from dtheme.imagestyles.
            - If style is an ImageStyle object, it will be copied before further processing to avoid
              modifying the original object.
        """
        if style is None:
            style = dtheme.imagestyles.get()
        elif isinstance(style, str):
            style = dtheme.imagestyles.get(name=style)
        elif isinstance(style, ImageStyle):
            style = style.copy()
        else:
            raise ValueError()

        style = dtheme.imagestyles.get().merge(style)
        style = SYSTEM_DEFAULT_IMAGE_STYLE.merge(style)
        return style
