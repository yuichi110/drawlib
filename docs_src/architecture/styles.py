# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib styles configuration file."""

from __future__ import annotations

from drawlib.preset_colors import DefaultColors
from drawlib.preset_styles import DefaultStyles

# Configure project-wide drawing styles, custom preset styles, or colors here.
#
# All variables defined here will automatically override or extend drawlib.styles.
#
# Available style presets:
# - DefaultStyles / DefaultColors (Default theme, variants 1-6 available)
# - GoogleStyles / GoogleColors (Google Slides/Docs palette & style)
# - MonochromeStyles / MonochromeColors (Black & white printing style)
#
# Example (switching or extending theme):
#
# from drawlib.preset_colors import GoogleColors
# from drawlib.preset_styles import GoogleStyles
#
# Colors = GoogleColors()
# Styles = GoogleStyles()

Colors = DefaultColors()
Styles = DefaultStyles()
