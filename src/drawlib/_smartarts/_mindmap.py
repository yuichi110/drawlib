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

from typing import Literal

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeCoordinate,
    TypeFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import ellipse, get_charwidth_from_fontsize, line, rectangle
from drawlib._preset_styles import get_style


class MindMapNode:
    """Class for rendering smart art MindMap and hierarchy tree diagrams.

    Supports nodes with rectangle, oval, or text-only (none) shapes, connected with
    right-angled fork lines via automatically placed junctions, expanding in 4 directions
    (bottom, top, left, right).
    """

    @guarded
    def __init__(  # noqa: PLR0913
        self,
        text: TypeStr,
        branch: Literal["bottom", "top", "left", "right"] | None = None,
        shape: Literal["rectangle", "oval", "none"] | None = None,
        size: tuple[TypeFloat, TypeFloat] | None = None,
        style: TypeStr | Style | None = None,
        r: TypeFloat | None = None,
        textstyle: TypeStr | Style | None = None,
        linestyle: TypeStr | Style | None = None,
        horizontal_margin: TypeFloat | None = None,
        vertical_margin: TypeFloat | None = None,
        line_length: TypeFloat | None = None,
        xy_shift: tuple[TypeFloat, TypeFloat] | None = None,
        children: list[MindMapNode] | None = None,
        # Default options inherited by descendant nodes
        default_branch: Literal["bottom", "top", "left", "right"] | None = None,
        default_shape: Literal["rectangle", "oval", "none"] | None = None,
        default_size: tuple[TypeFloat, TypeFloat] | None = None,
        default_style: TypeStr | Style | None = None,
        default_r: TypeFloat | None = None,
        default_textstyle: TypeStr | Style | None = None,
        default_linestyle: TypeStr | Style | None = None,
        default_horizontal_margin: TypeFloat | None = None,
        default_vertical_margin: TypeFloat | None = None,
        default_line_length: TypeFloat | None = None,
        # Backward compatibility parameters
        boxsize: tuple[TypeFloat, TypeFloat] | None = None,
        boxstyle: TypeStr | Style | None = None,
        box_r: TypeFloat | None = None,
        box_horizontal_margin: TypeFloat | None = None,
        box_vertical_margin: TypeFloat | None = None,
        line_horizontal_length: TypeFloat | None = None,
        line_vertical_length: TypeFloat | None = None,
        default_boxsize: tuple[TypeFloat, TypeFloat] | None = None,
        default_boxstyle: TypeStr | Style | None = None,
        default_box_r: TypeFloat | None = None,
        default_box_horizontal_margin: TypeFloat | None = None,
        default_box_vertical_margin: TypeFloat | None = None,
        default_line_horizontal_length: TypeFloat | None = None,
        default_line_vertical_length: TypeFloat | None = None,
    ) -> None:
        """Initialize MindMapNode.

        Args:
            text: Text content displayed in this node.
            branch: Branch direction for child nodes ("bottom", "top", "left", "right").
            shape: Shape of this node ("rectangle", "oval", "none").
            size: Size of the node as (width, height).
            style: Shape style object or preset name.
            r: Corner radius when shape is "rectangle".
            textstyle: Style object or preset name for text.
            linestyle: Style object or preset name for connecting lines.
            horizontal_margin: Horizontal margin between sibling subtrees.
            vertical_margin: Vertical margin between sibling subtrees.
            line_length: Distance between parent and child hierarchy levels.
            xy_shift: Optional coordinate shift (dx, dy) to fine-tune this node's position.
            children: List of child MindMapNode instances.
            default_branch: Default branch direction for descendant nodes.
            default_shape: Default shape for descendant nodes.
            default_size: Default size for descendant nodes.
            default_style: Default style for descendant nodes.
            default_r: Default corner radius for descendant nodes.
            default_textstyle: Default text style for descendant nodes.
            default_linestyle: Default line style for descendant nodes.
            default_horizontal_margin: Default horizontal margin for descendant nodes.
            default_vertical_margin: Default vertical margin for descendant nodes.
            default_line_length: Default line length for descendant nodes.
            boxsize: Backward-compatible alias for size.
            boxstyle: Backward-compatible alias for style.
            box_r: Backward-compatible alias for r.
            box_horizontal_margin: Backward-compatible alias for horizontal_margin.
            box_vertical_margin: Backward-compatible alias for vertical_margin.
            line_horizontal_length: Backward-compatible alias for line_length.
            line_vertical_length: Backward-compatible alias for line_length.
            default_boxsize: Backward-compatible alias for default_size.
            default_boxstyle: Backward-compatible alias for default_style.
            default_box_r: Backward-compatible alias for default_r.
            default_box_horizontal_margin: Backward-compatible alias for default_horizontal_margin.
            default_box_vertical_margin: Backward-compatible alias for default_vertical_margin.
            default_line_horizontal_length: Backward-compatible alias for default_line_length.
            default_line_vertical_length: Backward-compatible alias for default_line_length.
        """
        self._text = text
        self._branch = branch
        self._shape = shape

        resolved_size = size if size is not None else boxsize
        self._size = resolved_size

        resolved_style = style if style is not None else boxstyle
        if isinstance(resolved_style, str):
            resolved_style = get_style(resolved_style)
        self._style = resolved_style

        self._r = r if r is not None else box_r

        if isinstance(textstyle, str):
            textstyle = get_style(textstyle)
        self._textstyle = textstyle

        if isinstance(linestyle, str):
            linestyle = get_style(linestyle)
        self._linestyle = linestyle

        self._horizontal_margin = horizontal_margin if horizontal_margin is not None else box_horizontal_margin
        self._vertical_margin = vertical_margin if vertical_margin is not None else box_vertical_margin

        resolved_line_len = line_length
        if resolved_line_len is None:
            resolved_line_len = line_vertical_length if line_vertical_length is not None else line_horizontal_length
        self._line_length = resolved_line_len

        self._xy_shift = xy_shift
        self._children: list[MindMapNode] = [] if children is None else children

        # Default options
        self._default_branch = default_branch
        self._default_shape = default_shape

        resolved_def_size = default_size if default_size is not None else default_boxsize
        self._default_size = resolved_def_size

        resolved_def_style = default_style if default_style is not None else default_boxstyle
        if isinstance(resolved_def_style, str):
            resolved_def_style = get_style(resolved_def_style)
        self._default_style = resolved_def_style

        self._default_r = default_r if default_r is not None else default_box_r

        if isinstance(default_textstyle, str):
            default_textstyle = get_style(default_textstyle)
        self._default_textstyle = default_textstyle

        if isinstance(default_linestyle, str):
            default_linestyle = get_style(default_linestyle)
        self._default_linestyle = default_linestyle

        self._default_horizontal_margin = (
            default_horizontal_margin if default_horizontal_margin is not None else default_box_horizontal_margin
        )
        self._default_vertical_margin = (
            default_vertical_margin if default_vertical_margin is not None else default_box_vertical_margin
        )

        resolved_def_line_len = default_line_length
        if resolved_def_line_len is None:
            resolved_def_line_len = (
                default_line_vertical_length
                if default_line_vertical_length is not None
                else default_line_horizontal_length
            )
        self._default_line_length = resolved_def_line_len

        # Backward compatibility internal attributes
        self._boxsize = self._size
        self._boxstyle = self._style
        self._box_r = self._r
        self._box_horizontal_margin = self._horizontal_margin
        self._box_vertical_margin = self._vertical_margin
        self._line_horizontal_length = (
            line_horizontal_length if line_horizontal_length is not None else self._line_length
        )
        self._line_vertical_length = (
            line_vertical_length if line_vertical_length is not None else self._line_length
        )
        self._default_boxsize = self._default_size
        self._default_boxstyle = self._default_style
        self._default_box_r = self._default_r
        self._default_box_horizontal_margin = self._default_horizontal_margin
        self._default_box_vertical_margin = self._default_vertical_margin
        self._default_line_horizontal_length = (
            default_line_horizontal_length
            if default_line_horizontal_length is not None
            else self._default_line_length
        )
        self._default_line_vertical_length = (
            default_line_vertical_length
            if default_line_vertical_length is not None
            else self._default_line_length
        )

        # Internal layout computation attributes
        self._resolved_w: float = 0.0
        self._resolved_h: float = 0.0
        self._extent_w: float = 0.0
        self._extent_h: float = 0.0

    @guarded
    def draw(
        self,
        xy: TypeCoordinate,
        branch: Literal["bottom", "top", "left", "right"] = "bottom",
        *,
        orientation: Literal["horizontal", "vertical"] | None = None,
        align: Literal["top", "bottom", "center", "left", "right"] | None = None,
    ) -> None:
        """Draw the mindmap tree rooted at this node.

        The given xy coordinate specifies the center point of this root node.

        Args:
            xy: Center coordinates (x, y) of the root node.
            branch: Default branch direction for child nodes ("bottom", "top", "left", "right").
            orientation: Backward-compatible argument. Maps "horizontal" -> "right", "vertical" -> "bottom".
            align: Backward-compatible argument for alignment.
        """
        root_branch = self._resolve_branch(self._branch or self._default_branch or branch, orientation)

        # Baseline defaults
        def_shape: Literal["rectangle", "oval", "none"] = self._default_shape or "rectangle"
        def_size = self._default_size or (20.0, 8.0)
        def_style = self._default_style or get_style("solid")
        def_r = 0.0 if self._default_r is None else self._default_r
        def_textstyle = self._default_textstyle
        def_linestyle = self._default_linestyle or get_style("solid")
        def_h_margin = 4.0 if self._default_horizontal_margin is None else self._default_horizontal_margin
        def_v_margin = 4.0 if self._default_vertical_margin is None else self._default_vertical_margin
        def_line_len = 10.0 if self._default_line_length is None else self._default_line_length

        # Pass 1: Measure subtree extents bottom-up
        self._measure_pass(
            current_branch=root_branch,
            default_shape=def_shape,
            default_size=def_size,
            default_style=def_style,
            default_textstyle=def_textstyle,
            default_h_margin=def_h_margin,
            default_v_margin=def_v_margin,
            default_line_len=def_line_len,
        )

        # Pass 2: Layout and draw top-down starting from root center xy
        root_cx, root_cy = xy
        if self._xy_shift is not None:
            root_cx += self._xy_shift[0]
            root_cy += self._xy_shift[1]
        self._layout_and_draw(
            center_xy=(root_cx, root_cy),
            current_branch=root_branch,
            default_shape=def_shape,
            default_size=def_size,
            default_style=def_style,
            default_r=def_r,
            default_textstyle=def_textstyle,
            default_linestyle=def_linestyle,
            default_h_margin=def_h_margin,
            default_v_margin=def_v_margin,
            default_line_len=def_line_len,
        )

    @staticmethod
    def _resolve_branch(
        branch: Literal["bottom", "top", "left", "right"],
        orientation: Literal["horizontal", "vertical"] | None,
    ) -> Literal["bottom", "top", "left", "right"]:
        if orientation == "horizontal":
            return "right"
        if orientation == "vertical":
            return "bottom"
        return branch

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
            b = child._branch or child._default_branch or current_branch
            groups[b].append(child)
        return groups

    def _measure_pass(  # noqa: PLR0913
        self,
        current_branch: Literal["bottom", "top", "left", "right"],
        default_shape: Literal["rectangle", "oval", "none"],
        default_size: tuple[float, float],
        default_style: Style,
        default_textstyle: Style | None,
        default_h_margin: float,
        default_v_margin: float,
        default_line_len: float,
    ) -> None:
        shape = self._shape or self._default_shape or default_shape
        size = self._size or self._default_size or default_size
        node_style = self._style or self._default_style or default_style
        text_style = self._textstyle or self._default_textstyle or default_textstyle or node_style

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

        h_margin = self._horizontal_margin or self._default_horizontal_margin or default_h_margin
        v_margin = self._vertical_margin or self._default_vertical_margin or default_v_margin
        line_len = self._line_length or self._default_line_length or default_line_len

        # Cascaded defaults for children
        new_def_shape = self._default_shape or default_shape
        new_def_size = self._default_size or default_size
        new_def_style = self._default_style or default_style
        new_def_textstyle = self._default_textstyle or default_textstyle
        new_def_h_margin = self._default_horizontal_margin or default_h_margin
        new_def_v_margin = self._default_vertical_margin or default_v_margin
        new_def_line_len = self._default_line_length or default_line_len

        child_groups = self._get_children_by_branch(current_branch)

        for b, group in child_groups.items():
            for child in group:
                child._measure_pass(
                    current_branch=b,
                    default_shape=new_def_shape,
                    default_size=new_def_size,
                    default_style=new_def_style,
                    default_textstyle=new_def_textstyle,
                    default_h_margin=new_def_h_margin,
                    default_v_margin=new_def_v_margin,
                    default_line_len=new_def_line_len,
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
        default_shape: Literal["rectangle", "oval", "none"],
        default_size: tuple[float, float],
        default_style: Style,
        default_r: float,
        default_textstyle: Style | None,
        default_linestyle: Style,
        default_h_margin: float,
        default_v_margin: float,
        default_line_len: float,
    ) -> None:
        cx, cy = center_xy

        shape = self._shape or self._default_shape or default_shape
        node_style = self._style or self._default_style or default_style
        r_val = self._r if self._r is not None else (self._default_r if self._default_r is not None else default_r)
        explicit_textstyle = self._textstyle or self._default_textstyle or default_textstyle
        text_style = explicit_textstyle or node_style
        if (
            shape != "none"
            and explicit_textstyle is None
            and node_style.fill_color is not None
            and node_style.fill_color == text_style.text_color
        ):
            text_style = get_style("white")
        line_style = self._linestyle or self._default_linestyle or default_linestyle

        h_margin = self._horizontal_margin or self._default_horizontal_margin or default_h_margin
        v_margin = self._vertical_margin or self._default_vertical_margin or default_v_margin
        line_len = self._line_length or self._default_line_length or default_line_len

        # Cascaded defaults for children
        new_def_shape = self._default_shape or default_shape
        new_def_size = self._default_size or default_size
        new_def_style = self._default_style or default_style
        new_def_r = self._default_r if self._default_r is not None else default_r
        new_def_textstyle = self._default_textstyle or default_textstyle
        new_def_linestyle = self._default_linestyle or default_linestyle
        new_def_h_margin = self._default_horizontal_margin or default_h_margin
        new_def_v_margin = self._default_vertical_margin or default_v_margin
        new_def_line_len = self._default_line_length or default_line_len

        bw, bh = self._resolved_w, self._resolved_h

        # 1. Draw node shape
        if shape == "rectangle":
            rectangle(
                xy=(cx, cy),
                width=bw,
                height=bh,
                r=r_val,
                style=node_style,
                text=self._text,
                textstyle=text_style,
            )
        elif shape == "oval":
            ellipse(
                xy=(cx, cy),
                width=bw,
                height=bh,
                style=node_style,
                text=self._text,
                textstyle=text_style,
            )
        else:  # shape == "none" (transparent box)
            transparent_style = node_style.copy()
            transparent_style.line_width = 0
            transparent_style.line_color = None
            transparent_style.fill_color = None
            transparent_style.fill_alpha = 0
            rectangle(
                xy=(cx, cy),
                width=bw,
                height=bh,
                style=transparent_style,
                text=self._text,
                textstyle=text_style,
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
                    new_def_shape=new_def_shape,
                    new_def_size=new_def_size,
                    new_def_style=new_def_style,
                    new_def_r=new_def_r,
                    new_def_textstyle=new_def_textstyle,
                    new_def_linestyle=new_def_linestyle,
                    new_def_h_margin=new_def_h_margin,
                    new_def_v_margin=new_def_v_margin,
                    new_def_line_len=new_def_line_len,
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
                    new_def_shape=new_def_shape,
                    new_def_size=new_def_size,
                    new_def_style=new_def_style,
                    new_def_r=new_def_r,
                    new_def_textstyle=new_def_textstyle,
                    new_def_linestyle=new_def_linestyle,
                    new_def_h_margin=new_def_h_margin,
                    new_def_v_margin=new_def_v_margin,
                    new_def_line_len=new_def_line_len,
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
                    new_def_shape=new_def_shape,
                    new_def_size=new_def_size,
                    new_def_style=new_def_style,
                    new_def_r=new_def_r,
                    new_def_textstyle=new_def_textstyle,
                    new_def_linestyle=new_def_linestyle,
                    new_def_h_margin=new_def_h_margin,
                    new_def_v_margin=new_def_v_margin,
                    new_def_line_len=new_def_line_len,
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
                    new_def_shape=new_def_shape,
                    new_def_size=new_def_size,
                    new_def_style=new_def_style,
                    new_def_r=new_def_r,
                    new_def_textstyle=new_def_textstyle,
                    new_def_linestyle=new_def_linestyle,
                    new_def_h_margin=new_def_h_margin,
                    new_def_v_margin=new_def_v_margin,
                    new_def_line_len=new_def_line_len,
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
        new_def_shape: Literal["rectangle", "oval", "none"],
        new_def_size: tuple[float, float],
        new_def_style: Style,
        new_def_r: float,
        new_def_textstyle: Style | None,
        new_def_linestyle: Style,
        new_def_h_margin: float,
        new_def_v_margin: float,
        new_def_line_len: float,
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

        if len(group) == 1:
            c, c_cx, c_cy = child_positions[0]
            child_top = (c_cx, c_cy + c._resolved_h / 2.0)
            if abs(c_cx - cx) < 1e-6:
                line(xy1=parent_pt, xy2=child_top, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
                line(xy1=(cx, junction_y), xy2=(c_cx, junction_y), style=line_style)
                line(xy1=(c_cx, junction_y), xy2=child_top, style=line_style)
        else:
            line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
            all_xs = [cx] + [pos[1] for pos in child_positions]
            line(xy1=(min(all_xs), junction_y), xy2=(max(all_xs), junction_y), style=line_style)
            for child, child_cx, child_cy in child_positions:
                line(xy1=(child_cx, junction_y), xy2=(child_cx, child_cy + child._resolved_h / 2.0), style=line_style)

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="bottom",
                default_shape=new_def_shape,
                default_size=new_def_size,
                default_style=new_def_style,
                default_r=new_def_r,
                default_textstyle=new_def_textstyle,
                default_linestyle=new_def_linestyle,
                default_h_margin=new_def_h_margin,
                default_v_margin=new_def_v_margin,
                default_line_len=new_def_line_len,
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
        new_def_shape: Literal["rectangle", "oval", "none"],
        new_def_size: tuple[float, float],
        new_def_style: Style,
        new_def_r: float,
        new_def_textstyle: Style | None,
        new_def_linestyle: Style,
        new_def_h_margin: float,
        new_def_v_margin: float,
        new_def_line_len: float,
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

        if len(group) == 1:
            c, c_cx, c_cy = child_positions[0]
            child_bottom = (c_cx, c_cy - c._resolved_h / 2.0)
            if abs(c_cx - cx) < 1e-6:
                line(xy1=parent_pt, xy2=child_bottom, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
                line(xy1=(cx, junction_y), xy2=(c_cx, junction_y), style=line_style)
                line(xy1=(c_cx, junction_y), xy2=child_bottom, style=line_style)
        else:
            line(xy1=parent_pt, xy2=(cx, junction_y), style=line_style)
            all_xs = [cx] + [pos[1] for pos in child_positions]
            line(xy1=(min(all_xs), junction_y), xy2=(max(all_xs), junction_y), style=line_style)
            for child, child_cx, child_cy in child_positions:
                line(xy1=(child_cx, junction_y), xy2=(child_cx, child_cy - child._resolved_h / 2.0), style=line_style)

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="top",
                default_shape=new_def_shape,
                default_size=new_def_size,
                default_style=new_def_style,
                default_r=new_def_r,
                default_textstyle=new_def_textstyle,
                default_linestyle=new_def_linestyle,
                default_h_margin=new_def_h_margin,
                default_v_margin=new_def_v_margin,
                default_line_len=new_def_line_len,
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
        new_def_shape: Literal["rectangle", "oval", "none"],
        new_def_size: tuple[float, float],
        new_def_style: Style,
        new_def_r: float,
        new_def_textstyle: Style | None,
        new_def_linestyle: Style,
        new_def_h_margin: float,
        new_def_v_margin: float,
        new_def_line_len: float,
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

        if len(group) == 1:
            c, c_cx, c_cy = child_positions[0]
            child_left = (c_cx - c._resolved_w / 2.0, c_cy)
            if abs(c_cy - cy) < 1e-6:
                line(xy1=parent_pt, xy2=child_left, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
                line(xy1=(junction_x, cy), xy2=(junction_x, c_cy), style=line_style)
                line(xy1=(junction_x, c_cy), xy2=child_left, style=line_style)
        else:
            line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
            all_ys = [cy] + [pos[2] for pos in child_positions]
            line(xy1=(junction_x, min(all_ys)), xy2=(junction_x, max(all_ys)), style=line_style)
            for child, child_cx, child_cy in child_positions:
                line(xy1=(junction_x, child_cy), xy2=(child_cx - child._resolved_w / 2.0, child_cy), style=line_style)

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="right",
                default_shape=new_def_shape,
                default_size=new_def_size,
                default_style=new_def_style,
                default_r=new_def_r,
                default_textstyle=new_def_textstyle,
                default_linestyle=new_def_linestyle,
                default_h_margin=new_def_h_margin,
                default_v_margin=new_def_v_margin,
                default_line_len=new_def_line_len,
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
        new_def_shape: Literal["rectangle", "oval", "none"],
        new_def_size: tuple[float, float],
        new_def_style: Style,
        new_def_r: float,
        new_def_textstyle: Style | None,
        new_def_linestyle: Style,
        new_def_h_margin: float,
        new_def_v_margin: float,
        new_def_line_len: float,
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

        if len(group) == 1:
            c, c_cx, c_cy = child_positions[0]
            child_right = (c_cx + c._resolved_w / 2.0, c_cy)
            if abs(c_cy - cy) < 1e-6:
                line(xy1=parent_pt, xy2=child_right, style=line_style)
            else:
                line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
                line(xy1=(junction_x, cy), xy2=(junction_x, c_cy), style=line_style)
                line(xy1=(junction_x, c_cy), xy2=child_right, style=line_style)
        else:
            line(xy1=parent_pt, xy2=(junction_x, cy), style=line_style)
            all_ys = [cy] + [pos[2] for pos in child_positions]
            line(xy1=(junction_x, min(all_ys)), xy2=(junction_x, max(all_ys)), style=line_style)
            for child, child_cx, child_cy in child_positions:
                line(xy1=(junction_x, child_cy), xy2=(child_cx + child._resolved_w / 2.0, child_cy), style=line_style)

        for child, child_cx, child_cy in child_positions:
            child._layout_and_draw(
                center_xy=(child_cx, child_cy),
                current_branch="left",
                default_shape=new_def_shape,
                default_size=new_def_size,
                default_style=new_def_style,
                default_r=new_def_r,
                default_textstyle=new_def_textstyle,
                default_linestyle=new_def_linestyle,
                default_h_margin=new_def_h_margin,
                default_v_margin=new_def_v_margin,
                default_line_len=new_def_line_len,
            )
