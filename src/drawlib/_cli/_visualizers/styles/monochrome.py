# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Specialized visualizer for MonochromeStyles presets."""

from __future__ import annotations

from drawlib._cli._visualizers.styles.base import render_styles_matrix
from drawlib._core.l3_images import Dimage
from drawlib._preset_styles import BaseStyles


class MonochromeStylesVisualizer:
    """Visualizer specialized for MonochromeStyles catalogs."""

    @staticmethod
    def render(
        styles: BaseStyles,
        name: str,
        *,
        page: int = 1,
        page_size: int = 25,
        filter_color: str | None = None,
        grid: bool = False,
        no_cache: bool = False,
    ) -> Dimage:
        """Render MonochromeStyles matrix."""
        return render_styles_matrix(
            styles,
            name,
            page=page,
            page_size=page_size,
            filter_color=filter_color,
            grid=grid,
            no_cache=no_cache,
        )
