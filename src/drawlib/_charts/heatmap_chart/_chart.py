# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HeatmapChart container class implementation."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pydantic import validate_call

import drawlib._charts.heatmap_chart._renderer as _renderer_module
from drawlib._charts._common._base import draw_with_box_overrides
from drawlib._charts._common._types import DrawDirection, FormatterType, Orientation
from drawlib._charts.heatmap_chart._models import (
    Cell,
    Row,
    draw_colorbar_common,
    draw_stops_legend_common,
    extract_heatmap_color,
    resolve_style_stops,
)
from drawlib._core.l3_colors import Color
from drawlib._core.l3_styles import Style


class HeatmapChart:
    """Configurable container and builder for 2D matrix/grid heatmaps."""

    @validate_call
    def __init__(
        self,
        *,
        styles: list[Style] | None = None,
        min_style: Style | None = None,
        max_style: Style | None = None,
        x_categories: list[str] | None = None,
        y_categories: list[str] | None = None,
        axis_line_style: Style | None = None,
        width: float = 80.0,
        height: float = 55.0,
        min_value: float | None = None,
        max_value: float | None = None,
        cell_gap: float = 0.6,
        cell_r: float = 0.4,
        cell_line_style: Style | None = None,
        value_format: FormatterType = None,
        auto_contrast_text: bool = True,
        x_label_position: Literal["bottom", "top"] = "bottom",
        y_origin: Literal["top", "bottom"] = "top",
        axis_text_style: Style | None = None,
        value_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None:
        """Initialize HeatmapChart.

        Args:
            styles: Sequence of 2 or more Style objects defining color stops from min_value to max_value.
            min_style: Style for minimum value when styles is omitted.
            max_style: Style for maximum value when styles is omitted.
            x_categories: Column category labels along the horizontal axis.
            y_categories: Row category labels along the vertical axis.
            axis_line_style: Optional Style for outer matrix plot frame lines.
            width: Total width of the chart container. Defaults to 80.0.
            height: Total height of the chart container. Defaults to 55.0.
            min_value: Explicit minimum scale value. If None, inferred from data.
            max_value: Explicit maximum scale value. If None, inferred from data.
            cell_gap: Spacing gap between adjacent matrix cells in canvas units. Defaults to 0.6.
            cell_r: Corner rounding radius for matrix cells. Defaults to 0.4.
            cell_line_style: Optional Style overriding cell border stroke.
            value_format: Formatter string or callable for numerical cell values.
            auto_contrast_text: Whether to automatically switch cell value text color between dark and light
                based on cell background luminance. Defaults to True.
            x_label_position: Placement of X-axis column labels ("bottom" or "top"). Defaults to "bottom".
            y_origin: Vertical ordering of rows ("top" places row 0 at top; "bottom" places row 0 at bottom).
                Defaults to "top".
            axis_text_style: Optional Style for row and column category labels.
            value_text_style: Optional Style for numerical value labels inside cells.
            background_style: Optional Style for the chart background card.
            title: Title text displayed at the top of the chart. Defaults to "".
            title_style: Optional Style for the chart title typography.

        Raises:
            ValueError: If neither styles (>= 2) nor (min_style, max_style) are provided.
        """
        self._style_stops: list[Style] = resolve_style_stops(styles, min_style, max_style)
        self.x_categories: list[str] = list(x_categories) if x_categories is not None else []
        self.y_categories: list[str] = list(y_categories) if y_categories is not None else []
        self.axis_line_style: Style | None = axis_line_style
        self.width: float = float(width)
        self.height: float = float(height)
        self.min_value: float | None = float(min_value) if min_value is not None else None
        self.max_value: float | None = float(max_value) if max_value is not None else None
        self.cell_gap: float = max(0.0, float(cell_gap))
        self.cell_r: float = max(0.0, float(cell_r))
        self.cell_line_style: Style | None = cell_line_style
        self.value_format: FormatterType = value_format
        self.auto_contrast_text: bool = bool(auto_contrast_text)
        self.x_label_position: Literal["bottom", "top"] = x_label_position
        self.y_origin: Literal["top", "bottom"] = y_origin
        self.axis_text_style: Style | None = axis_text_style
        self.value_text_style: Style | None = value_text_style
        self.background_style: Style | None = background_style
        self.title: str = title
        self.title_style: Style | None = title_style

        self._rows: list[Row] = []
        self._cells: dict[tuple[int, int], Cell] = {}

    @property
    def styles(self) -> list[Style]:
        """List of Style stops defining the heatmap color scale."""
        return list(self._style_stops)

    @property
    def color_stops(self) -> list[Color]:
        """List of extracted Color stops from the configured Style stops."""
        return [extract_heatmap_color(s) for s in self._style_stops]

    @property
    def rows(self) -> list[Row]:
        """List of registered matrix rows."""
        return list(self._rows)

    @property
    def cells(self) -> list[Cell]:
        """List of registered cell overrides."""
        return list(self._cells.values())

    def add_row(
        self,
        name: str,
        values: Sequence[float | None],
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> Row:
        """Add a horizontal row of values to the heatmap matrix.

        Args:
            name: Row label displayed on the Y-axis.
            values: Sequence of numerical cell values (or None for empty cells).
            show: Whether to render this row on the canvas. Defaults to True.
            draw_ratio: Spatial rendering ratio from 0.0 to 1.0. Defaults to 1.0.
            draw_direction: Partial rendering direction ("left_to_right" or "bottom_to_top").

        Returns:
            Row: The newly created and registered row object.
        """
        row = Row(
            name=name,
            values=values,
            show=show,
            draw_ratio=draw_ratio,
            draw_direction=draw_direction,
        )
        row_idx = len(self._rows)
        self._rows.append(row)
        if len(self.y_categories) == row_idx and name:
            self.y_categories.append(name)
        return row

    def set_data(
        self,
        values: Sequence[Sequence[float | None]],
        *,
        x_categories: Sequence[str] | None = None,
        y_categories: Sequence[str] | None = None,
    ) -> HeatmapChart:
        """Replace all matrix rows with a 2D array of values.

        Args:
            values: 2D sequence of row values (rows x columns).
            x_categories: Optional column category labels.
            y_categories: Optional row category labels.

        Returns:
            HeatmapChart: Self for method chaining.
        """
        if x_categories is not None:
            self.x_categories = list(x_categories)
        if y_categories is not None:
            self.y_categories = list(y_categories)

        self._rows.clear()
        for r_idx, row_vals in enumerate(values):
            r_name = self.y_categories[r_idx] if r_idx < len(self.y_categories) else f"Row {r_idx + 1}"
            self._rows.append(Row(name=r_name, values=row_vals))
        return self

    def _resolve_col_index(self, x: int | str) -> int:
        """Resolve column index from integer or x_categories label."""
        if isinstance(x, int):
            if x < 0:
                raise ValueError(f"Column index must be >= 0, got {x}.")
            return x
        if x in self.x_categories:
            return self.x_categories.index(x)
        raise ValueError(f"Column '{x}' not found in x_categories: {self.x_categories}")

    def _resolve_row_index(self, y: int | str) -> int:
        """Resolve row index from integer or y_categories/row name."""
        if isinstance(y, int):
            if y < 0:
                raise ValueError(f"Row index must be >= 0, got {y}.")
            return y
        if y in self.y_categories:
            return self.y_categories.index(y)
        for idx, r in enumerate(self._rows):
            if r.name == y:
                return idx
        raise ValueError(f"Row '{y}' not found in y_categories: {self.y_categories}")

    def set_cell(
        self,
        x: int | str,
        y: int | str,
        value: float | None,
        *,
        label: str = "",
        style: Style | None = None,
        show: bool = True,
    ) -> Cell:
        """Set or override a specific matrix cell by column and row index or category name.

        Args:
            x: Zero-based column index or column category name.
            y: Zero-based row index or row category name.
            value: Numerical cell value, or None for an empty cell.
            label: Custom text label overriding the formatted numeric value. Defaults to "".
            style: Optional explicit Style overriding color-scale fill and border for this cell.
            show: Whether to render this cell. Defaults to True.

        Returns:
            Cell: The registered cell override object.
        """
        col_idx = self._resolve_col_index(x)
        row_idx = self._resolve_row_index(y)
        cell = Cell(
            x=col_idx,
            y=row_idx,
            value=value,
            label=label,
            style=style,
            show=show,
        )
        self._cells[(col_idx, row_idx)] = cell
        return cell

    def _get_effective_range(self) -> tuple[float, float]:
        """Compute effective (min_value, max_value) across the full dataset."""
        all_vals: list[float] = []
        for r in self._rows:
            for v in r.values:
                if v is not None:
                    all_vals.append(v)
        for c in self._cells.values():
            if c.value is not None:
                all_vals.append(c.value)

        data_min = min(all_vals) if all_vals else 0.0
        data_max = max(all_vals) if all_vals else 1.0
        eff_min = self.min_value if self.min_value is not None else data_min
        eff_max = self.max_value if self.max_value is not None else data_max
        if eff_max <= eff_min:
            eff_max = eff_min + 1.0
        return (eff_min, eff_max)

    def get_size(self) -> tuple[float, float]:
        """Get the total dimensions (width, height) of this heatmap chart."""
        return (self.width, self.height)

    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        *,
        width: float | None = None,
        height: float | None = None,
        align: Literal["bottom_left", "center"] = "bottom_left",
        scale: float = 1.0,
    ) -> None:
        """Render this heatmap chart onto the canvas at coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y) (interpreted via align).
            width: Optional temporary width override for this draw call.
            height: Optional temporary height override for this draw call.
            align: Anchor alignment of xy ("bottom_left" or "center"). Defaults to "bottom_left".
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        draw_with_box_overrides(
            self,
            _renderer_module.draw_heatmap_chart,
            xy,
            width=width,
            height=height,
            align=align,
            scale=scale,
        )

    def draw_colorbar(
        self,
        xy: tuple[float, float],
        text_style: Style,
        *,
        length: float = 30.0,
        thickness: float = 2.2,
        orientation: Orientation = "horizontal",
        num_ticks: int = 5,
        value_format: FormatterType = None,
        label: str = "",
        border_style: Style | None = None,
        scale: float = 1.0,
    ) -> None:
        """Render a continuous gradient colorbar legend for this heatmap.

        Args:
            xy: Bottom-left anchor coordinate (x, y) of the colorbar.
            text_style: Style for tick labels and colorbar title.
            length: Length of the colorbar along its primary axis. Defaults to 30.0.
            thickness: Thickness of the colorbar perpendicular to its axis. Defaults to 2.2.
            orientation: "horizontal" or "vertical". Defaults to "horizontal".
            num_ticks: Number of tick marks/labels (>= 2). Defaults to 5.
            value_format: Optional value formatter overriding chart value_format.
            label: Optional descriptive title label above the colorbar. Defaults to "".
            border_style: Optional Style for colorbar outline and tick marks.
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        eff_min, eff_max = self._get_effective_range()
        fmt = value_format if value_format is not None else self.value_format
        b_style = border_style if border_style is not None else self.axis_line_style
        draw_colorbar_common(
            stops=self.color_stops,
            eff_min=eff_min,
            eff_max=eff_max,
            xy=xy,
            text_style=text_style,
            length=length,
            thickness=thickness,
            orientation=orientation,
            num_ticks=num_ticks,
            value_format=fmt,
            label=label,
            border_style=b_style,
            scale=scale,
        )

    def draw_legend(
        self,
        xy: tuple[float, float],
        text_style: Style,
        orientation: Orientation = "vertical",
        swatch_width: float = 2.4,
        swatch_height: float = 1.2,
        item_gap: float = 4.0,
        *,
        num_steps: int = 5,
        labels: Sequence[str] | None = None,
        scale: float = 1.0,
    ) -> None:
        """Render discrete stepped color swatches for this heatmap at coordinate xy.

        Args:
            xy: Starting placement coordinate (x, y).
            text_style: Base Style for legend text labels.
            orientation: "vertical" or "horizontal". Defaults to "vertical".
            swatch_width: Width of color swatches. Defaults to 2.4.
            swatch_height: Height of color swatches. Defaults to 1.2.
            item_gap: Spacing between consecutive legend items. Defaults to 4.0.
            num_steps: Number of discrete color steps when labels is None. Defaults to 5.
            labels: Optional custom step labels (e.g. ["Low", "Medium", "High"]).
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        eff_min, eff_max = self._get_effective_range()
        draw_stops_legend_common(
            stops=self.color_stops,
            eff_min=eff_min,
            eff_max=eff_max,
            xy=xy,
            text_style=text_style,
            orientation=orientation,
            swatch_width=swatch_width,
            swatch_height=swatch_height,
            item_gap=item_gap,
            num_steps=num_steps,
            value_format=self.value_format,
            labels=labels,
            scale=scale,
        )
