# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Tree implementation module."""

from __future__ import annotations

from typing import Callable, Literal, Self

from pydantic import BaseModel, validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line, text, transform


class _TreeNodeDrawingItem(BaseModel):
    """Represents a drawing item for a tree node."""

    location: Literal["before", "after"]
    padding_width: PosFloat
    function: Callable
    style: Style
    args: dict


class TreeNode:
    """Class for rendering smart art trees.

    This class provides methods to create and manipulate tree-like smart art
    diagrams, supporting custom text styles, line styles, and margins for
    horizontal and vertical lines.
    """

    _drawing_item_map: dict[str, _TreeNodeDrawingItem] = {}

    def __init__(  # noqa: PLR0913
        self,
        text: str,
        *,
        text_style: Style | None = None,
        line_style: Style | None = None,
        line_horizontal_margin: PosFloat | None = None,
        line_horizontal_length: PosFloat | None = None,
        line_vertical_margin: PosFloat | None = None,
        children: list[TreeNode] | None = None,
        show: bool = True,
    ) -> None:
        """Initializes a TreeNode instance with specific text, styles, and optional children.

        Args:
            text: The text content for the tree node.
            text_style: The text style for the node. Inherited by child nodes if not overridden.
            line_style: The line style for connecting lines. Inherited by child nodes if not overridden.
            line_horizontal_margin: Horizontal margin between node and connector line. Inherited if not overridden.
            line_horizontal_length: Length of horizontal connector line. Inherited if not overridden.
            line_vertical_margin: Vertical margin between child nodes. Inherited if not overridden.
            children: A list of child nodes connected to this node. Defaults to None.
            show: Whether to render this tree node. Defaults to True.
        """
        self._text = text
        self._text_style = text_style
        self._line_style = line_style
        self._line_horizontal_margin = line_horizontal_margin
        self._line_horizontal_length = line_horizontal_length
        self._line_vertical_margin = line_vertical_margin
        self._children: list[TreeNode] = children if children is not None else []
        self._drawing_item_name: str | None = None
        self.show: bool = show

    @property
    def text(self) -> str:
        """Return or set the node text."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

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
    def children(self) -> list[TreeNode]:
        """Return the child nodes."""
        return self._children

    @validate_call
    def add(  # noqa: PLR0913
        self,
        text: str,
        *,
        text_style: Style | None = None,
        line_style: Style | None = None,
        line_horizontal_margin: PosFloat | None = None,
        line_horizontal_length: PosFloat | None = None,
        line_vertical_margin: PosFloat | None = None,
        show: bool = True,
    ) -> Self:
        """Create and append a child TreeNode, returning the created child.

        Args:
            text: The text content for the child tree node.
            text_style: The text style for the child node. Inherited if None.
            line_style: The line style for connecting lines. Inherited if None.
            line_horizontal_margin: Horizontal margin between node and connector line. Inherited if None.
            line_horizontal_length: Length of horizontal connector line. Inherited if None.
            line_vertical_margin: Vertical margin between child nodes. Inherited if None.
            show: Whether to render the child node. Defaults to True.

        Returns:
            TreeNode: The newly created child TreeNode instance.
        """
        child = type(self)(
            text=text,
            text_style=text_style,
            line_style=line_style,
            line_horizontal_margin=line_horizontal_margin,
            line_horizontal_length=line_horizontal_length,
            line_vertical_margin=line_vertical_margin,
            show=show,
        )
        self._children.append(child)
        return child

    @classmethod
    @validate_call
    def register_drawing_item(  # noqa: PLR0913
        cls,
        name: str,
        location: Literal["before", "after"],
        padding_width: float,
        function: Callable,
        style: Style,
        args: dict,
    ) -> None:
        """Register a drawing item for the tree node.

        Args:
            name (str): Name of drawing item.
            location (Literal["before", "after"]): The location of the drawing item relative to the text.
            padding_width (float): The padding width for the drawing item.
            function (Callable): The function to render the drawing item.
            style (Union[Style]): The style for the drawing item.
            args (dict): The arguments for the function.

        Returns:
            TreeNode: The current tree node instance.
        """
        style = style.patch(text_halign="left", text_valign="center")

        item = _TreeNodeDrawingItem(
            location=location,
            padding_width=padding_width,
            function=function,
            style=style,
            args=args,
        )

        cls._drawing_item_map[name] = item

    @validate_call
    def set_drawing_item(
        self,
        name: str,
    ) -> Self:
        """Set a drawing item for the tree node.

        Args:
            name (str): Name of drawing item.

        Returns:
            TreeNode: The current tree node instance.
        """
        if name not in self._drawing_item_map:
            raise ValueError(f'Drawing item "{name}" is not registered.')
        self._drawing_item_name = name

        return self

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        scale: PosFloat = 1.0,
    ) -> None:
        """Draw the tree node and its children.

        Args:
            xy: The coordinates to start drawing.
            scale: Proportional scale factor around xy. Defaults to 1.0.

        Raises:
            ValueError: If any required style or margin is missing on the root node.
        """
        if self._text_style is None:
            raise ValueError('Root of TreeNode must be initialized with "text_style".')
        if self._line_style is None:
            raise ValueError('Root of TreeNode must be initialized with "line_style".')
        if self._line_horizontal_margin is None:
            raise ValueError('Root of TreeNode must be initialized with "line_horizontal_margin".')
        if self._line_horizontal_length is None:
            raise ValueError('Root of TreeNode must be initialized with "line_horizontal_length".')
        if self._line_vertical_margin is None:
            raise ValueError('Root of TreeNode must be initialized with "line_vertical_margin".')

        with transform(origin=xy, scale=scale):
            self._draw(
                xy=xy,
                effective_text_style=self._text_style,
                effective_line_style=self._line_style,
                effective_line_horizontal_margin=self._line_horizontal_margin,
                effective_line_horizontal_length=self._line_horizontal_length,
                effective_line_vertical_margin=self._line_vertical_margin,
            )

    def _draw(  # noqa: C901, PLR0912, PLR0913
        self,
        xy: Coordinate,
        effective_text_style: Style,
        effective_line_style: Style,
        effective_line_horizontal_margin: PosFloat,
        effective_line_horizontal_length: PosFloat,
        effective_line_vertical_margin: PosFloat,
    ) -> float:
        """Draw the tree node and its children (internal method).

        Args:
            xy: The coordinates to start drawing.
            effective_text_style: The effective text style inherited from parent.
            effective_line_style: The effective line style inherited from parent.
            effective_line_horizontal_margin: The effective horizontal line margin inherited from parent.
            effective_line_horizontal_length: The effective horizontal line length inherited from parent.
            effective_line_vertical_margin: The effective vertical line margin inherited from parent.

        Returns:
            float: The y-coordinate after drawing the node and its children.
        """
        # Cascade overrides: if this node specified a value, it overrides for this node and descendants
        if self._text_style is not None:
            effective_text_style = self._text_style
        if self._line_style is not None:
            effective_line_style = self._line_style
        if self._line_horizontal_margin is not None:
            effective_line_horizontal_margin = self._line_horizontal_margin
        if self._line_horizontal_length is not None:
            effective_line_horizontal_length = self._line_horizontal_length
        if self._line_vertical_margin is not None:
            effective_line_vertical_margin = self._line_vertical_margin

        # draw text
        if self.show:
            patched_text_style = effective_text_style.patch(text_halign="left")
            if self._drawing_item_name is None:
                text(xy=xy, text=self._text, style=patched_text_style)

            else:
                drawing_item = self._drawing_item_map[self._drawing_item_name]

                if drawing_item.location == "before":
                    args = dict(drawing_item.args)
                    args["xy"] = xy
                    args["style"] = drawing_item.style
                    drawing_item.function(**args)

                    text(xy=(xy[0] + drawing_item.padding_width, xy[1]), text=self._text, style=patched_text_style)

                else:
                    text(xy=xy, text=self._text, style=patched_text_style)

                    args = dict(drawing_item.args)
                    args["xy"] = (xy[0] + drawing_item.padding_width, xy[1])
                    args["style"] = drawing_item.style
                    drawing_item.function(**args)

        # draw children
        horizontal_line_x1 = xy[0] + effective_line_horizontal_margin
        horizontal_line_x2 = horizontal_line_x1 + effective_line_horizontal_length * 2 / 3
        child_x = horizontal_line_x1 + effective_line_horizontal_margin
        child_y = xy[1]
        last_visible_child_y: float | None = None
        for child in self._children:
            child_y -= effective_line_vertical_margin
            if self.show and child.show:
                # draw child horizontal line
                line(
                    xy1=(horizontal_line_x1, child_y),
                    xy2=(horizontal_line_x2, child_y),
                    style=effective_line_style,
                )
                last_visible_child_y = child_y
            # draw child
            child_y = child._draw(
                xy=(child_x, child_y),
                effective_text_style=effective_text_style,
                effective_line_style=effective_line_style,
                effective_line_horizontal_margin=effective_line_horizontal_margin,
                effective_line_horizontal_length=effective_line_horizontal_length,
                effective_line_vertical_margin=effective_line_vertical_margin,
            )
        # draw children vertical line
        if self.show and last_visible_child_y is not None:
            line(
                (horizontal_line_x1, xy[1] - effective_line_vertical_margin / 2),
                (horizontal_line_x1, last_visible_child_y),
                style=effective_line_style,
            )
        return child_y
