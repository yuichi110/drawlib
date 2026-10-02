# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Specialized visualizer for W3C CssColors palettes."""

from __future__ import annotations

from drawlib._cli._visualizers.colors.base import BaseColorVisualizer


class CssColorVisualizer(BaseColorVisualizer):
    """Visualizer specialized for CssColors catalogs."""
