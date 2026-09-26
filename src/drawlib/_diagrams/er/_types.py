# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for ER (Entity-Relationship) diagrams."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

# Relationship multiplicity (IE / Crow's Foot notation)
Cardinality = Literal[
    "1:*",
    "1:1",
    "1:1..*",
    "1:0..1",
    "0..1:1",
    "0..1:*",
    "*:*",
]

# Side attachment on entity borders
Side = Literal["left", "right", "top", "bottom", "auto"]

# Line routing strategy
RoutingType = Literal["orthogonal", "direct"]


class ColumnInfo(BaseModel):
    """Internal representation of an entity column.

    Attributes:
        name: Name of the column.
        type: Data type string (e.g. 'INT', 'VARCHAR(255)').
        pk: Whether this column is a Primary Key.
        fk: Whether this column is a Foreign Key.
        nullable: Whether this column is nullable.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    type: str = ""
    pk: bool = False
    fk: bool = False
    nullable: bool = True
