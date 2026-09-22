# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cycle SmartArt implementation module."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Literal

from drawlib._charts.bar_chart._series import DEFAULT_CHART_PALETTE
from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeAngle,
    TypeColor,
    TypeCoordinate,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import arrow_arc as canvas_arrow_arc
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line_arc as canvas_line_arc
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._preset_styles import get_style


class _CycleItem:
    """Internal container for a single step in Cycle."""

    def __init__(
        self,
        text: str,
        description: str = "",
        style: Style | None = None,
        textstyle: Style | None = None,
        description_style: Style | None = None,
        arrow_style: Style | None = None,
    ) -> None:
        self.text = text
        self.description = description
        self.style = style
        self.textstyle = textstyle
        self.description_style = description_style
        self.arrow_style = arrow_style


class Cycle:
    """SmartArt component for circular and cyclical process diagrams (e.g. PDCA, life cycles)."""

    @guarded
    def __init__(
        self,
        clockwise: bool = True,
        start_angle: TypeAngle = 90.0,
        node_shape: Literal["circle", "rectangle", "none"] = "circle",
        node_radius: TypePosFloat = 8.0,
        node_size: tuple[TypePosFloat, TypePosFloat] = (18.0, 10.0),
        description_placement: Literal["inside", "outside"] = "inside",
        arrow_type: Literal["arc", "line", "none"] = "arc",
        arrow_width: TypePosFloat = 2.0,
        arrow_head_width: TypePosFloat = 4.5,
        arrow_color_mode: Literal["monochrome", "match_source", "match_target"] = "match_source",
        arrow_gap: TypePosFloat = 2.5,
        default_style: str | Style | None = None,
        default_textstyle: str | Style | None = None,
        default_description_style: str | Style | None = None,
        default_arrow_style: str | Style | None = None,
        palette: Sequence[TypeColor] | None = None,
        center_text: TypeStr = "",
        center_description: TypeStr = "",
        center_radius: TypePosFloat = 10.0,
        center_style: str | Style | None = None,
        center_textstyle: str | Style | None = None,
        center_description_style: str | Style | None = None,
    ) -> None:
        """Initialize Cycle SmartArt.

        Args:
            clockwise: Whether the process flows clockwise (True) or counter-clockwise (False).
                Defaults to True.
            start_angle: Angle in degrees for the first node (0 is right, 90 is top). Defaults to 90.0.
            node_shape: Shape of the step nodes ("circle", "rectangle", or "none"). Defaults to "circle".
            node_radius: Radius of nodes when node_shape is "circle". Defaults to 8.0.
            node_size: Width and height tuple (w, h) when node_shape is "rectangle". Defaults to (18.0, 10.0).
            description_placement: Placement of description text ("inside" or "outside" node).
                Defaults to "inside".
            arrow_type: Connecting arrow style ("arc" for curved block arrow, "line" for arc line, "none").
                Defaults to "arc".
            arrow_width: Tail thickness of block arrow or line width of arc line arrow. Defaults to 2.0.
            arrow_head_width: Head width of block arrow. Defaults to 4.5.
            arrow_color_mode: Coloring mode for connecting arrows ("match_source", "match_target", "monochrome").
                Defaults to "match_source".
            arrow_gap: Distance margin between arrow endpoints and step nodes. Defaults to 2.5.
            default_style: Default style for step nodes. If None, colors from palette are used.
            default_textstyle: Default style for primary step text (titles).
            default_description_style: Default style for secondary description text.
            default_arrow_style: Default style for connecting arrows.
            palette: Optional sequence of colors to automatically style consecutive steps.
            center_text: Optional title text for a center node (creating a Radial Cycle).
            center_description: Optional supporting description text for the center node.
            center_radius: Radius of the center circle. Defaults to 10.0.
            center_style: Custom style for the center node circle.
            center_textstyle: Custom style for the center node title.
            center_description_style: Custom style for the center node description text.
        """
        self._clockwise = bool(clockwise)
        self._start_angle = float(start_angle)
        self._node_shape = node_shape
        self._node_radius = float(node_radius)
        self._node_size = (float(node_size[0]), float(node_size[1]))
        self._description_placement = description_placement
        self._arrow_type = arrow_type
        self._arrow_width = float(arrow_width)
        self._arrow_head_width = float(arrow_head_width)
        self._arrow_color_mode = arrow_color_mode
        self._arrow_gap = float(arrow_gap)
        self._default_style = get_style(default_style) if default_style is not None else None
        self._default_textstyle = get_style(default_textstyle) if default_textstyle is not None else None
        self._default_description_style = (
            get_style(default_description_style) if default_description_style is not None else None
        )
        self._default_arrow_style = get_style(default_arrow_style) if default_arrow_style is not None else None
        self._palette = list(palette) if palette is not None else None

        self._center_text = center_text
        self._center_description = center_description
        self._center_radius = float(center_radius)
        self._center_style = get_style(center_style) if center_style is not None else None
        self._center_textstyle = get_style(center_textstyle) if center_textstyle is not None else None
        self._center_description_style = (
            get_style(center_description_style) if center_description_style is not None else None
        )

        self._items: list[_CycleItem] = []

    @property
    def items(self) -> list[_CycleItem]:
        """Return the registered cycle items."""
        return self._items

    @guarded
    def append(
        self,
        text: TypeStr,
        description: TypeStr = "",
        style: str | Style | None = None,
        textstyle: str | Style | None = None,
        description_style: str | Style | None = None,
        arrow_style: str | Style | None = None,
    ) -> None:
        """Append a step to the cycle.

        Args:
            text: Primary step title text.
            description: Optional supporting description text.
            style: Custom Style or preset string for this step node.
            textstyle: Custom Style or preset string for the title text.
            description_style: Custom Style or preset string for the description text.
            arrow_style: Custom Style or preset string for the arrow following this step.
        """
        resolved_style = get_style(style) if style is not None else None
        resolved_textstyle = get_style(textstyle) if textstyle is not None else None
        resolved_desc_style = get_style(description_style) if description_style is not None else None
        resolved_arrow_style = get_style(arrow_style) if arrow_style is not None else None

        item = _CycleItem(
            text=text,
            description=description,
            style=resolved_style,
            textstyle=resolved_textstyle,
            description_style=resolved_desc_style,
            arrow_style=resolved_arrow_style,
        )
        self._items.append(item)

    @guarded
    def extend(
        self,
        texts: list[TypeStr],
        descriptions: list[TypeStr] | None = None,
    ) -> None:
        """Extend the cycle with multiple step titles.

        Args:
            texts: List of step title texts.
            descriptions: Optional list of corresponding descriptions.
        """
        for i, text in enumerate(texts):
            desc = descriptions[i] if descriptions and i < len(descriptions) else ""
            self.append(text=text, description=desc)

    @guarded
    def insert(
        self,
        index: int,
        text: TypeStr,
        description: TypeStr = "",
        style: str | Style | None = None,
        textstyle: str | Style | None = None,
        description_style: str | Style | None = None,
        arrow_style: str | Style | None = None,
    ) -> None:
        """Insert a step at the specified index.

        Args:
            index: Position index to insert the step.
            text: Primary step title text.
            description: Optional supporting description text.
            style: Custom Style or preset string for this step node.
            textstyle: Custom Style or preset string for the title text.
            description_style: Custom Style or preset string for the description text.
            arrow_style: Custom Style or preset string for the arrow following this step.
        """
        resolved_style = get_style(style) if style is not None else None
        resolved_textstyle = get_style(textstyle) if textstyle is not None else None
        resolved_desc_style = get_style(description_style) if description_style is not None else None
        resolved_arrow_style = get_style(arrow_style) if arrow_style is not None else None

        item = _CycleItem(
            text=text,
            description=description,
            style=resolved_style,
            textstyle=resolved_textstyle,
            description_style=resolved_desc_style,
            arrow_style=resolved_arrow_style,
        )
        self._items.insert(index, item)

    @guarded
    def set_center(
        self,
        text: TypeStr,
        description: TypeStr = "",
        radius: TypePosFloat | None = None,
        style: str | Style | None = None,
        textstyle: str | Style | None = None,
        description_style: str | Style | None = None,
    ) -> None:
        """Configure the optional center node for a Radial Cycle.

        Args:
            text: Center node title text.
            description: Optional supporting description for the center node.
            radius: Radius of the center circle. If None, retains current center_radius.
            style: Custom Style or preset string for the center circle.
            textstyle: Custom Style or preset string for the center title text.
            description_style: Custom Style or preset string for the center description text.
        """
        self._center_text = text
        self._center_description = description
        if radius is not None:
            self._center_radius = float(radius)
        if style is not None:
            self._center_style = get_style(style)
        if textstyle is not None:
            self._center_textstyle = get_style(textstyle)
        if description_style is not None:
            self._center_description_style = get_style(description_style)

    @guarded
    def draw(
        self,
        xy: TypeCoordinate,
        radius: TypePosFloat = 35.0,
        align: Literal["center", "bottom_left"] = "center",
    ) -> None:
        """Draw the cycle diagram at the specified coordinate.

        Args:
            xy: Coordinate tuple (x, y) anchoring the diagram.
            radius: Orbit radius from diagram center to step nodes. Defaults to 35.0.
            align: Anchor alignment ("center" if xy is center, "bottom_left" if xy is bottom-left bounding corner).
                Defaults to "center".
        """
        orbit_r = float(radius)
        num_items = len(self._items)

        # Resolve center coordinate
        if align == "center":
            cx, cy = float(xy[0]), float(xy[1])
        else:
            node_half_extent = (
                self._node_radius
                if self._node_shape == "circle"
                else max(self._node_size[0], self._node_size[1]) / 2.0
            )
            extra_margin = 8.0 if self._description_placement == "outside" else 2.0
            offset = orbit_r + node_half_extent + extra_margin
            cx, cy = float(xy[0]) + offset, float(xy[1]) + offset

        if num_items == 0:
            if self._center_text:
                self._draw_center_node(cx, cy)
            return

        angles = self._compute_item_angles(num_items)

        # 1. Draw connecting arrows if multiple items exist
        if num_items >= 2 and self._arrow_type != "none":
            self._draw_arrows(cx, cy, orbit_r, num_items, angles)

        # 2. Draw center node if specified
        if self._center_text:
            self._draw_center_node(cx, cy)

        # 3. Draw nodes and their texts
        for i, item in enumerate(self._items):
            ang_rad = math.radians(angles[i])
            nx = cx + orbit_r * math.cos(ang_rad)
            ny = cy + orbit_r * math.sin(ang_rad)
            node_style = self._resolve_item_style(item, i)

            # Render shape
            if self._node_shape == "circle":
                canvas_circle(xy=(nx, ny), radius=self._node_radius, style=node_style)
            elif self._node_shape == "rectangle":
                canvas_rectangle(
                    xy=(nx, ny),
                    width=self._node_size[0],
                    height=self._node_size[1],
                    r=2.0,
                    style=node_style,
                )

            # Render texts
            self._draw_item_texts(item, nx, ny, ang_rad)

    def _compute_item_angles(self, num_items: int) -> list[float]:
        """Compute angular placement for each item in degrees."""
        delta = 360.0 / num_items
        angles = []
        for i in range(num_items):
            if self._clockwise:
                ang = (self._start_angle - i * delta) % 360.0
            else:
                ang = (self._start_angle + i * delta) % 360.0
            angles.append(ang)
        return angles

    def _get_node_angular_margin(self, orbit_r: float, delta: float) -> float:
        """Compute the angular margin needed around nodes to avoid arrow collisions."""
        if self._node_shape == "circle":
            node_half_extent = self._node_radius
        elif self._node_shape == "rectangle":
            node_half_extent = math.hypot(self._node_size[0], self._node_size[1]) / 2.0
        else:
            node_half_extent = 4.0

        margin_rad = (node_half_extent + self._arrow_gap) / orbit_r
        margin_deg = math.degrees(margin_rad)
        max_margin = delta * 0.42
        return min(margin_deg, max_margin)

    def _draw_arrows(
        self,
        cx: float,
        cy: float,
        orbit_r: float,
        num_items: int,
        angles: list[float],
    ) -> None:
        """Draw connecting arc arrows between consecutive items."""
        delta = 360.0 / num_items
        margin_deg = self._get_node_angular_margin(orbit_r, delta)

        for i in range(num_items):
            next_i = (i + 1) % num_items
            arrow_style = self._resolve_arrow_style(i, next_i)

            if self._clockwise:
                # Tail leaves current item, head points towards next item
                tail_ang = (angles[i] - margin_deg) % 360.0
                head_ang = (angles[next_i] + margin_deg) % 360.0
                a_start, a_end = head_ang, tail_ang
                arc_head = "<-"
            else:
                tail_ang = (angles[i] + margin_deg) % 360.0
                head_ang = (angles[next_i] - margin_deg) % 360.0
                a_start, a_end = tail_ang, head_ang
                arc_head = "->"

            if self._arrow_type == "arc":
                arc_span = (a_end - a_start) % 360.0
                adaptive_head_angle = max(3.0, min(8.0, arc_span * 0.35))
                canvas_arrow_arc(
                    xy=(cx, cy),
                    width=orbit_r * 2.0,
                    height=orbit_r * 2.0,
                    tail_width=self._arrow_width,
                    head_width=self._arrow_head_width,
                    head_angle=adaptive_head_angle,
                    head=arc_head,
                    angle_start=a_start,
                    angle_end=a_end,
                    style=arrow_style,
                )
            elif self._arrow_type == "line":
                canvas_line_arc(
                    xy=(cx, cy),
                    width=orbit_r * 2.0,
                    height=orbit_r * 2.0,
                    arrowhead=arc_head,
                    linewidth=self._arrow_width,
                    angle_start=a_start,
                    angle_end=a_end,
                    style=arrow_style,
                )

    def _resolve_item_style(self, item: _CycleItem, index: int) -> Style:
        """Determine final Style for a step node."""
        if item.style is not None:
            return item.style
        if self._default_style is not None:
            return self._default_style

        palette = self._palette if self._palette is not None else DEFAULT_CHART_PALETTE
        color = palette[index % len(palette)]
        return Style(
            fill_color=color,
            line_color=(255, 255, 255, 1.0),
            line_width=1.5,
        )

    def _resolve_arrow_style(self, from_idx: int, to_idx: int) -> Style:
        """Determine final Style for a connecting arrow."""
        item = self._items[from_idx]
        if item.arrow_style is not None:
            return item.arrow_style
        if self._default_arrow_style is not None:
            return self._default_arrow_style

        palette = self._palette if self._palette is not None else DEFAULT_CHART_PALETTE

        if self._arrow_color_mode == "match_source":
            from_style = self._resolve_item_style(item, from_idx)
            color = from_style.fill_color or palette[from_idx % len(palette)]
        elif self._arrow_color_mode == "match_target":
            to_style = self._resolve_item_style(self._items[to_idx], to_idx)
            color = to_style.fill_color or palette[to_idx % len(palette)]
        else:
            color = (170, 170, 170, 0.9)

        if self._arrow_type == "arc":
            return Style(fill_color=color, line_width=0)
        return Style(line_color=color, line_width=self._arrow_width)

    def _draw_item_texts(
        self,
        item: _CycleItem,
        nx: float,
        ny: float,
        ang_rad: float,
    ) -> None:
        """Render primary title and optional description text for a step node."""
        has_desc = bool(item.description.strip())
        is_colored = self._node_shape in {"circle", "rectangle"}

        default_title_color = (255, 255, 255, 1.0) if is_colored else (40, 40, 40, 1.0)
        default_desc_color = (255, 255, 255, 0.92) if is_colored else (80, 80, 80, 1.0)

        t_style = item.textstyle or self._default_textstyle or Style(
            text_size=9.5 if self._node_shape != "rectangle" else 9.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=default_title_color,
            text_halign="center",
            text_valign="center",
        )

        if not has_desc:
            canvas_text(xy=(nx, ny), text=item.text, style=t_style)
            return

        if self._description_placement == "inside":
            # Title on top, description on bottom inside the node
            if self._node_shape == "circle":
                title_y = ny + self._node_radius * 0.22
                desc_y = ny - self._node_radius * 0.35
                desc_size = max(6.0, self._node_radius * 0.7)
            elif self._node_shape == "rectangle":
                title_y = ny + self._node_size[1] * 0.20
                desc_y = ny - self._node_size[1] * 0.25
                desc_size = 6.5
            else:
                title_y = ny + 2.0
                desc_y = ny - 2.5
                desc_size = 7.0

            d_style = item.description_style or self._default_description_style or Style(
                text_size=desc_size,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=default_desc_color,
                text_halign="center",
                text_valign="center",
            )
            canvas_text(xy=(nx, title_y), text=item.text, style=t_style)
            canvas_text(xy=(nx, desc_y), text=item.description, style=d_style)

        else:
            # Title inside node, description placed radially outward
            canvas_text(xy=(nx, ny), text=item.text, style=t_style)

            node_half_extent = (
                self._node_radius
                if self._node_shape == "circle"
                else max(self._node_size[0], self._node_size[1]) / 2.0
            )
            rad_offset = node_half_extent + 3.5
            dx = nx + rad_offset * math.cos(ang_rad)
            dy = ny + rad_offset * math.sin(ang_rad)

            cos_a = math.cos(ang_rad)
            sin_a = math.sin(ang_rad)
            halign: Literal["left", "center", "right"] = "center"
            if cos_a > 0.35:
                halign = "left"
            elif cos_a < -0.35:
                halign = "right"

            valign: Literal["top", "center", "bottom"] = "center"
            if sin_a > 0.5:
                valign = "bottom"
            elif sin_a < -0.5:
                valign = "top"

            d_style = item.description_style or self._default_description_style or Style(
                text_size=8.0,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=(70, 70, 70, 1.0),
                text_halign=halign,
                text_valign=valign,
            )
            canvas_text(xy=(dx, dy), text=item.description, style=d_style)

    def _draw_center_node(self, cx: float, cy: float) -> None:
        """Render the center node for Radial Cycle diagrams."""
        c_style = self._center_style or Style(
            fill_color=(245, 247, 250, 1.0),
            line_color=(185, 195, 210, 1.0),
            line_width=1.5,
        )
        canvas_circle(xy=(cx, cy), radius=self._center_radius, style=c_style)

        has_desc = bool(self._center_description.strip())
        t_style = self._center_textstyle or Style(
            text_size=11.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(50, 60, 80, 1.0),
            text_halign="center",
            text_valign="center",
        )

        if not has_desc:
            canvas_text(xy=(cx, cy), text=self._center_text, style=t_style)
        else:
            title_y = cy + self._center_radius * 0.22
            desc_y = cy - self._center_radius * 0.35
            d_style = self._center_description_style or Style(
                text_size=7.5,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=(90, 100, 120, 1.0),
                text_halign="center",
                text_valign="center",
            )
            canvas_text(xy=(cx, title_y), text=self._center_text, style=t_style)
            canvas_text(xy=(cx, desc_y), text=self._center_description, style=d_style)
