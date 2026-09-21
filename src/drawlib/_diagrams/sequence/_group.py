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
    from drawlib._diagrams.sequence._diagram import Diagram
    from drawlib._diagrams.sequence._participant import Participant


class ParticipantGroup:
    """Grouping boundary enclosing participant headers at the top of a sequence diagram."""

    def __init__(
        self,
        title: str = "",
        padding: float = 4.0,
        style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Initialize ParticipantGroup.

        Args:
            title: Group title text.
            padding: Padding around enclosed participant header cards. Defaults to 4.0.
            style: Optional Style object for the boundary box.
            textstyle: Optional Style object for the title text.
        """
        self.title = title
        self.padding = float(padding)
        self.style = style
        self.textstyle = textstyle
        self._participants: list[Participant] = []
        self._diagram: Diagram | None = None

    @property
    def participants(self) -> list[Participant]:
        """Get the list of member participants in this group."""
        return list(self._participants)

    def add(self, participant: Participant) -> Participant:
        """Add a participant to this group.

        Args:
            participant: Participant instance.

        Returns:
            Participant: The added participant for chaining or variable assignment.
        """
        if participant not in self._participants:
            self._participants.append(participant)
        if self._diagram is not None and participant not in self._diagram.participants:
            self._diagram.add(participant)
        return participant
