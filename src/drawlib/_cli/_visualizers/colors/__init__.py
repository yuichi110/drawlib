# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color visualizers package and chart dispatcher."""

from __future__ import annotations

from typing import Literal

from drawlib._cli._visualizers.colors.base import (
    BaseColorVisualizer,
    SortMode,
    calc_grid_cols,
    draw_color_tile,
    sort_colors,
)
from drawlib._cli._visualizers.colors.css import CssColorVisualizer
from drawlib._cli._visualizers.colors.default import DefaultColorVisualizer
from drawlib._cli._visualizers.colors.google import GoogleColorVisualizer
from drawlib._cli._visualizers.colors.monochrome import MonochromeColorVisualizer
from drawlib._core.l3_colors import BaseColors
from drawlib._core.l3_images import Dimage


def render_color_chart(
    colors: BaseColors | type[BaseColors],
    name: str,
    *,
    sort_mode: SortMode = "hsv",
    grid: bool = False,
    no_cache: bool = False,
) -> Dimage:
    """Render a dynamic visual color chart for any BaseColors instance.

    Dispatches to palette-specific visualizer (Google, Default, Monochrome, CSS).

    Args:
        colors (BaseColors | type[BaseColors]): BaseColors instance or class containing color attributes.
        name (str): Display name of the color palette.
        sort_mode (SortMode): Sorting strategy ('hsv', 'name', or 'raw'). Defaults to 'hsv'.
        grid (bool): Whether to overlay coordinate grid. Defaults to False.
        no_cache (bool): If True, bypass cache and force re-rendering. Defaults to False.

    Returns:
        Dimage: Rendered in-memory image.
    """
    cls_name = colors.__name__ if isinstance(colors, type) else colors.__class__.__name__

    visualizer: BaseColorVisualizer
    if "Google" in cls_name:
        visualizer = GoogleColorVisualizer()
    elif "Monochrome" in cls_name:
        visualizer = MonochromeColorVisualizer()
    elif "Css" in cls_name:
        visualizer = CssColorVisualizer()
    else:
        visualizer = DefaultColorVisualizer()

    return visualizer.render(
        colors=colors,
        name=name,
        sort_mode=sort_mode,
        grid=grid,
        no_cache=no_cache,
    )


__all__ = [
    "BaseColorVisualizer",
    "CssColorVisualizer",
    "DefaultColorVisualizer",
    "GoogleColorVisualizer",
    "MonochromeColorVisualizer",
    "SortMode",
    "calc_grid_cols",
    "draw_color_tile",
    "render_color_chart",
    "sort_colors",
]
