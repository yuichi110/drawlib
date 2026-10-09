# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base color visualizer components and shared drawing routines."""

from __future__ import annotations

import colorsys
import io
import math
from typing import Literal

from PIL import Image

from drawlib import LIB_VERSION
from drawlib._builder._common.cache import CliImageCache, hash_text
from drawlib._core.l3_colors import BaseColors, Color
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_images import Dimage
from drawlib._core.l3_styles import Style
from drawlib.canvas import clear, get_dimage, setup
from drawlib.shapes import rectangle
from drawlib.text import text

SortMode = Literal["hsv", "name", "raw"]
SEMANTIC_KEYS: tuple[str, ...] = ("Primary", "Secondary", "Accent", "Muted", "Danger", "Success")


def sort_colors(items: list[tuple[str, Color]], mode: SortMode) -> list[tuple[str, Color]]:
    """Sort color items by HSV, name, or raw definition order.

    Args:
        items (list[tuple[str, Color]]): List of (name, Color) pairs.
        mode (SortMode): Sorting mode ('hsv', 'name', or 'raw').

    Returns:
        list[tuple[str, Color]]: Sorted list of (name, Color) pairs.
    """
    if mode == "raw":
        return items
    if mode == "name":
        return sorted(items, key=lambda x: x[0].lower())

    def _hsv_key(item: tuple[str, Color]) -> tuple[int, float, float, float]:
        _, col = item
        if col.alpha == 0.0:
            return (0, 0.0, 0.0, 0.0)

        r, g, b = col.r / 255.0, col.g / 255.0, col.b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # Grayscale / Low saturation (< 0.08)
        if s < 0.08:
            return (1, 0.0, -round(v, 3), 0.0)

        # Chromatic colors sorted by Hue, then Value, then Saturation
        return (2, round(h, 2), round(v, 2), round(s, 2))

    return sorted(items, key=_hsv_key)


def draw_color_tile(
    cx: float,
    cy: float,
    tile_w: float,
    tile_h: float,
    col_name: str,
    col: Color,
) -> None:
    """Draw a single color swatch tile with color name and hex code.

    Args:
        cx (float): Center X coordinate.
        cy (float): Center Y coordinate.
        tile_w (float): Tile width.
        tile_h (float): Tile height.
        col_name (str): Color name label.
        col (Color): Color instance.
    """
    if col.alpha == 0.0:
        rectangle(
            (cx, cy),
            width=tile_w - 1.2,
            height=tile_h - 1.2,
            style=Style(
                shape_fill_color=Color(255, 255, 255),
                shape_line_color=Color(180, 180, 180),
                shape_line_width=1,
                shape_line_style="dashed",
                shape_r=0.8,
            ),
        )
        text_color = Color(80, 80, 80)
        hex_str = "Alpha 0.0"
    else:
        rectangle(
            (cx, cy),
            width=tile_w - 1.2,
            height=tile_h - 1.2,
            style=Style(
                shape_fill_color=col,
                shape_line_color=Color(200, 200, 200, 0.6),
                shape_line_width=1,
                shape_r=0.8,
            ),
        )
        lum = (col.r * 299 + col.g * 587 + col.b * 114) / 1000
        text_color = Color(0, 0, 0) if lum > 140 else Color(255, 255, 255)
        hex_str = col.hex

    if len(col_name) >= 16:
        font_size = 6.5
    elif len(col_name) >= 13:
        font_size = 7.5
    elif len(col_name) >= 10:
        font_size = 8.5
    else:
        font_size = 9.0

    label = f"{col_name}\n{hex_str}"
    text(
        (cx, cy),
        label,
        style=Style(
            text_color=text_color,
            text_size=font_size,
            text_font=Font.SANSSERIF_BOLD,
        ),
    )


def calc_grid_cols(n: int, has_semantics: bool, semantic_count: int) -> int:
    """Determine optimal grid columns for color palette items.

    Args:
        n (int): Total number of items.
        has_semantics (bool): Whether palette has semantic theme colors.
        semantic_count (int): Number of semantic colors.

    Returns:
        int: Number of columns for layout.
    """
    if n <= 24:
        cols = 4
    elif n <= 60:
        cols = 6
    else:
        cols = 10
    if has_semantics:
        cols = max(cols, semantic_count)
    return cols


class BaseColorVisualizer:
    """Base visualizer for color palettes."""

    @staticmethod
    def render(
        colors: BaseColors | type[BaseColors],
        name: str,
        *,
        sort_mode: SortMode = "hsv",
        grid: bool = False,
        no_cache: bool = False,
    ) -> Dimage:
        """Render a color palette chart.

        Args:
            colors (BaseColors | type[BaseColors]): Color catalog.
            name (str): Catalog display name.
            sort_mode (SortMode): Sort mode.
            grid (bool): Whether to overlay coordinate grid.
            no_cache (bool): Whether to bypass cache.

        Returns:
            Dimage: Rendered image.
        """
        preset_slug = name.strip().lower().split()[0]
        cache = CliImageCache(enabled=not no_cache)
        cache_key = hash_text(f"colors_chart:{preset_slug}:{sort_mode}:{grid}:{LIB_VERSION}")

        if cache.enabled:
            cached_blob = cache.get(cache_key)
            if cached_blob is not None:
                pil_img = Image.open(io.BytesIO(cached_blob))
                return Dimage(pil_img)

        semantic_items = [(k, getattr(colors, k)) for k in SEMANTIC_KEYS if getattr(colors, k, None) is not None]
        has_semantics = len(semantic_items) > 0

        raw_items = [(k, v) for k, v in colors if k not in SEMANTIC_KEYS]
        items = sort_colors(raw_items, sort_mode)
        n = len(items)

        cols = calc_grid_cols(n, has_semantics, len(semantic_items))
        rows = math.ceil(n / cols)

        tile_w = 17.0
        tile_h = 10.5
        margin_x = 6.0
        margin_y = 6.0
        header_h = 10.0
        semantic_h = 17.0 if has_semantics else 0.0

        canvas_w = int(math.ceil(margin_x * 2 + cols * tile_w))
        canvas_h = int(math.ceil(margin_y * 2 + rows * tile_h + header_h + semantic_h))

        clear()
        setup(width=canvas_w, height=canvas_h, grid=grid)

        title_text = f"{name} ({n} colors)"
        text(
            (canvas_w / 2, canvas_h - margin_y - header_h / 2),
            title_text,
            style=Style(
                text_size=16,
                text_font=Font.SANSSERIF_BOLD,
                text_color=Color(40, 40, 40),
            ),
        )

        if has_semantics:
            sem_title_y = canvas_h - margin_y - header_h - 2.5
            sem_names = ", ".join(k for k, _ in semantic_items)
            text(
                (canvas_w / 2, sem_title_y),
                f"Semantic Theme Colors ({sem_names})",
                style=Style(
                    text_size=9.5,
                    text_font=Font.SANSSERIF_BOLD,
                    text_color=Color(70, 70, 70),
                ),
            )
            sem_total_w = len(semantic_items) * tile_w
            sem_start_x = (canvas_w - sem_total_w) / 2
            sem_cy = sem_title_y - (tile_h / 2 + 2.0)
            for s_idx, (s_name, s_col) in enumerate(semantic_items):
                s_cx = sem_start_x + s_idx * tile_w + tile_w / 2
                draw_color_tile(s_cx, sem_cy, tile_w, tile_h, s_name, s_col)

        start_y = canvas_h - margin_y - header_h - semantic_h
        for idx, (col_name, col) in enumerate(items):
            r_idx = idx // cols
            c_idx = idx % cols

            cx = margin_x + c_idx * tile_w + tile_w / 2
            cy = start_y - (r_idx * tile_h + tile_h / 2)
            draw_color_tile(cx, cy, tile_w, tile_h, col_name, col)

        dimage = get_dimage()
        if cache.enabled:
            bio = io.BytesIO()
            dimage.get_pil_image().save(bio, format="PNG")
            cache.put(
                cache_key=cache_key,
                category="colors",
                preset_name=preset_slug,
                page=1,
                has_grid=grid,
                png_blob=bio.getvalue(),
            )

        return dimage
