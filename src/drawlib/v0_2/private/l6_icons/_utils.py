# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Icon utility module for canvas operations."""

from drawlib.v0_2.private.l2_models import StaticContainer
from drawlib.v0_2.private.l3_styles import SYSTEM_DEFAULT_ICON_STYLE, IconStyle
from drawlib.v0_2.private.l4_theme import dtheme


class IconUtil(StaticContainer):
    """A utility class for handling icon styles."""

    @staticmethod
    def format_style(
        style: IconStyle | str | None,
        default_icon_style: str | None = None,
    ) -> IconStyle:
        """Format and retrieve an IconStyle object based on input parameters.

        Args:
            style (IconStyle | str | None):
                The style to format. Can be an IconStyle object, a style name (str),
                or None. If None, the default icon style from dtheme.iconstyles is used.
            default_icon_style (str | None):
                Default style name to use if style is None or a string.

        Returns:
            IconStyle: The formatted IconStyle object.

        Raises:
            ValueError: If the input style parameter is invalid or cannot be formatted.

        Notes:
            - If default_icon_style is provided, it will override dtheme.iconstyles.get().
            - The returned style is a merged result of the input style, dtheme.iconstyles.get(),
              and SYSTEM_DEFAULT_ICON_STYLE.
        """
        if default_icon_style is None:
            ...
        elif isinstance(default_icon_style, str):
            ...
        else:
            raise ValueError()

        if style is None:
            style = dtheme.iconstyles.get()
        elif isinstance(style, str):
            style = dtheme.iconstyles.get(name=style)
        elif isinstance(style, IconStyle):
            ...
        else:
            raise ValueError()

        style = dtheme.iconstyles.get().merge(style)
        style = SYSTEM_DEFAULT_ICON_STYLE.merge(style)
        return style
