# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for UML Class diagrams."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

# Relationship kinds in UML Class diagrams
RelationshipType = Literal[
    "inheritance",
    "realization",
    "composition",
    "aggregation",
    "association",
    "dependency",
]

# Side attachment on class node borders
Side = Literal["left", "right", "top", "bottom", "auto"]

# Line routing strategy
RoutingType = Literal["orthogonal", "direct"]


class AttributeInfo(BaseModel):
    """Internal representation of a class attribute/field.

    Attributes:
        name: Name of the attribute.
        type: Data type string (e.g. 'int', 'str', 'list[Item]').
        is_public: Whether the attribute is public (True) or private (False). Defaults to True.
        visibility: Optional explicit UML visibility symbol ('+', '-', '#', '~'). Overrides is_public if set.
        default_value: Optional default value string.
        is_static: Whether the attribute is static (class-level).
    """

    model_config = ConfigDict(frozen=True)

    name: str
    type: str = ""
    is_public: bool = True
    visibility: str | None = None
    default_value: str = ""
    is_static: bool = False

    @property
    def symbol(self) -> str:
        """Get visibility prefix symbol."""
        if self.visibility is not None:
            return self.visibility
        return "+" if self.is_public else "-"

    @property
    def display_text(self) -> str:
        """Formatted string representation for rendering."""
        parts = [f"{self.symbol} {self.name}"]
        if self.type:
            parts.append(f": {self.type}")
        if self.default_value:
            parts.append(f" = {self.default_value}")
        return "".join(parts)


class MethodInfo(BaseModel):
    """Internal representation of a class operation/method.

    Attributes:
        name: Method name (with or without parentheses).
        params: Parameter signature string (e.g. 'amount: float').
        return_type: Return type string (e.g. 'bool', 'void').
        is_public: Whether the method is public (True) or private (False). Defaults to True.
        visibility: Optional explicit UML visibility symbol ('+', '-', '#', '~'). Overrides is_public if set.
        is_static: Whether the method is static.
        is_abstract: Whether the method is abstract.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    params: str = ""
    return_type: str = ""
    is_public: bool = True
    visibility: str | None = None
    is_static: bool = False
    is_abstract: bool = False

    @property
    def symbol(self) -> str:
        """Get visibility prefix symbol."""
        if self.visibility is not None:
            return self.visibility
        return "+" if self.is_public else "-"

    @property
    def display_text(self) -> str:
        """Formatted string representation for rendering."""
        name_part = self.name
        if not ("(" in name_part and ")" in name_part):
            name_part = f"{name_part}({self.params})"
        parts = [f"{self.symbol} {name_part}"]
        if self.return_type:
            parts.append(f": {self.return_type}")
        return "".join(parts)
