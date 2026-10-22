# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""HeatmapOverlay container class for spatial and diagram hotspot overlays."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, Protocol

from pydantic import validate_call

import drawlib._charts.heatmap_chart._overlay_renderer as _overlay_renderer_module
from drawlib._charts._common._types import BlendMode, FormatterType, Orientation, OverlayMode
from drawlib._charts.heatmap_chart._models import (
    Spot,
    draw_colorbar_common,
    draw_stops_legend_common,
    extract_heatmap_color,
    resolve_style_stops,
)
from drawlib._core import l4_canvas as canvas
from drawlib._core.l3_colors import Color
from drawlib._core.l3_styles import Style


class _HasXYProtocol(Protocol):
    @property
    def xy(self) -> tuple[float, float]: ...


class HeatmapOverlay:
    """Spatial thermal/hotspot heatmap overlay for diagrams (e.g., ClassDiagram) and canvas regions."""

    @validate_call
    def __init__(
        self,
        *,
        styles: list[Style] | None = None,
        min_style: Style | None = None,
        max_style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
        mode: OverlayMode = "smooth",
        blend_mode: BlendMode = "add",
        min_value: float = 0.0,
        max_value: float = 1.0,
        default_radius: float = 15.0,
        max_alpha: float = 0.55,
        levels: int = 4,
        show_contour_lines: bool = True,
        contour_line_width: float = 1.0,
        resolution: int = 240,
        value_format: FormatterType = None,
        value_text_style: Style | None = None,
        border_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None:
        """Initialize HeatmapOverlay.

        Args:
            styles: Sequence of 2 or more Style objects defining thermal color stops from cool (min) to hot (max).
            min_style: Style for minimum intensity when styles is omitted.
            max_style: Style for maximum intensity when styles is omitted.
            width: Optional fixed overlay bounding width. If None, auto-computed from spots.
            height: Optional fixed overlay bounding height. If None, auto-computed from spots.
            mode: Visual rendering mode ("smooth" for Gaussian thermal gradient, "contour" for concentric rings).
                Defaults to "smooth".
            blend_mode: Accumulation mode when smooth hotspots overlap ("add" or "max"). Defaults to "add".
            min_value: Minimum intensity scale value. Defaults to 0.0.
            max_value: Maximum intensity scale value. Defaults to 1.0.
            default_radius: Default hotspot influence radius in canvas units. Defaults to 15.0.
            max_alpha: Peak opacity (0.0 to 1.0) at hotspot centers so underlying diagrams stay readable.
                Defaults to 0.55.
            levels: Number of concentric isoline rings per spot when mode="contour". Defaults to 4.
            show_contour_lines: Whether to draw contour ring stroke outlines in mode="contour". Defaults to True.
            contour_line_width: Stroke width of contour rings in mode="contour". Defaults to 1.0.
            resolution: Pixel grid resolution along the longer axis for mode="smooth". Defaults to 240.
            value_format: Optional formatter string or callable for spot value labels.
            value_text_style: Optional Style for spot annotation labels.
            border_style: Optional Style for drawing an outer bounding frame around the overlay region.
            title: Optional title text displayed above the overlay region. Defaults to "".
            title_style: Optional Style for the overlay title typography.

        Raises:
            ValueError: If neither styles (>= 2) nor (min_style, max_style) are provided.
        """
        self._style_stops: list[Style] = resolve_style_stops(styles, min_style, max_style)
        self.custom_width: float | None = float(width) if width is not None else None
        self.custom_height: float | None = float(height) if height is not None else None
        self.mode: OverlayMode = mode
        self.blend_mode: BlendMode = blend_mode
        self.min_value: float = float(min_value)
        self.max_value: float = float(max_value) if float(max_value) > float(min_value) else float(min_value) + 1.0
        self.default_radius: float = max(0.5, float(default_radius))
        self.max_alpha: float = max(0.05, min(1.0, float(max_alpha)))
        self.levels: int = max(1, int(levels))
        self.show_contour_lines: bool = bool(show_contour_lines)
        self.contour_line_width: float = max(0.0, float(contour_line_width))
        self.resolution: int = max(32, min(1024, int(resolution)))
        self.value_format: FormatterType = value_format
        self.value_text_style: Style | None = value_text_style
        self.border_style: Style | None = border_style
        self.title: str = title
        self.title_style: Style | None = title_style

        self._spots: list[Spot] = []

    @property
    def styles(self) -> list[Style]:
        """List of Style stops defining the thermal color scale."""
        return list(self._style_stops)

    @property
    def color_stops(self) -> list[Color]:
        """List of extracted Color stops from the configured Style stops."""
        return [extract_heatmap_color(s) for s in self._style_stops]

    @property
    def spots(self) -> list[Spot]:
        """List of registered thermal hotspots."""
        return list(self._spots)

    def add_spot(
        self,
        xy: tuple[float, float] | _HasXYProtocol,
        value: float = 1.0,
        radius: float | None = None,
        *,
        label: str = "",
        label_style: Style | None = None,
        style: Style | None = None,
        show: bool = True,
        draw_ratio: float = 1.0,
    ) -> Spot:
        """Add a thermal hotspot at the given coordinate or diagram node position.

        Args:
            xy: Center coordinate tuple (x, y) or a diagram node object exposing an `.xy` attribute
                (such as `ClassNode`).
            value: Numerical intensity/temperature value (mapped between min_value and max_value).
                Defaults to 1.0.
            radius: Influence radius of the hotspot in canvas units. If None, uses default_radius.
            label: Optional text annotation displayed at the hotspot. Defaults to "".
            label_style: Optional custom Style for the hotspot annotation text.
            style: Optional Style overriding the hotspot's contour color.
            show: Whether to render this hotspot. Defaults to True.
            draw_ratio: Spatial rendering ratio in [0.0, 1.0] scaling hotspot intensity/radius.
                Defaults to 1.0.

        Returns:
            Spot: The newly created and registered hotspot object.
        """
        if isinstance(xy, (tuple, list)):
            coord = (float(xy[0]), float(xy[1]))
        else:
            raw_xy = xy.xy
            coord = (float(raw_xy[0]), float(raw_xy[1]))

        eff_r = float(radius) if radius is not None else self.default_radius
        spot = Spot(
            xy=coord,
            value=value,
            radius=eff_r,
            label=label,
            label_style=label_style,
            style=style,
            show=show,
            draw_ratio=draw_ratio,
        )
        self._spots.append(spot)
        return spot

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Compute local enclosing bounding box [min_x, min_y, max_x, max_y] of all spots.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        if self.custom_width is not None and self.custom_height is not None:
            return (0.0, 0.0, self.custom_width, self.custom_height)

        if not self._spots:
            w = self.custom_width if self.custom_width is not None else 40.0
            h = self.custom_height if self.custom_height is not None else 40.0
            return (0.0, 0.0, w, h)

        pad_factor = 1.25 if self.mode == "smooth" else 1.05
        min_x = min(s.xy[0] - s.radius * pad_factor for s in self._spots)
        min_y = min(s.xy[1] - s.radius * pad_factor for s in self._spots)
        max_x = max(s.xy[0] + s.radius * pad_factor for s in self._spots)
        max_y = max(s.xy[1] + s.radius * pad_factor for s in self._spots)

        if self.custom_width is not None:
            cx = (min_x + max_x) / 2.0
            min_x = cx - self.custom_width / 2.0
            max_x = cx + self.custom_width / 2.0
        if self.custom_height is not None:
            cy = (min_y + max_y) / 2.0
            min_y = cy - self.custom_height / 2.0
            max_y = cy + self.custom_height / 2.0

        return (min_x, min_y, max_x, max_y)

    def get_size(self) -> tuple[float, float]:
        """Compute overall dimensions (width, height) of the overlay region."""
        min_x, min_y, max_x, max_y = self.get_bounds()
        return (max(1.0, max_x - min_x), max(1.0, max_y - min_y))

    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        *,
        width: float | None = None,
        height: float | None = None,
        align: Literal["bottom_left", "center"] = "bottom_left",
        scale: float = 1.0,
    ) -> None:
        """Render the thermal heatmap overlay onto the canvas anchored at coordinate xy.

        When overlaying on top of a `ClassDiagram` (or other diagram), pass the same `xy`
        base coordinate used in `diagram.draw(xy=...)` so spot coordinates align 1-to-1.

        Args:
            xy: Base canvas placement coordinate (x, y) (interpreted via align). Defaults to (0.0, 0.0).
            width: Optional temporary width override for this draw call.
            height: Optional temporary height override for this draw call.
            align: Anchor alignment of xy ("bottom_left" or "center"). Defaults to "bottom_left".
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        orig_w, orig_h = self.custom_width, self.custom_height
        try:
            if width is not None:
                self.custom_width = float(width)
            if height is not None:
                self.custom_height = float(height)

            if align == "center":
                min_x, min_y, max_x, max_y = self.get_bounds()
                base_xy = (float(xy[0]) - (min_x + max_x) / 2.0, float(xy[1]) - (min_y + max_y) / 2.0)
            else:
                base_xy = (float(xy[0]), float(xy[1]))

            with canvas.transform(origin=xy, scale=scale):
                _overlay_renderer_module.draw_heatmap_overlay(self, base_xy)
        finally:
            self.custom_width, self.custom_height = orig_w, orig_h

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
        """Render a continuous gradient colorbar legend for this thermal overlay.

        Args:
            xy: Bottom-left anchor coordinate (x, y) of the colorbar.
            text_style: Style for tick labels and colorbar title.
            length: Length of the colorbar along its primary axis. Defaults to 30.0.
            thickness: Thickness of the colorbar perpendicular to its axis. Defaults to 2.2.
            orientation: "horizontal" or "vertical". Defaults to "horizontal".
            num_ticks: Number of tick marks/labels (>= 2). Defaults to 5.
            value_format: Optional value formatter overriding overlay value_format.
            label: Optional descriptive title label above the colorbar. Defaults to "".
            border_style: Optional Style for colorbar outline and tick marks.
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        fmt = value_format if value_format is not None else self.value_format
        b_style = border_style if border_style is not None else self.border_style
        draw_colorbar_common(
            stops=self.color_stops,
            eff_min=self.min_value,
            eff_max=self.max_value,
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
        num_steps: int = 4,
        labels: Sequence[str] | None = None,
        scale: float = 1.0,
    ) -> None:
        """Render discrete stepped color swatches for this overlay at coordinate xy.

        Args:
            xy: Starting placement coordinate (x, y).
            text_style: Base Style for legend text labels.
            orientation: "vertical" or "horizontal". Defaults to "vertical".
            swatch_width: Width of color swatches. Defaults to 2.4.
            swatch_height: Height of color swatches. Defaults to 1.2.
            item_gap: Spacing between consecutive legend items. Defaults to 4.0.
            num_steps: Number of discrete color steps when labels is None. Defaults to 4.
            labels: Optional custom step labels (e.g. ["Safe", "Moderate", "High Risk", "Critical"]).
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        draw_stops_legend_common(
            stops=self.color_stops,
            eff_min=self.min_value,
            eff_max=self.max_value,
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
