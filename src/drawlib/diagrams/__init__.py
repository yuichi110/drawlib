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

from drawlib.diagrams import architecture, er, sequence
from drawlib.diagrams.architecture import ArchitectureDiagram
from drawlib.diagrams.er import ERDiagram
from drawlib.diagrams.sequence import SequenceDiagram

__all__ = [
    "ArchitectureDiagram",
    "ERDiagram",
    "SequenceDiagram",
    "architecture",
    "er",
    "sequence",
]
