# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public diagrams package for drawlib."""

from __future__ import annotations

from drawlib.diagrams import architecture, class_diagram, er, flow, sequence, state_diagram
from drawlib.diagrams.architecture import ArchitectureDiagram
from drawlib.diagrams.class_diagram import ClassDiagram
from drawlib.diagrams.er import ERDiagram
from drawlib.diagrams.flow import FlowDiagram
from drawlib.diagrams.sequence import SequenceDiagram
from drawlib.diagrams.state_diagram import StateDiagram

__all__ = [
    "ArchitectureDiagram",
    "ClassDiagram",
    "ERDiagram",
    "FlowDiagram",
    "SequenceDiagram",
    "StateDiagram",
    "architecture",
    "class_diagram",
    "er",
    "flow",
    "sequence",
    "state_diagram",
]
