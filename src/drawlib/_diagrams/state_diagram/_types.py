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

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict

# Node visual shape kinds
ShapeType = Literal[
    "box",
    "oval",
    "circle",
    "double_circle",
    "text_only",
]

# Side attachment on state borders
Side = Literal[
    "left",
    "right",
    "top",
    "bottom",
    "auto",
    "top_right",
    "top_left",
    "bottom_right",
    "bottom_left",
]

# Self-loop placement side
LoopSide = Literal[
    "top",
    "bottom",
    "left",
    "right",
    "top_right",
    "top_left",
    "bottom_right",
    "bottom_left",
]

# Line routing strategy
RoutingType = Literal["curved", "orthogonal", "direct"]

# Padding type
PaddingType = Union[float, tuple[float, float]]


class StateAction(BaseModel):
    """Internal representation of a state internal activity / action (entry, do, exit).

    Attributes:
        kind: Action trigger ('entry', 'do', 'exit', or custom).
        action: Activity or function call string.
    """

    model_config = ConfigDict(frozen=True)

    kind: str
    action: str

    @property
    def display_text(self) -> str:
        """Formatted string representation for rendering."""
        return f"{self.kind} / {self.action}"
