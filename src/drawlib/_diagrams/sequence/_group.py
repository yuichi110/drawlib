# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""ParticipantGroup implementation for sequence diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.sequence._diagram import SequenceDiagram
    from drawlib._diagrams.sequence._participant import Participant


class ParticipantGroup:
    """Grouping boundary enclosing participant headers at the top of a sequence diagram."""

    def __init__(
        self,
        title: str = "",
        padding: float = 4.0,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize ParticipantGroup.

        Args:
            title: Group title text.
            padding: Padding around enclosed participant header cards. Defaults to 4.0.
            style: Optional Style object for the boundary box.
            text_style: Optional Style object for the title text.
            show: Whether to render this group boundary. Defaults to True.
        """
        self.title = title
        self.padding = float(padding)
        self.style = style
        self.text_style = text_style
        self.show = bool(show)
        self._participants: list[Participant] = []
        self._diagram: SequenceDiagram | None = None

    @property
    def participants(self) -> list[Participant]:
        """Get the list of member participants in this group."""
        return list(self._participants)

    def add(self, participant: Participant, *, show: bool | None = None) -> Participant:
        """Add a participant to this group.

        Args:
            participant: Participant instance.
            show: Optional override for participant.show.

        Returns:
            Participant: The added participant for chaining or variable assignment.
        """
        if show is not None:
            participant.show = bool(show)
        if participant not in self._participants:
            self._participants.append(participant)
        if self._diagram is not None and participant not in self._diagram.participants:
            self._diagram.add(participant)
        return participant
