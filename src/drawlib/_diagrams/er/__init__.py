# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""ER diagram internal module package."""

from __future__ import annotations

from drawlib._diagrams.er._diagram import ERDiagram
from drawlib._diagrams.er._entity import Entity
from drawlib._diagrams.er._relationship import Relationship
from drawlib._diagrams.er._types import Cardinality, ColumnInfo, RoutingType, Side

__all__ = [
    "Cardinality",
    "ColumnInfo",
    "ERDiagram",
    "Entity",
    "Relationship",
    "RoutingType",
    "Side",
]
