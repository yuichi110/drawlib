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
from drawlib._core.l4_canvas import line, text


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

    def __init__(
        self,
        text: str,
        *,
        text_style: Style | None = None,
        line_style: Style | None = None,
        line_horizontal_margin: PosFloat | None = None,
        line_horizontal_length: PosFloat | None = None,
        line_vertical_margin: PosFloat | None = None,
        children: list[TreeNode] | None = None,
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
        """
        self._text = text
        self._text_style = text_style
        self._line_style = line_style
        self._line_horizontal_margin = line_horizontal_margin
        self._line_horizontal_length = line_horizontal_length
        self._line_vertical_margin = line_vertical_margin
        self._children: list[TreeNode] = children if children is not None else []
        self._drawing_item_name: str | None = None

    @classmethod
    @validate_call
    def register_drawing_item(
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
    def draw(self, xy: Coordinate) -> None:
        """Draw the tree node and its children.

        Args:
            xy: The coordinates to start drawing.

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

        self._draw(
            xy=xy,
            effective_text_style=self._text_style,
            effective_line_style=self._line_style,
            effective_line_horizontal_margin=self._line_horizontal_margin,
            effective_line_horizontal_length=self._line_horizontal_length,
            effective_line_vertical_margin=self._line_vertical_margin,
        )

    def _draw(  # noqa: C901
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
        patched_text_style = effective_text_style.patch(text_halign="left")
        if self._drawing_item_name is None:
            text(xy=xy, text=self._text, style=patched_text_style)

        else:
            drawing_item = self._drawing_item_map[self._drawing_item_name]

            if drawing_item.location == "before":
                args = drawing_item.args
                args["xy"] = xy
                args["style"] = drawing_item.style
                drawing_item.function(**args)

                text(xy=(xy[0] + drawing_item.padding_width, xy[1]), text=self._text, style=patched_text_style)

            else:
                text(xy=xy, text=self._text, style=patched_text_style)

                args = drawing_item.args
                args["xy"] = (xy[0] + drawing_item.padding_width, xy[1])
                args["style"] = drawing_item.style
                drawing_item.function(**args)

        # draw children
        horizontal_line_x1 = xy[0] + effective_line_horizontal_margin
        horizontal_line_x2 = horizontal_line_x1 + effective_line_horizontal_length * 2 / 3
        child_x = horizontal_line_x1 + effective_line_horizontal_margin
        child_y = xy[1]
        child_y_previous = child_y
        for child in self._children:
            child_y -= effective_line_vertical_margin
            # draw child horizontal line
            line(
                xy1=(horizontal_line_x1, child_y),
                xy2=(horizontal_line_x2, child_y),
                style=effective_line_style,
            )
            # draw child
            child_y_previous = child_y
            child_y = child._draw(
                xy=(child_x, child_y),
                effective_text_style=effective_text_style,
                effective_line_style=effective_line_style,
                effective_line_horizontal_margin=effective_line_horizontal_margin,
                effective_line_horizontal_length=effective_line_horizontal_length,
                effective_line_vertical_margin=effective_line_vertical_margin,
            )
        # draw children vertical line
        if xy[1] != child_y_previous:
            line(
                (horizontal_line_x1, xy[1] - effective_line_vertical_margin / 2),
                (horizontal_line_x1, child_y_previous),
                style=effective_line_style,
            )
        return child_y
