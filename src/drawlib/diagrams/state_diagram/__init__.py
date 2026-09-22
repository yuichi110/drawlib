# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public State diagrams module."""

from __future__ import annotations

from drawlib._diagrams.state_diagram._diagram import StateDiagram
from drawlib._diagrams.state_diagram._state_node import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    State,
    StateNodeBase,
)
from drawlib._diagrams.state_diagram._transition import StateTransition
from drawlib._diagrams.state_diagram._types import (
    PaddingType,
    RoutingType,
    ShapeType,
    Side,
    StateAction,
)

__all__ = [
    "ChoiceState",
    "FinalState",
    "ForkJoinState",
    "InitialState",
    "PaddingType",
    "RoutingType",
    "ShapeType",
    "Side",
    "State",
    "StateAction",
    "StateDiagram",
    "StateNodeBase",
    "StateTransition",
]
