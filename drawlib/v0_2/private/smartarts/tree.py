# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Tree implementation module."""

from __future__ import annotations

import dataclasses
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

from drawlib.v0_2.private.core.model import IconStyle, ImageStyle, LineStyle, ShapeStyle, TextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core_canvas.canvas import line, text


class TreeNode:
    """Class for rendering smart art Tree."""

    _drawing_item_map: Dict[str, _TreeNodeDrawingItem] = {}

    def __init__(
        self,
        text: str,
        textstyle: Union[str, TextStyle, None] = None,
        linestyle: Union[str, LineStyle, None] = None,
        line_horizontal_margin: Optional[float] = None,
        line_horizontal_length: Optional[float] = None,
        line_vertical_margin: Optional[float] = None,
        children: Optional[List[TreeNode]] = None,
        default_textstyle: Union[str, TextStyle, None] = None,
        default_linestyle: Union[str, LineStyle, None] = None,
        default_line_horizontal_margin: Optional[float] = None,
        default_line_horizontal_length: Optional[float] = None,
        default_line_vertical_margin: Optional[float] = None,
    ) -> None:
        """Initialize class."""
        self._text = text

        if isinstance(textstyle, str):
            textstyle = dtheme.textstyles.get(textstyle)
        self._textstyle = textstyle
        if isinstance(linestyle, str):
            linestyle = dtheme.linestyles.get(linestyle)
        self._linestyle = linestyle

        self._line_horizontal_margin = line_horizontal_margin
        self._line_horizontal_length = line_horizontal_length
        self._line_vertical_margin = line_vertical_margin

        if children is None:
            self._children: List[TreeNode] = []
        else:
            self._children: List[TreeNode] = children

        if isinstance(default_textstyle, str):
            default_textstyle = dtheme.textstyles.get(default_textstyle)
        self._default_textstyle: Union[TextStyle, None] = default_textstyle
        if isinstance(default_linestyle, str):
            default_linestyle = dtheme.linestyles.get(default_linestyle)
        self._default_linestyle: Union[LineStyle, None] = default_linestyle

        self._default_line_horizontal_margin: Optional[float] = default_line_horizontal_margin
        self._default_line_horizontal_length: Optional[float] = default_line_horizontal_length
        self._default_line_vertical_margin: Optional[float] = default_line_vertical_margin

        self._drawing_item_name: Optional[str] = None

    @classmethod
    def register_drawing_item(
        cls,
        name: str,
        location: Literal["before", "after"],
        padding_width: float,
        function: Callable,
        style: Union[IconStyle, ImageStyle, ShapeStyle, TextStyle],
        args: dict,
    ) -> None:
        """Register a drawing item for the tree node.

        Args:
            name (str): Name of drawing item.
            location (Literal["before", "after"]): The location of the drawing item relative to the text.
            padding_width (float): The padding width for the drawing item.
            function (Callable): The function to render the drawing item.
            style (Union[IconStyle, ImageStyle, ShapeStyle, TextStyle]): The style for the drawing item.
            args (dict): The arguments for the function.

        Returns:
            TreeNode: The current tree node instance.
        """
        style.halign = "left"
        style.valign = "center"

        item = _TreeNodeDrawingItem(
            location=location,
            padding_width=padding_width,
            function=function,
            style=style,
            args=args,
        )

        cls._drawing_item_map[name] = item

    def set_drawing_item(
        self,
        name: str,
    ) -> TreeNode:
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

    def draw(self, xy: Tuple[float, float]) -> None:
        """Draw the tree node and its children.

        Args:
            xy (Tuple[float, float]): The coordinates to start drawing.

        Raises:
            ValueError: If any of the default styles or margins are None.
        """
        if self._default_textstyle is None:
            raise ValueError()
        if self._default_linestyle is None:
            raise ValueError()
        if self._default_line_horizontal_margin is None:
            raise ValueError()
        if self._default_line_horizontal_length is None:
            raise ValueError()
        if self._default_line_vertical_margin is None:
            raise ValueError()

        self._draw(
            xy=xy,
            default_textstyle=self._default_textstyle,
            default_linestyle=self._default_linestyle,
            default_line_horizontal_margin=self._default_line_horizontal_margin,
            default_line_horizontal_length=self._default_line_horizontal_length,
            default_line_vertical_margin=self._default_line_vertical_margin,
        )

    def _draw(  # noqa: C901
        self,
        xy: Tuple[float, float],
        default_textstyle: TextStyle,
        default_linestyle: LineStyle,
        default_line_horizontal_margin: float,
        default_line_horizontal_length: float,
        default_line_vertical_margin: float,
    ) -> float:
        """Draw the tree node and its children (internal method).

        Args:
            xy (Tuple[float, float]): The coordinates to start drawing.
            default_textstyle (TextStyle): The default text style.
            default_linestyle (LineStyle): The default line style.
            default_line_horizontal_margin (float): The default horizontal line margin.
            default_line_horizontal_length (float): The default horizontal line length.
            default_line_vertical_margin (float): The default vertical line margin.

        Returns:
            float: The y-coordinate after drawing the node and its children.
        """
        # update default values
        if self._default_textstyle is not None:
            default_textstyle = self._default_textstyle
        if self._default_linestyle is not None:
            default_linestyle = self._default_linestyle
        if self._default_line_horizontal_margin is not None:
            default_line_horizontal_margin = self._default_line_horizontal_margin
        if self._default_line_horizontal_length is not None:
            default_line_horizontal_length = self._default_line_horizontal_length
        if self._default_line_vertical_margin is not None:
            default_line_vertical_margin = self._default_line_vertical_margin

        # update values
        textstyle = self._textstyle if self._textstyle is not None else default_textstyle
        linestyle = self._linestyle if self._linestyle is not None else default_linestyle
        if self._line_horizontal_margin is not None:
            line_horizontal_margin = self._line_horizontal_margin
        else:
            line_horizontal_margin = default_line_horizontal_margin
        if self._line_horizontal_length is not None:
            line_horizontal_length = self._line_horizontal_length
        else:
            line_horizontal_length = default_line_horizontal_length
        if self._line_vertical_margin is not None:
            line_vertical_margin = self._line_vertical_margin
        else:
            line_vertical_margin = default_line_vertical_margin

        # draw text
        if self._drawing_item_name is None:
            textstyle.halign = "left"
            text(xy=xy, text=self._text, style=textstyle)

        else:
            drawing_item = self._drawing_item_map[self._drawing_item_name]

            if drawing_item.location == "before":
                args = drawing_item.args
                args["xy"] = xy
                args["style"] = drawing_item.style
                drawing_item.function(**args)

                textstyle.halign = "left"
                text(xy=(xy[0] + drawing_item.padding_width, xy[1]), text=self._text, style=textstyle)

            else:
                textstyle.halign = "left"
                text(xy=xy, text=self._text, style=textstyle)

                args = drawing_item.args
                args["xy"] = (xy[0] + drawing_item.padding_width, xy[1])
                args["style"] = drawing_item.style
                drawing_item.function(**args)

        # draw children
        horizontal_line_x1 = xy[0] + line_horizontal_margin
        horizontal_line_x2 = horizontal_line_x1 + line_horizontal_length * 2 / 3
        child_x = horizontal_line_x1 + line_horizontal_margin
        child_y = xy[1]
        child_y_previous = child_y
        for child in self._children:
            child_y -= line_vertical_margin
            # draw child horizontal line
            line(
                xy1=(horizontal_line_x1, child_y),
                xy2=(horizontal_line_x2, child_y),
                style=linestyle,
            )
            # draw child
            child_y_previous = child_y
            child_y = child._draw(
                xy=(child_x, child_y),
                default_textstyle=default_textstyle,
                default_linestyle=default_linestyle,
                default_line_horizontal_margin=default_line_horizontal_margin,
                default_line_horizontal_length=default_line_horizontal_length,
                default_line_vertical_margin=default_line_vertical_margin,
            )
        # draw children vertical line
        if xy[1] != child_y_previous:
            line(
                (horizontal_line_x1, xy[1] - line_vertical_margin / 2),
                (horizontal_line_x1, child_y_previous),
                style=linestyle,
            )
        return child_y


@dataclasses.dataclass
class _TreeNodeDrawingItem:
    location: Literal["before", "after"]
    padding_width: float
    function: Callable
    style: Union[IconStyle, ImageStyle, ShapeStyle, TextStyle]
    args: dict
