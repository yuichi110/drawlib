# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Icon utility module for canvas operations."""

from drawlib._core.l2_types import IconStyle
from drawlib._core.l3_styles import Style


class IconUtil:
    """A utility class for handling icon styles."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    @staticmethod
    def validate_icon_style(style: Style) -> None:
        """Validate that required icon properties are set in Style.

        Args:
            style: The Style instance to validate.

        Raises:
            ValueError: If style does not support icons or icon_color is None.
        """
        if "icon" not in style.supports:
            raise ValueError(f"Style cannot be used for icons. Declared supports: {set(style.supports)}.")
        if style.icon_color is None:
            raise ValueError("Icon drawing requires attribute 'icon_color', but it is None in the provided Style.")

    @staticmethod
    def format_style(
        style: Style,
        default_icon_style: IconStyle | None = None,
    ) -> Style:
        """Validate and format icon style."""
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')

        IconUtil.validate_icon_style(style)

        if style.icon_style is None and default_icon_style is not None:
            style = style.patch(icon_style=default_icon_style)

        return style
