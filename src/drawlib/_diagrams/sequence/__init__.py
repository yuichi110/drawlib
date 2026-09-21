# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Sequence diagrams implementation package."""

from __future__ import annotations

from drawlib._diagrams.sequence._block import Block
from drawlib._diagrams.sequence._diagram import Diagram
from drawlib._diagrams.sequence._group import ParticipantGroup
from drawlib._diagrams.sequence._message import Message
from drawlib._diagrams.sequence._note import Note
from drawlib._diagrams.sequence._participant import Participant

__all__ = [
    "Block",
    "Diagram",
    "Message",
    "Note",
    "Participant",
    "ParticipantGroup",
]
