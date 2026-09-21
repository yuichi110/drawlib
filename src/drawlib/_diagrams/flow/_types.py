# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for Flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeVar, Union

if TYPE_CHECKING:
    from drawlib._diagrams.flow._diagram import FlowDiagram
    from drawlib._diagrams.flow._junction import Junction
    from drawlib._diagrams.flow._node import FlowNode

# Edge routing strategy
RoutingType = Literal["orthogonal", "direct"]

# Attachment side on node boundary
Side = Literal["left", "right", "top", "bottom", "auto"]

# Supported flowchart shape types
ShapeType = Literal["process", "decision", "start", "end", "data"]

# Swimlane layout direction
Orientation = Literal["vertical", "horizontal"]

# Arrowhead directionality
ArrowType = Union[Literal["->", "<-", "<->", "-"], str]

# Edge padding (gap clearance)
PaddingType = Union[float, tuple[float, float]]

# Connectable elements
Connectable = Union["FlowNode", "Junction"]

# Diagram items that can be added via add()
DiagramItem = Union["FlowNode", "Junction"]
ItemT = TypeVar("ItemT", bound="DiagramItem")

DiagramT = TypeVar("DiagramT", bound="FlowDiagram")
