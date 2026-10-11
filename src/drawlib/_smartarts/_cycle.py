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
from typing import Literal

from pydantic import BaseModel, ConfigDict, validate_call

from drawlib._core.l2_types import Angle, Coordinate, PosFloat
from drawlib._core.l3_colors import ColorType, ColorUtil
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import arrow_arc as canvas_arrow_arc
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line_arc as canvas_line_arc
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import transform


class CycleItem(BaseModel):
    """Container for a single step in Cycle."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    text: str
    style: Style
    description: str = ""
    text_style: Style | None = None
    description_style: Style | None = None
    arrow_style: Style | None = None
    show: bool = True


class CycleCenter(BaseModel):
    """Container for the center node in a Radial Cycle."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    text: str
    description: str = ""
    radius: float = 10.0
    style: Style | None = None
    text_style: Style | None = None
    description_style: Style | None = None
    show: bool = True


class Cycle:
    """SmartArt component for circular and cyclical process diagrams (e.g. PDCA, life cycles)."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        style: Style,
        text_style: Style,
        description_style: Style | None = None,
        arrow_style: Style | None = None,
        clockwise: bool = True,
        start_angle: Angle = 90.0,
        node_shape: Literal["circle", "rectangle", "none"] = "circle",
        node_radius: PosFloat = 8.0,
        node_width: PosFloat = 18.0,
        node_height: PosFloat = 10.0,
        description_placement: Literal["inside", "outside"] = "inside",
        arrow_type: Literal["arc", "line", "none"] = "arc",
        arrow_width: PosFloat = 2.0,
        arrow_head_width: PosFloat = 4.5,
        arrow_color_mode: Literal["monochrome", "match_source", "match_target"] = "match_source",
        arrow_gap: PosFloat = 2.5,
        center_text: str = "",
        center_description: str = "",
        center_radius: PosFloat = 10.0,
        center_style: Style | None = None,
        center_text_style: Style | None = None,
        center_description_style: Style | None = None,
    ) -> None:
        """Initialize Cycle SmartArt.

        Args:
            style: Default style for the step nodes.
            text_style: Default style for primary step text (titles).
            description_style: Default style for secondary description text.
            arrow_style: Default style for connecting arrows.
            clockwise: Whether the process flows clockwise (True) or counter-clockwise (False).
                Defaults to True.
            start_angle: Angle in degrees for the first node (0 is right, 90 is top). Defaults to 90.0.
            node_shape: Shape of the step nodes ("circle", "rectangle", or "none"). Defaults to "circle".
            node_radius: Radius of nodes when node_shape is "circle". Defaults to 8.0.
            node_width: Width of nodes when node_shape is "rectangle". Defaults to 18.0.
            node_height: Height of nodes when node_shape is "rectangle". Defaults to 10.0.
            description_placement: Placement of description text ("inside" or "outside" node).
                Defaults to "inside".
            arrow_type: Connecting arrow style ("arc" for curved block arrow, "line" for arc line, "none").
                Defaults to "arc".
            arrow_width: Tail thickness of block arrow or line width of arc line arrow. Defaults to 2.0.
            arrow_head_width: Head width of block arrow. Defaults to 4.5.
            arrow_color_mode: Coloring mode for connecting arrows ("match_source", "match_target", "monochrome").
                Defaults to "match_source".
            arrow_gap: Distance margin between arrow endpoints and step nodes. Defaults to 2.5.
            center_text: Optional title text for a center node (creating a Radial Cycle).
            center_description: Optional supporting description text for the center node.
            center_radius: Radius of the center circle. Defaults to 10.0.
            center_style: Custom style for the center node circle.
            center_text_style: Custom style for the center node title.
            center_description_style: Custom style for the center node description text.
        """
        self._clockwise = bool(clockwise)
        self._start_angle = float(start_angle)
        self._node_shape = node_shape
        self._node_radius = float(node_radius)
        self._node_width = float(node_width)
        self._node_height = float(node_height)
        self._description_placement = description_placement
        self._arrow_type = arrow_type
        self._arrow_width = float(arrow_width)
        self._arrow_head_width = float(arrow_head_width)
        self._arrow_color_mode = arrow_color_mode
        self._arrow_gap = float(arrow_gap)
        self._style = style
        self._text_style = text_style
        self._description_style = description_style
        self._arrow_style = arrow_style

        resolved_center_text_style = center_text_style or text_style
        resolved_center_desc_style = center_description_style or description_style

        if bool(center_text.strip()):
            if center_style is None:
                raise ValueError("'center_style' was not provided for center node.")
            if resolved_center_text_style is None:
                raise ValueError("Neither 'center_text_style' nor 'text_style' was provided for center node.")
            if bool(center_description.strip()) and resolved_center_desc_style is None:
                raise ValueError(
                    "Neither 'center_description_style' nor 'description_style' "
                    "was provided for center node description."
                )

        self._center = CycleCenter(
            text=center_text,
            description=center_description,
            radius=float(center_radius),
            style=center_style,
            text_style=resolved_center_text_style,
            description_style=resolved_center_desc_style,
            show=True,
        )
        self._items: list[CycleItem] = []

    @property
    def items(self) -> list[CycleItem]:
        """Return the registered cycle items."""
        return self._items

    @property
    def center(self) -> CycleCenter:
        """Return the center node model."""
        return self._center

    @validate_call
    def add(  # noqa: PLR0913
        self,
        text: str,
        *,
        style: Style | None = None,
        description: str = "",
        text_style: Style | None = None,
        description_style: Style | None = None,
        arrow_style: Style | None = None,
        show: bool = True,
    ) -> CycleItem:
        """Add a step to the cycle.

        Args:
            text: Primary step title text.
            style: Style for this step node. If None, default style is used.
            description: Optional supporting description text.
            text_style: Custom Style for the title text. If None, default text_style is used.
            description_style: Custom Style for the description text. If None, default description_style is used.
            arrow_style: Custom Style for the arrow following this step.
            show: Whether to render this step node. Defaults to True.

        Returns:
            CycleItem: The created cycle item instance.
        """
        effective_style = style if style is not None else self._style
        effective_text_style = text_style if text_style is not None else self._text_style
        effective_description_style = description_style if description_style is not None else self._description_style
        effective_arrow_style = arrow_style if arrow_style is not None else self._arrow_style

        if bool(description.strip()) and effective_description_style is None:
            raise ValueError(
                "Neither default 'description_style' nor item 'description_style' was provided "
                f"for description of item '{text}'."
            )

        if (
            self._arrow_type != "none"
            and self._arrow_color_mode == "monochrome"
            and effective_arrow_style is None
        ):
            raise ValueError(
                f"Neither default 'arrow_style' nor item 'arrow_style' was provided for arrow after '{text}'."
            )

        item = CycleItem(
            text=text,
            style=effective_style,
            description=description,
            text_style=effective_text_style,
            description_style=effective_description_style,
            arrow_style=effective_arrow_style,
            show=show,
        )
        self._items.append(item)
        return item

    @validate_call
    def set_center(  # noqa: PLR0913
        self,
        text: str,
        *,
        style: Style | None = None,
        description: str = "",
        radius: PosFloat | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CycleCenter:
        """Configure the optional center node for a Radial Cycle.

        Args:
            text: Center node title text.
            style: Custom Style for the center circle. If None, retains current center_style.
            description: Optional supporting description for the center node.
            radius: Radius of the center circle. If None, retains current center_radius.
            text_style: Custom Style for the center title text.
            description_style: Custom Style for the center description text.
            show: Whether to render the center node. Defaults to True.

        Returns:
            CycleCenter: The center node configuration instance.
        """
        self._center.text = text
        self._center.description = description
        self._center.show = show
        if radius is not None:
            self._center.radius = float(radius)
        if style is not None:
            self._center.style = style
        elif self._center.style is None:
            raise ValueError("'style' is required when setting center node.")
        if text_style is not None:
            self._center.text_style = text_style
        if description_style is not None:
            self._center.description_style = description_style
        return self._center

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        radius: PosFloat = 35.0,
        align: Literal["center", "bottom_left"] = "center",
        scale: PosFloat = 1.0,
    ) -> None:
        """Draw the cycle diagram at the specified coordinate.

        Args:
            xy: Coordinate tuple (x, y) anchoring the diagram.
            radius: Orbit radius from diagram center to step nodes. Defaults to 35.0.
            align: Anchor alignment ("center" if xy is center, "bottom_left" if xy is bottom-left bounding corner).
                Defaults to "center".
            scale: Proportional scale factor around xy. Defaults to 1.0.
        """
        orbit_r = float(radius)
        num_items = len(self._items)

        # Resolve center coordinate
        if align == "center":
            cx, cy = float(xy[0]), float(xy[1])
        else:
            node_half_extent = (
                self._node_radius if self._node_shape == "circle" else max(self._node_width, self._node_height) / 2.0
            )
            extra_margin = 8.0 if self._description_placement == "outside" else 2.0
            offset = orbit_r + node_half_extent + extra_margin
            cx, cy = float(xy[0]) + offset, float(xy[1]) + offset

        with transform(origin=xy, scale=scale):
            if num_items == 0:
                if self._center.text and self._center.show:
                    self._draw_center_node(cx, cy)
                return

            angles = self._compute_item_angles(num_items)

            # 1. Draw connecting arrows if multiple items exist
            if num_items >= 2 and self._arrow_type != "none":
                self._draw_arrows(cx, cy, orbit_r, num_items, angles)

            # 2. Draw center node if specified
            if self._center.text and self._center.show:
                self._draw_center_node(cx, cy)

            # 3. Draw nodes and their texts
            for i, item in enumerate(self._items):
                if not item.show:
                    continue
                ang_rad = math.radians(angles[i])
                nx = cx + orbit_r * math.cos(ang_rad)
                ny = cy + orbit_r * math.sin(ang_rad)
                node_style = item.style

                # Render shape
                if self._node_shape == "circle":
                    canvas_circle(xy=(nx, ny), radius=self._node_radius, style=node_style)
                elif self._node_shape == "rectangle":
                    rect_style = node_style if node_style.shape_r is not None else node_style.patch(shape_r=2.0)
                    canvas_rectangle(
                        xy=(nx, ny),
                        width=self._node_width,
                        height=self._node_height,
                        style=rect_style,
                    )

                # Render texts
                self._draw_item_texts(item, node_style, nx, ny, ang_rad)

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
            node_half_extent = math.hypot(self._node_width, self._node_height) / 2.0
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
            if not (self._items[i].show and self._items[next_i].show):
                continue
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
                    arrow_head=arc_head,
                    angle_start=a_start,
                    angle_end=a_end,
                    style=arrow_style.patch(line_width=self._arrow_width),
                )

    def _resolve_arrow_style(self, from_idx: int, to_idx: int) -> Style:
        """Determine final Style for a connecting arrow."""
        item = self._items[from_idx]
        if item.arrow_style is not None:
            return item.arrow_style
        if self._arrow_style is not None:
            return self._arrow_style

        if self._arrow_color_mode == "match_source":
            color = item.style.shape_fill_color or (170, 170, 170, 0.9)
        elif self._arrow_color_mode == "match_target":
            color = self._items[to_idx].style.shape_fill_color or (170, 170, 170, 0.9)
        else:
            color = (170, 170, 170, 0.9)

        if self._arrow_type == "arc":
            return Style(
                shape_fill_color=color,
                shape_line_color=color,
                shape_line_width=0,
                shape_line_style="solid",
            )
        return Style(
            line_color=color,
            line_width=self._arrow_width,
            line_style="solid",
        )

    def _resolve_node_text_colors(
        self, node_style: Style
    ) -> tuple[ColorType, ColorType]:
        """Resolve default title and description colors based on node fill luminance."""
        if self._node_shape == "none":
            return (40, 40, 40, 1.0), (80, 80, 80, 1.0)
        fill_color = node_style.shape_fill_color
        fill_alpha = node_style.alpha
        title_color = ColorUtil.get_contrast_text_color(fill_color, fill_alpha)
        desc_color = ColorUtil.get_contrast_text_color(
            fill_color,
            fill_alpha,
            dark_color=(80, 80, 80, 1.0),
            light_color=(255, 255, 255, 0.92),
        )
        return title_color, desc_color

    def _draw_item_texts(
        self,
        item: CycleItem,
        node_style: Style,
        nx: float,
        ny: float,
        ang_rad: float,
    ) -> None:
        """Render primary title and optional description text for a step node."""
        has_desc = bool(item.description.strip())
        default_title_color, default_desc_color = self._resolve_node_text_colors(node_style)

        t_style = (
            item.text_style
            or self._text_style
            or Style(
                text_size=9.5 if self._node_shape != "rectangle" else 9.0,
                text_font=Font.SANSSERIF_BOLD,
                text_color=default_title_color,
                halign="center",
                valign="center",
            )
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
                title_y = ny + self._node_height * 0.20
                desc_y = ny - self._node_height * 0.25
                desc_size = 6.5
            else:
                title_y = ny + 2.0
                desc_y = ny - 2.5
                desc_size = 7.0

            d_style = (
                item.description_style
                or self._description_style
                or Style(
                    text_size=desc_size,
                    text_font=Font.SANSSERIF_REGULAR,
                    text_color=default_desc_color,
                    halign="center",
                    valign="center",
                )
            )
            canvas_text(xy=(nx, title_y), text=item.text, style=t_style)
            canvas_text(xy=(nx, desc_y), text=item.description, style=d_style)

        else:
            # Title inside node, description placed radially outward
            canvas_text(xy=(nx, ny), text=item.text, style=t_style)

            node_half_extent = (
                self._node_radius if self._node_shape == "circle" else max(self._node_width, self._node_height) / 2.0
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

            d_style = (
                item.description_style
                or self._description_style
                or Style(
                    text_size=8.0,
                    text_font=Font.SANSSERIF_REGULAR,
                    text_color=(70, 70, 70, 1.0),
                    halign=halign,
                    valign=valign,
                )
            )
            canvas_text(xy=(dx, dy), text=item.description, style=d_style)

    def _draw_center_node(self, cx: float, cy: float) -> None:
        """Render the center node for Radial Cycle diagrams."""
        center = self._center
        c_style = center.style or Style(
            shape_fill_color=(245, 247, 250, 1.0),
            shape_line_color=(185, 195, 210, 1.0),
            shape_line_width=1.5,
            shape_line_style="solid",
        )
        canvas_circle(xy=(cx, cy), radius=center.radius, style=c_style)

        fill_color = c_style.shape_fill_color
        fill_alpha = c_style.alpha
        def_center_title_col = ColorUtil.get_contrast_text_color(
            fill_color,
            fill_alpha,
            dark_color=(50, 60, 80, 1.0),
            light_color=(255, 255, 255, 1.0),
        )
        def_center_desc_col = ColorUtil.get_contrast_text_color(
            fill_color,
            fill_alpha,
            dark_color=(90, 100, 120, 1.0),
            light_color=(255, 255, 255, 0.92),
        )

        has_desc = bool(center.description.strip())
        t_style = center.text_style or Style(
            text_size=11.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=def_center_title_col,
            halign="center",
            valign="center",
        )

        if not has_desc:
            canvas_text(xy=(cx, cy), text=center.text, style=t_style)
        else:
            title_y = cy + center.radius * 0.22
            desc_y = cy - center.radius * 0.35
            d_style = center.description_style or Style(
                text_size=7.5,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=def_center_desc_col,
                halign="center",
                valign="center",
            )
            canvas_text(xy=(cx, title_y), text=center.text, style=t_style)
            canvas_text(xy=(cx, desc_y), text=center.description, style=d_style)
