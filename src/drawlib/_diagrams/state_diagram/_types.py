# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for State diagrams."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Union

# Node visual shape kinds
ShapeType = Literal[
    "box",
    "oval",
    "circle",
    "double_circle",
    "text_only",
]

# Side attachment on state borders
Side = Literal["left", "right", "top", "bottom", "auto"]

# Line routing strategy
RoutingType = Literal["curved", "orthogonal", "direct"]

# Padding type
PaddingType = Union[float, tuple[float, float]]


@dataclass(frozen=True)
class StateAction:
    """Internal representation of a state internal activity / action (entry, do, exit).

    Attributes:
        kind: Action trigger ('entry', 'do', 'exit', or custom).
        action: Activity or function call string.
    """

    kind: str
    action: str

    @property
    def display_text(self) -> str:
        """Formatted string representation for rendering."""
        return f"{self.kind} / {self.action}"
