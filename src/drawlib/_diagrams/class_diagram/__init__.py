# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Internal UML Class diagrams module."""

from __future__ import annotations

from drawlib._diagrams.class_diagram._class_node import ClassNode
from drawlib._diagrams.class_diagram._diagram import ClassDiagram
from drawlib._diagrams.class_diagram._relationship import ClassRelationship
from drawlib._diagrams.class_diagram._types import (
    AttributeInfo,
    MethodInfo,
    RelationshipType,
    RoutingType,
    Side,
)

__all__ = [
    "AttributeInfo",
    "ClassDiagram",
    "ClassNode",
    "ClassRelationship",
    "MethodInfo",
    "RelationshipType",
    "RoutingType",
    "Side",
]
