# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public preset_styles module for drawlib."""

from drawlib._preset_styles import (
    BaseStyles,
    DefaultStyles,
    GoogleStyles,
    MonochromeStyles,
    StylesDefault,
    StylesDefaultDark,
    StylesDefaultLight,
    StylesGoogle,
    StylesMonochrome,
    default_dark_styles,
    default_light_styles,
    default_styles,
    google_styles,
    monochrome_styles,
)

EssentialsStyles = DefaultStyles
essentials_styles = default_styles

__all__ = [
    "BaseStyles",
    "DefaultStyles",
    "EssentialsStyles",
    "GoogleStyles",
    "MonochromeStyles",
    "StylesDefault",
    "StylesDefaultDark",
    "StylesDefaultLight",
    "StylesGoogle",
    "StylesMonochrome",
    "default_dark_styles",
    "default_light_styles",
    "default_styles",
    "essentials_styles",
    "google_styles",
    "monochrome_styles",
]
