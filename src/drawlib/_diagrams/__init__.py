# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Internal diagrams module package."""

from __future__ import annotations

from drawlib._diagrams import architecture, class_diagram, er, flow, sequence
from drawlib._diagrams.architecture import ArchitectureDiagram
from drawlib._diagrams.class_diagram import ClassDiagram
from drawlib._diagrams.er import ERDiagram
from drawlib._diagrams.flow import FlowDiagram
from drawlib._diagrams.sequence import SequenceDiagram

__all__ = [
    "ArchitectureDiagram",
    "ClassDiagram",
    "ERDiagram",
    "FlowDiagram",
    "SequenceDiagram",
    "architecture",
    "class_diagram",
    "er",
    "flow",
    "sequence",
]
