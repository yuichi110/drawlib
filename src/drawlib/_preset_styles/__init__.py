# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Private preset_styles package for drawlib."""

from drawlib._preset_styles._base import (
    BasePresetStyles,
    PresetStyles,
)
from drawlib._preset_styles._style_default import (
    DefaultStyles,
    default_styles,
)
from drawlib._preset_styles._style_essentials import (
    EssentialsStyles,
    essentials_styles,
)
from drawlib._preset_styles._style_google import (
    GoogleStyles,
    google_styles,
)
from drawlib._preset_styles._style_monochrome import (
    MonochromeStyles,
    monochrome_styles,
)

__all__ = [
    "BasePresetStyles",
    "DefaultStyles",
    "EssentialsStyles",
    "GoogleStyles",
    "MonochromeStyles",
    "PresetStyles",
    "default_styles",
    "essentials_styles",
    "google_styles",
    "monochrome_styles",
]
