# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""MindMap implementation module."""

from __future__ import annotations

from typing import Literal, Self

from pydantic import validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import ellipse, get_charwidth_from_fontsize, line, rectangle, transform


class MindMapNode:
    """Class for rendering smart art MindMap and hierarchy tree diagrams.

    Supports nodes with rectangle, oval, or text-only (none) shapes, connected with
    right-angled fork lines via automatically placed junctions, expanding in 4 directions
    (bottom, top, left, right).
    """

    def __init__(  # noqa: PLR0913
        self,
        text: str,
        *,
        branch: Literal["bottom", "top", "left", "right"] | None = None,
        shape: Literal["rectangle", "oval", "none"] | None = None,
        size: tuple[PosFloat, PosFloat] | None = None,
        style: Style | None = None,
        text_style: Style | None = None,
        line_style: Style | None = None,
        horizontal_margin: PosFloat | None = None,
        vertical_margin: PosFloat | None = None,
        line_length: PosFloat | None = None,
        xy_shift: Coordinate | None = None,
        children: list[MindMapNode] | None = None,
        show: bool = True,
    ) -> None:
        """Initialize MindMapNode.

        Args:
            text: Text content displayed in this node.
            branch: Branch direction for child nodes ("bottom", "top", "left", "right").
            shape: Shape of this node ("rectangle", "oval", "none").
            size: Size of the node as (width, height).
            style: Shape style object.
            text_style: Style object for text.
            line_style: Style object for connecting lines.
            horizontal_margin: Horizontal margin between sibling subtrees.
            vertical_margin: Vertical margin between sibling subtrees.
            line_length: Distance between parent and child hierarchy levels.
            xy_shift: Optional coordinate shift (dx, dy) to fine-tune this node's position.
            children: List of child MindMapNode instances.
            show: Whether to render this mindmap node. Defaults to True.
        """
        self._text = text
        self._branch = branch
        self._shape = shape
        self._size = size
        self._style = style
        self._text_style = text_style
        self._line_style = line_style
        self._horizontal_margin = horizontal_margin
        self._vertical_margin = vertical_margin
        self._line_length = line_length
        self._xy_shift = xy_shift
        self._children: list[MindMapNode] = [] if children is None else children
        self.show: bool = show

        # Internal layout computation attributes
        self._resolved_w: float = 0.0
        self._resolved_h: float = 0.0
        self._extent_w: float = 0.0
        self._extent_h: float = 0.0

    @property
    def text(self) -> str:
        """Return or set the node text."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def branch(self) -> Literal["bottom", "top", "left", "right"] | None:
        """Return or set the node branch direction."""
        return self._branch

    @branch.setter
    def branch(self, value: Literal["bottom", "top", "left", "right"] | None) -> None:
        self._branch = value

    @property
    def shape(self) -> Literal["rectangle", "oval", "none"] | None:
        """Return or set the node shape."""
        return self._shape

    @shape.setter
    def shape(self, value: Literal["rectangle", "oval", "none"] | None) -> None:
        self._shape = value

    @property
    def size(self) -> tuple[PosFloat, PosFloat] | None:
        """Return or set the node size."""
        return self._size

    @size.setter
    def size(self, value: tuple[PosFloat, PosFloat] | None) -> None:
        self._size = value

    @property
    def style(self) -> Style | None:
        """Return or set the node style."""
        return self._style

    @style.setter
    def style(self, value: Style | None) -> None:
        self._style = value

    @property
    def text_style(self) -> Style | None:
        """Return or set the node text style."""
        return self._text_style

    @text_style.setter
    def text_style(self, value: Style | None) -> None:
        self._text_style = value

    @property
    def line_style(self) -> Style | None:
        """Return or set the node connector line style."""
        return self._line_style

    @line_style.setter
    def line_style(self, value: Style | None) -> None:
        self._line_style = value

    @property
    def children(self) -> list[MindMapNode]:
        """Return the child nodes."""
        return self._children

    @validate_call
    def add(  # noqa: PLR0913
        self,
        text: str,
        *,
        branch: Literal["bottom", "top", "left", "right"] | None = None,
        shape: Literal["rectangle", "oval", "none"] | None = None,
        size: tuple[PosFloat, PosFloat] | None = None,
        style: Style | None = None,
        text_style: Style | None = None,
        line_style: Style | None = None,
        horizontal_margin: PosFloat | None = None,
        vertical_margin: PosFloat | None = None,
        line_length: PosFloat | None = None,
        xy_shift: Coordinate | None = None,
        show: bool = True,
    ) -> Self:
        """Create and append a child MindMapNode, returning the created child.

        Args:
            text: Text content displayed in the child node.
            branch: Branch direction for the child node ("bottom", "top", "left", "right").
            shape: Shape of the child node ("rectangle", "oval", "none").
            size: Size of the child node as (width, height).
            style: Shape style object for the child node.
            text_style: Style object for child text.
            line_style: Style object for connecting lines.
            horizontal_margin: Horizontal margin between sibling subtrees.
            vertical_margin: Vertical margin between sibling subtrees.
            line_length: Distance between parent and child hierarchy levels.
            xy_shift: Optional coordinate shift (dx, dy) to fine-tune the child node's position.
            show: Whether to render the child node. Defaults to True.

        Returns:
            MindMapNode: The newly created child MindMapNode instance.
        """
        child = type(self)(
            text=text,
            branch=branch,
            shape=shape,
            size=size,
            style=style,
            text_style=text_style,
            line_style=line_style,
            horizontal_margin=horizontal_margin,
            vertical_margin=vertical_margin,
            line_length=line_length,
            xy_shift=xy_shift,
            show=show,
        )
        self._children.append(child)
        return child

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        branch: Literal["bottom", "top", "left", "right"] = "bottom",
        scale: PosFloat = 1.0,
    ) -> None:
        """Draw the mindmap tree rooted at this node.

        The given xy coordinate specifies the center point of this root node.

        Args:
            xy: Center coordinates (x, y) of the root node.
            branch: Default branch direction for child nodes ("bottom", "top", "left", "right").
            scale: Proportional scale factor around xy. Defaults to 1.0.

        Raises:
            ValueError: If root node is missing mandatory style, text_style, or line_style.
        """
        if self._style is None:
            raise ValueError('Root of MindMapNode must be initialized with "style".')
        if self._text_style is None:
            raise ValueError('Root of MindMapNode must be initialized with "text_style".')
        if self._line_style is None:
            raise ValueError('Root of MindMapNode must be initialized with "line_style".')

        root_branch = self._branch if self._branch is not None else branch

        # Baseline defaults for root if not explicitly provided
        root_shape = self._shape if self._shape is not None else "rectangle"
        root_size = self._size if self._size is not None else (20.0, 8.0)
        root_h_margin = self._horizontal_margin if self._horizontal_margin is not None else 4.0
        root_v_margin = self._vertical_margin if self._vertical_margin is not None else 4.0
        root_line_len = self._line_length if self._line_length is not None else 10.0

        # Pass 1: Measure subtree extents bottom-up
        self._measure_pass(
            current_branch=root_branch,
            parent_shape=root_shape,
            parent_size=root_size,
            parent_style=self._style,
            parent_text_style=self._text_style,
            parent_h_margin=root_h_margin,
            parent_v_margin=root_v_margin,
            parent_line_len=root_line_len,
        )

        # Pass 2: Layout and draw top-down starting from root center xy
        root_cx, root_cy = xy
        if self._xy_shift is not None:
            root_cx += self._xy_shift[0]
            root_cy += self._xy_shift[1]
        with transform(origin=xy, scale=scale):
            self._layout_and_draw(
                center_xy=(root_cx, root_cy),
                current_branch=root_branch,
                parent_shape=root_shape,
                parent_size=root_size,
                parent_style=self._style,
                parent_text_style=self._text_style,
                parent_line_style=self._line_style,
                parent_h_margin=root_h_margin,
                parent_v_margin=root_v_margin,
                parent_line_len=root_line_len,
            )

    def _get_children_by_branch(
        self,
        current_branch: Literal["bottom", "top", "left", "right"],
    ) -> dict[Literal["bottom", "top", "left", "right"], list[MindMapNode]]:
        groups: dict[Literal["bottom", "top", "left", "right"], list[MindMapNode]] = {
            "bottom": [],
            "top": [],
            "left": [],
            "right": [],
        }
        for child in self._children:
            b = child._branch if child._branch is not None else current_branch
            groups[b].append(child)
        return groups

    def _measure_pass(  # noqa: PLR0913
        self,
        current_branch: Literal["bottom", "top", "left", "right"],
        parent_shape: Literal["rectangle", "oval", "none"],
        parent_size: tuple[float, float],
        parent_style: Style,
        parent_text_style: Style,
        parent_h_margin: float,
        parent_v_margin: float,
        parent_line_len: float,
    ) -> None:
        shape = self._shape if self._shape is not None else parent_shape
        size = self._size if self._size is not None else parent_size
        node_style = self._style if self._style is not None else parent_style
        text_style = self._text_style if self._text_style is not None else parent_text_style

        if shape == "none":
            # Auto-calculate bounding box with padding using canvas-scaled character width
            font_size = float(text_style.text_size or 16.0)
            cw = get_charwidth_from_fontsize(font_size)
            text_w = sum(cw if ord(ch) > 127 else cw * 0.52 for ch in self._text)
            auto_w = max(text_w + cw * 1.6, cw * 2.5)
            auto_h = max(cw * 1.8, 6.0)
            w = float(size[0]) if self._size is not None else auto_w
            h = float(size[1]) if self._size is not None else auto_h
        else:
            w = float(size[0])
            h = float(size[1])

        self._resolved_w = w
        self._resolved_h = h

        h_margin = self._horizontal_margin if self._horizontal_margin is not None else parent_h_margin
        v_margin = self._vertical_margin if self._vertical_margin is not None else parent_v_margin
        line_len = self._line_length if self._line_length is not None else parent_line_len

        child_groups = self._get_children_by_branch(current_branch)

        for b, group in child_groups.items():
            for child in group:
                child._measure_pass(
                    current_branch=b,
                    parent_shape=shape,
                    parent_size=size,
                    parent_style=node_style,
                    parent_text_style=text_style,
                    parent_h_margin=h_margin,
                    parent_v_margin=v_margin,
                    parent_line_len=line_len,
                )

        # Compute subtree extents along the direction
        extent_w = self._resolved_w
        extent_h = self._resolved_h

        # Consider bottom / top children
        for b in ("bottom", "top"):
            group = child_groups[b]
            if group:
                total_w = sum(c._extent_w for c in group) + (len(group) - 1) * h_margin
                extent_w = max(extent_w, total_w)
                extent_h += line_len + max(c._extent_h for c in group)

        # Consider left / right children
        for b in ("left", "right"):
            group = child_groups[b]
            if group:
                total_h = sum(c._extent_h for c in group) + (len(group) - 1) * v_margin
                extent_h = max(extent_h, total_h)
                extent_w += line_len + max(c._extent_w for c in group)

        self._extent_w = extent_w
        self._extent_h = extent_h

    def _layout_and_draw(  # noqa: C901, PLR0913
        self,
        center_xy: tuple[float, float],
        current_branch: Literal["bottom", "top", "left", "right"],
        parent_shape: Literal["rectangle", "oval", "none"],
        parent_size: tuple[float, float],
        parent_style: Style,
        parent_text_style: Style,
        parent_line_style: Style,
        parent_h_margin: float,
        parent_v_margin: float,
        parent_line_len: float,
    ) -> None:
        cx, cy = center_xy

        shape = self._shape if self._shape is not None else parent_shape
        size = self._size if self._size is not None else parent_size
        node_style = self._style if self._style is not None else parent_style
        base_text_style = self._text_style if self._text_style is not None else parent_text_style
        line_style = self._line_style if self._line_style is not None else parent_line_style

        text_style = base_text_style
        # Smart contrast adjustment
        if shape != "none":
            if (
                node_style.shape_fill_color is not None
                and text_style.text_color is not None
                and node_style.shape_fill_color == text_style.text_color
            ):
                text_style = text_style.patch(text_color=(255, 255, 255))
        # For shape="none", if text is white (inherited from a solid root),
        # fall back to node_style / line_style text color so text is visible on canvas
        elif text_style.text_color in {(255, 255, 255), (255, 255, 255, 1.0)}:
            if node_style.text_color and node_style.text_color not in {(255, 255, 255), (255, 255, 255, 1.0)}:
                text_style = text_style.patch(text_color=node_style.text_color)
            elif line_style.line_color and line_style.line_color not in {(255, 255, 255), (255, 255, 255, 1.0)}:
                text_style = text_style.patch(text_color=line_style.line_color)

        h_margin = self._horizontal_margin if self._horizontal_margin is not None else parent_h_margin
        v_margin = self._vertical_margin if self._vertical_margin is not None else parent_v_margin
        line_len = self._line_length if self._line_length is not None else parent_line_len

        bw, bh = self._resolved_w, self._resolved_h

        # 1. Draw node shape
        if self.show:
            if shape == "rectangle":
                rectangle(
                    xy=(cx, cy),
                    width=bw,
                    height=bh,
                    style=node_style,
                    text=self._text,
                    text_style=text_style,
                )
            elif shape == "oval":
                ellipse(
                    xy=(cx, cy),
                    width=bw,
                    height=bh,
                    style=node_style,
                    text=self._text,
                    text_style=text_style,
                )
            else:  # shape == "none" (transparent box)
                transparent_style = node_style.patch(
                    shape_line_width=0,
                    shape_line_color=(0, 0, 0, 0.0),
                    shape_fill_color=(0, 0, 0, 0.0),
                    alpha=0.0,
                )
                rectangle(
                    xy=(cx, cy),
                    width=bw,
                    height=bh,
                    style=transparent_style,
                    text=self._text,
                    text_style=text_style,
                )

        if not self._children:
            return

        child_groups = self._get_children_by_branch(current_branch)

        # 2. Layout and connect children in each branch direction
        for b, group in child_groups.items():
            if not group:
                continue

            if b == "bottom":
                self._connect_and_layout_bottom(
                    cx=cx,
                    cy=cy,
                    bh=bh,
                    group=group,
                    line_len=line_len,
                    h_margin=h_margin,
                    line_style=line_style,
                    parent_shape=shape,
                    parent_size=size,
                    parent_style=node_style,
                    parent_text_style=base_text_style,
                    parent_line_style=line_style,
                    parent_h_margin=h_margin,
                    parent_v_margin=v_margin,
                    parent_line_len=line_len,
                    parent_show=self.show,
                )
            elif b == "top":
                self._connect_and_layout_top(
                    cx=cx,
                    cy=cy,
                    bh=bh,
                    group=group,
                    line_len=line_len,
                    h_margin=h_margin,
                    line_style=line_style,
                    parent_shape=shape,
                    parent_size=size,
                    parent_style=node_style,
                    parent_text_style=base_text_style,
                    parent_line_style=line_style,
                    parent_h_margin=h_margin,
                    parent_v_margin=v_margin,
                    parent_line_len=line_len,
                    parent_show=self.show,
                )
            elif b == "right":
                self._connect_and_layout_right(
                    cx=cx,
                    cy=cy,
                    bw=bw,
                    group=group,
                    line_len=line_len,
                    v_margin=v_margin,
                    line_style=line_style,
                    parent_shape=shape,
                    parent_size=size,
                    parent_style=node_style,
                    parent_text_style=base_text_style,
                    parent_line_style=line_style,
                    parent_h_margin=h_margin,
                    parent_v_margin=v_margin,
                    parent_line_len=line_len,
                    parent_show=self.show,
                )
            else:  # "left"
                self._connect_and_layout_left(
                    cx=cx,
                    cy=cy,
                    bw=bw,
                    group=group,
                    line_len=line_len,
                    v_margin=v_margin,
                    line_style=line_style,
                    parent_shape=shape,
                    parent_size=size,
                    parent_style=node_style,
                    parent_text_style=base_text_style,
                    parent_line_style=line_style,
                    parent_h_margin=h_margin,
                    parent_v_margin=v_margin,
                    parent_line_len=line_len,
                    parent_show=self.show,
                )

    @staticmethod
    def _connect_and_layout_bottom(  # noqa: PLR0913
        cx: float,
        cy: float,
        bh: float,
        group: list[MindMapNode],
        line_len: float,
        h_margin: float,
        line_style: Style,
        parent_shape: Literal["rectangle", "oval", "none"],
        parent_size: tuple[float, float],
        parent_style: Style,
        parent_text_style: Style,
        parent_line_style: Style,
        parent_h_margin: float,
        parent_v_margin: float,
        parent_line_len: float,
        parent_show: bool = True,
    ) -> None:
        parent_pt = (cx, cy - bh / 2.0)
        junction_y = cy - bh / 2.0 - line_len / 2.0

        total_w = sum(c._extent_w for c in group) + (len(group) - 1) * h_margin
        cur_x = cx - total_w / 2.0

        child_positions: list[tuple[MindMapNode, float, float]] = []
        for child in group:
            child_cx = cur_x + child._extent_w / 2.0
            child_cy = cy - bh / 2.0 - line_len - child._resolved_h / 2.0
            if child._xy_shift is not None:
                child_cx += child._xy_shift[0]
                child_cy += child._xy_shift[1]
            child_positions.append((child, child_cx, child_cy))
            cur_x += child._extent_w + h_margin

        visible_positions = [(c, c_cx, c_cy) for (c, c_cx, c_cy) in child_positions if c.show]
        if parent_show and visible_positions:
            if len(group) == 1 and len(visible_positions) == 1:
                c, c_cx, c_cy = visible_positions[0]
                child_top = (c_cx, c_cy + c._resolved_h / 2.0)
                if abs(c_cx - cx) < 1e-6:
                    line(xy1=parent_pt, xy2=child_top, style=line_style)
                else:
                    line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
                    line(xy1=(cx, junction_y), xy2=(c_cx, junction_y), style=line_style)
                    line(xy1=(c_cx, junction_y), xy2=child_top, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
                all_xs = [cx] + [pos[1] for pos in visible_positions]
                line(xy1=(min(all_xs), junction_y), xy2=(max(all_xs), junction_y), style=line_style)
                for child, child_cx, child_cy in visible_positions:
                    line(
                        xy1=(child_cx, junction_y),
                        xy2=(child_cx, child_cy + child._resolved_h / 2.0),
                        style=line_style,
                    )

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="bottom",
                parent_shape=parent_shape,
                parent_size=parent_size,
                parent_style=parent_style,
                parent_text_style=parent_text_style,
                parent_line_style=parent_line_style,
                parent_h_margin=parent_h_margin,
                parent_v_margin=parent_v_margin,
                parent_line_len=parent_line_len,
            )

    @staticmethod
    def _connect_and_layout_top(  # noqa: PLR0913
        cx: float,
        cy: float,
        bh: float,
        group: list[MindMapNode],
        line_len: float,
        h_margin: float,
        line_style: Style,
        parent_shape: Literal["rectangle", "oval", "none"],
        parent_size: tuple[float, float],
        parent_style: Style,
        parent_text_style: Style,
        parent_line_style: Style,
        parent_h_margin: float,
        parent_v_margin: float,
        parent_line_len: float,
        parent_show: bool = True,
    ) -> None:
        parent_pt = (cx, cy + bh / 2.0)
        junction_y = cy + bh / 2.0 + line_len / 2.0

        total_w = sum(c._extent_w for c in group) + (len(group) - 1) * h_margin
        cur_x = cx - total_w / 2.0

        child_positions: list[tuple[MindMapNode, float, float]] = []
        for child in group:
            child_cx = cur_x + child._extent_w / 2.0
            child_cy = cy + bh / 2.0 + line_len + child._resolved_h / 2.0
            if child._xy_shift is not None:
                child_cx += child._xy_shift[0]
                child_cy += child._xy_shift[1]
            child_positions.append((child, child_cx, child_cy))
            cur_x += child._extent_w + h_margin

        visible_positions = [(c, c_cx, c_cy) for (c, c_cx, c_cy) in child_positions if c.show]
        if parent_show and visible_positions:
            if len(group) == 1 and len(visible_positions) == 1:
                c, c_cx, c_cy = visible_positions[0]
                child_bottom = (c_cx, c_cy - c._resolved_h / 2.0)
                if abs(c_cx - cx) < 1e-6:
                    line(xy1=parent_pt, xy2=child_bottom, style=line_style)
                else:
                    line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
                    line(xy1=(cx, junction_y), xy2=(c_cx, junction_y), style=line_style)
                    line(xy1=(c_cx, junction_y), xy2=child_bottom, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
                all_xs = [cx] + [pos[1] for pos in visible_positions]
                line(xy1=(min(all_xs), junction_y), xy2=(max(all_xs), junction_y), style=line_style)
                for child, child_cx, child_cy in visible_positions:
                    line(
                        xy1=(child_cx, junction_y),
                        xy2=(child_cx, child_cy - child._resolved_h / 2.0),
                        style=line_style,
                    )

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="top",
                parent_shape=parent_shape,
                parent_size=parent_size,
                parent_style=parent_style,
                parent_text_style=parent_text_style,
                parent_line_style=parent_line_style,
                parent_h_margin=parent_h_margin,
                parent_v_margin=parent_v_margin,
                parent_line_len=parent_line_len,
            )

    @staticmethod
    def _connect_and_layout_right(  # noqa: PLR0913
        cx: float,
        cy: float,
        bw: float,
        group: list[MindMapNode],
        line_len: float,
        v_margin: float,
        line_style: Style,
        parent_shape: Literal["rectangle", "oval", "none"],
        parent_size: tuple[float, float],
        parent_style: Style,
        parent_text_style: Style,
        parent_line_style: Style,
        parent_h_margin: float,
        parent_v_margin: float,
        parent_line_len: float,
        parent_show: bool = True,
    ) -> None:
        parent_pt = (cx + bw / 2.0, cy)
        junction_x = cx + bw / 2.0 + line_len / 2.0

        total_h = sum(c._extent_h for c in group) + (len(group) - 1) * v_margin
        cur_y = cy + total_h / 2.0

        child_positions: list[tuple[MindMapNode, float, float]] = []
        for child in group:
            child_cy = cur_y - child._extent_h / 2.0
            child_cx = cx + bw / 2.0 + line_len + child._resolved_w / 2.0
            if child._xy_shift is not None:
                child_cx += child._xy_shift[0]
                child_cy += child._xy_shift[1]
            child_positions.append((child, child_cx, child_cy))
            cur_y -= child._extent_h + v_margin

        visible_positions = [(c, c_cx, c_cy) for (c, c_cx, c_cy) in child_positions if c.show]
        if parent_show and visible_positions:
            if len(group) == 1 and len(visible_positions) == 1:
                c, c_cx, c_cy = visible_positions[0]
                child_left = (c_cx - c._resolved_w / 2.0, c_cy)
                if abs(c_cy - cy) < 1e-6:
                    line(xy1=parent_pt, xy2=child_left, style=line_style)
                else:
                    line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
                    line(xy1=(junction_x, cy), xy2=(junction_x, c_cy), style=line_style)
                    line(xy1=(junction_x, c_cy), xy2=child_left, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
                all_ys = [cy] + [pos[2] for pos in visible_positions]
                line(xy1=(junction_x, min(all_ys)), xy2=(junction_x, max(all_ys)), style=line_style)
                for child, child_cx, child_cy in visible_positions:
                    line(
                        xy1=(junction_x, child_cy),
                        xy2=(child_cx - child._resolved_w / 2.0, child_cy),
                        style=line_style,
                    )

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="right",
                parent_shape=parent_shape,
                parent_size=parent_size,
                parent_style=parent_style,
                parent_text_style=parent_text_style,
                parent_line_style=parent_line_style,
                parent_h_margin=parent_h_margin,
                parent_v_margin=parent_v_margin,
                parent_line_len=parent_line_len,
            )

    @staticmethod
    def _connect_and_layout_left(  # noqa: PLR0913
        cx: float,
        cy: float,
        bw: float,
        group: list[MindMapNode],
        line_len: float,
        v_margin: float,
        line_style: Style,
        parent_shape: Literal["rectangle", "oval", "none"],
        parent_size: tuple[float, float],
        parent_style: Style,
        parent_text_style: Style,
        parent_line_style: Style,
        parent_h_margin: float,
        parent_v_margin: float,
        parent_line_len: float,
        parent_show: bool = True,
    ) -> None:
        parent_pt = (cx - bw / 2.0, cy)
        junction_x = cx - bw / 2.0 - line_len / 2.0

        total_h = sum(c._extent_h for c in group) + (len(group) - 1) * v_margin
        cur_y = cy + total_h / 2.0

        child_positions: list[tuple[MindMapNode, float, float]] = []
        for child in group:
            child_cy = cur_y - child._extent_h / 2.0
            child_cx = cx - bw / 2.0 - line_len - child._resolved_w / 2.0
            if child._xy_shift is not None:
                child_cx += child._xy_shift[0]
                child_cy += child._xy_shift[1]
            child_positions.append((child, child_cx, child_cy))
            cur_y -= child._extent_h + v_margin

        visible_positions = [(c, c_cx, c_cy) for (c, c_cx, c_cy) in child_positions if c.show]
        if parent_show and visible_positions:
            if len(group) == 1 and len(visible_positions) == 1:
                c, c_cx, c_cy = visible_positions[0]
                child_right = (c_cx + c._resolved_w / 2.0, c_cy)
                if abs(c_cy - cy) < 1e-6:
                    line(xy1=parent_pt, xy2=child_right, style=line_style)
                else:
                    line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
                    line(xy1=(junction_x, cy), xy2=(junction_x, c_cy), style=line_style)
                    line(xy1=(junction_x, c_cy), xy2=child_right, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
                all_ys = [cy] + [pos[2] for pos in visible_positions]
                line(xy1=(junction_x, min(all_ys)), xy2=(junction_x, max(all_ys)), style=line_style)
                for child, child_cx, child_cy in visible_positions:
                    line(
                        xy1=(junction_x, child_cy),
                        xy2=(child_cx + child._resolved_w / 2.0, child_cy),
                        style=line_style,
                    )

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="left",
                parent_shape=parent_shape,
                parent_size=parent_size,
                parent_style=parent_style,
                parent_text_style=parent_text_style,
                parent_line_style=parent_line_style,
                parent_h_margin=parent_h_margin,
                parent_v_margin=parent_v_margin,
                parent_line_len=parent_line_len,
            )
