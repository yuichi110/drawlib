# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Icon utility module for canvas operations."""

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_styles import SYSTEM_DEFAULT_ICON_STYLE, Style
from drawlib._preset_styles import get_style


class IconUtil(StaticContainer):
    """A utility class for handling icon styles."""

    @staticmethod
    def format_style(
        style: Style | str | None,
        default_icon_style: str | None = None,
    ) -> Style:
        if default_icon_style is not None and not isinstance(default_icon_style, str):
            raise ValueError(f"default_icon_style must be str or None, but {type(default_icon_style)} given.")
        if style is None or isinstance(style, (Style, str)):
            formatted_style = get_style(style).copy()
        else:
            raise ValueError(f'Arg "style" must be Style or None, but {type(style)} given.')

        formatted_style = SYSTEM_DEFAULT_ICON_STYLE.merge(formatted_style)
        return formatted_style
