# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for sequence diagrams."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypeAlias

from PIL.Image import Image

from drawlib._core.l3_images import Dimage

if TYPE_CHECKING:
    from drawlib._diagrams.architecture._icons import CustomIcon, GcpIcon, PhosphorIcon
    from drawlib._diagrams.sequence._block import Block
    from drawlib._diagrams.sequence._group import ParticipantGroup
    from drawlib._diagrams.sequence._message import Message
    from drawlib._diagrams.sequence._note import Note
    from drawlib._diagrams.sequence._participant import Participant

# Arrowhead directionality
ArrowType = Literal["->", "<->", "-"] | str

# Note position relative to participant lifeline
NotePosition = Literal["left", "right", "over"]

# Control block types
BlockType = Literal["loop", "alt", "else", "opt", "par", "critical", "break"]

# Message clearance padding (float or (start, end) tuple)
PaddingType = float | tuple[float, float]

# Diagram canvas padding (single float or (top, right, bottom, left) tuple)
DiagramPadding = float | tuple[float, float, float, float]

# Supported icon representations
IconFunction = Callable[..., object]
IconType: TypeAlias = "GcpIcon | PhosphorIcon | CustomIcon | Dimage | Image | str | Path | IconFunction | None"

# Sequence timeline event items
SequenceItem: TypeAlias = "Participant | Message | Note | Block | ParticipantGroup"
