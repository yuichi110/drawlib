# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Concrete flow shape classes for flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._diagrams.flow._node import FlowNode

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class Process(FlowNode):
    """Represents an action, task, or operation step (rendered as a rectangle)."""

    def __init__(
        self,
        text: str = "",
        width: float = 24.0,
        height: float = 12.0,
        r: float = 0.0,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize Process.

        Args:
            text: Description of the action or process.
            width: Width of the process box. Defaults to 24.0.
            height: Height of the process box. Defaults to 12.0.
            r: Corner radius for rounded corners. Defaults to 0.0.
            style: Optional Style for fill and border stroke.
            text_style: Optional Style for label text.
            show: Whether to render this node. Defaults to True.
        """
        super().__init__(
            text=text,
            width=width,
            height=height,
            r=r,
            style=style,
            text_style=text_style,
            shape_type="process",
            show=show,
        )


class Decision(FlowNode):
    """Represents a decision or branching point (rendered as a rhombus/diamond)."""

    def __init__(
        self,
        text: str = "",
        width: float = 22.0,
        height: float = 14.0,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize Decision.

        Args:
            text: Question or conditional expression (e.g. "Is Valid?").
            width: Width of the diamond. Defaults to 22.0.
            height: Height of the diamond. Defaults to 14.0.
            style: Optional Style for fill and border stroke.
            text_style: Optional Style for label text.
            show: Whether to render this node. Defaults to True.
        """
        super().__init__(
            text=text,
            width=width,
            height=height,
            r=0.0,
            style=style,
            text_style=text_style,
            shape_type="decision",
            show=show,
        )


class Start(FlowNode):
    """Represents the starting point of a flow (rendered as a stadium/pill shape)."""

    def __init__(
        self,
        text: str = "Start",
        width: float = 20.0,
        height: float = 10.0,
        r: float = 5.0,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize Start.

        Args:
            text: Starting label text. Defaults to "Start".
            width: Width of the terminal shape. Defaults to 20.0.
            height: Height of the terminal shape. Defaults to 10.0.
            r: Corner radius. Defaults to 5.0 (half height for full stadium curve).
            style: Optional Style for fill and border stroke.
            text_style: Optional Style for label text.
            show: Whether to render this node. Defaults to True.
        """
        super().__init__(
            text=text,
            width=width,
            height=height,
            r=r,
            style=style,
            text_style=text_style,
            shape_type="start",
            show=show,
        )


class End(FlowNode):
    """Represents the endpoint of a flow (rendered as a stadium/pill shape)."""

    def __init__(
        self,
        text: str = "End",
        width: float = 20.0,
        height: float = 10.0,
        r: float = 5.0,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize End.

        Args:
            text: Ending label text. Defaults to "End".
            width: Width of the terminal shape. Defaults to 20.0.
            height: Height of the terminal shape. Defaults to 10.0.
            r: Corner radius. Defaults to 5.0 (half height for full stadium curve).
            style: Optional Style for fill and border stroke.
            text_style: Optional Style for label text.
            show: Whether to render this node. Defaults to True.
        """
        super().__init__(
            text=text,
            width=width,
            height=height,
            r=r,
            style=style,
            text_style=text_style,
            shape_type="end",
            show=show,
        )


class Data(FlowNode):
    """Represents data input or output (rendered as a parallelogram)."""

    def __init__(
        self,
        text: str = "",
        width: float = 24.0,
        height: float = 12.0,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize Data.

        Args:
            text: Input/output data description.
            width: Width of the parallelogram. Defaults to 24.0.
            height: Height of the parallelogram. Defaults to 12.0.
            style: Optional Style for fill and border stroke.
            text_style: Optional Style for label text.
            show: Whether to render this node. Defaults to True.
        """
        super().__init__(
            text=text,
            width=width,
            height=height,
            r=0.0,
            style=style,
            text_style=text_style,
            shape_type="data",
            show=show,
        )
