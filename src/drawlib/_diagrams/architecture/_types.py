# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for architecture diagrams."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Literal, TypeVar, Union

from PIL.Image import Image

from drawlib._core.images import Dimage

if TYPE_CHECKING:
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
    from drawlib._diagrams.architecture._group import NodeGroup
    from drawlib._diagrams.architecture._icons import CustomIcon, GcpIcon, PhosphorIcon
    from drawlib._diagrams.architecture._junction import Junction
    from drawlib._diagrams.architecture._node import Node

# Connectable elements (can be start or end of an edge)
Connectable = Union["Node", "NodeGroup", "Junction"]

# Diagram / Group item that can be added
DiagramItem = Union["Node", "NodeGroup", "Junction"]
ItemT = TypeVar("ItemT", bound="DiagramItem")

# Edge routing strategy
RoutingType = Literal["orthogonal", "direct", "curved"]

# Arrowhead configuration
ArrowType = Union[Literal["->", "<-", "<->", "-"], str]

# Edge padding type (float or (start_padding, end_padding))
PaddingType = Union[float, tuple[float, float]]

# Node label placement relative to icon
TextPosition = Literal["bottom", "top", "left", "right"]

# Node icon types supported
IconFunction = Callable[..., object]
IconType = Union[
    "GcpIcon",
    "PhosphorIcon",
    "CustomIcon",
    Dimage,
    Image,
    str,
    Path,
    IconFunction,
    None,
]

DiagramT = TypeVar("DiagramT", bound="ArchitectureDiagram")
