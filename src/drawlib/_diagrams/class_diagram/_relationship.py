# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Relationship connection model for UML Class diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from drawlib._diagrams.class_diagram._types import RelationshipType, RoutingType, Side

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.class_diagram._class_node import ClassNode
    from drawlib._diagrams.class_diagram._diagram import ClassDiagram

PaddingType = Union[float, tuple[float, float]]


class ClassRelationship:
    """Represents a relationship edge connecting two classes in a UML Class diagram."""

    def __init__(
        self,
        start: ClassNode,
        end: ClassNode,
        relationship_type: RelationshipType = "association",
        start_side: Side = "auto",
        end_side: Side = "auto",
        label: str = "",
        start_multiplicity: str = "",
        end_multiplicity: str = "",
        start_role: str = "",
        end_role: str = "",
        directed: bool = False,
        style: Style | None = None,
        routing: RoutingType = "orthogonal",
        padding: PaddingType = 0.0,
    ) -> None:
        """Initialize ClassRelationship.

        Args:
            start: Source ClassNode.
            end: Target ClassNode.
            relationship_type: UML relation kind ('inheritance', 'realization', 'composition',
                'aggregation', 'association', 'dependency').
            start_side: Attachment side on start class ('left', 'right', 'top', 'bottom', 'auto').
            end_side: Attachment side on end class ('left', 'right', 'top', 'bottom', 'auto').
            label: Optional relationship label text.
            start_multiplicity: Optional multiplicity text at the start anchor (e.g. '1', '0..1').
            end_multiplicity: Optional multiplicity text at the end anchor (e.g. '*', '1..*').
            start_role: Optional role name at start anchor.
            end_role: Optional role name at end anchor.
            directed: Whether to draw a directional open arrow at the end (for association/aggregation/composition).
            style: Optional Style object overriding relationship appearance.
            routing: Path routing strategy ('orthogonal' or 'direct').
            padding: Gap distance between class borders and line endpoints.
        """
        valid_types = {
            "inheritance",
            "realization",
            "composition",
            "aggregation",
            "association",
            "dependency",
        }
        if relationship_type not in valid_types:
            raise ValueError(
                f"Invalid relationship_type: {relationship_type!r}. Must be one of {sorted(valid_types)}."
            )

        valid_sides = {"left", "right", "top", "bottom", "auto"}
        if start_side not in valid_sides:
            raise ValueError(f"Invalid start_side: {start_side!r}. Must be one of {sorted(valid_sides)}.")
        if end_side not in valid_sides:
            raise ValueError(f"Invalid end_side: {end_side!r}. Must be one of {sorted(valid_sides)}.")

        valid_routings = {"orthogonal", "direct"}
        if routing not in valid_routings:
            raise ValueError(f"Invalid routing: {routing!r}. Must be one of {sorted(valid_routings)}.")

        self.start = start
        self.end = end
        self.relationship_type: RelationshipType = relationship_type
        self.start_side: Side = start_side
        self.end_side: Side = end_side
        self.label = label
        self.start_multiplicity = start_multiplicity
        self.end_multiplicity = end_multiplicity
        self.start_role = start_role
        self.end_role = end_role
        self.directed = directed
        self.style = style
        self.routing: RoutingType = routing
        self.padding: PaddingType = padding

        self._diagram: ClassDiagram | None = None
