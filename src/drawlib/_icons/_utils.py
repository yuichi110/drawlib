# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Icon utility module for canvas operations."""

from drawlib._core.types import Style, TypeIconStyle
from drawlib._core.utils import StaticContainer


class IconUtil(StaticContainer):
    """A utility class for handling icon styles."""

    @staticmethod
    def validate_icon_style(style: Style) -> None:
        """Validate that required icon properties are set in Style.

        Args:
            style: The Style instance to validate.

        Raises:
            ValueError: If icon_color is None.
        """
        if style.icon_color is None:
            raise ValueError("Icon drawing requires attribute 'icon_color', but it is None in the provided Style.")

    @staticmethod
    def format_style(
        style: Style,
        default_icon_style: TypeIconStyle | None = None,
    ) -> Style:
        """Validate and format icon style."""
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')

        IconUtil.validate_icon_style(style)

        if style.icon_style is None and default_icon_style is not None:
            style = style.patch(icon_style=default_icon_style)

        return style
