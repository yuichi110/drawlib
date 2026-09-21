# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Relationship connection model for ER diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from drawlib._diagrams.er._types import Cardinality, RoutingType, Side

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.er._diagram import ERDiagram
    from drawlib._diagrams.er._entity import Entity

PaddingType = Union[float, tuple[float, float]]


class Relationship:
    """Represents an edge connecting two database entities with Crow's Foot markers."""

    def __init__(
        self,
        start: Entity,
        end: Entity,
        cardinality: Cardinality = "1:*",
        start_side: Side = "auto",
        end_side: Side = "auto",
        start_column: str | None = None,
        end_column: str | None = None,
        label: str = "",
        style: Style | None = None,
        routing: RoutingType = "orthogonal",
        padding: PaddingType = 0.0,
    ) -> None:
        """Initialize Relationship.

        Args:
            start: Source Entity.
            end: Target Entity.
            cardinality: Multiplicity notation ("1:*", "1:1", "1:1..*", "1:0..1", "0..1:1", "0..1:*", "*:*").
            start_side: Attachment side on start entity ("left", "right", "top", "bottom", "auto").
            end_side: Attachment side on end entity ("left", "right", "top", "bottom", "auto").
            start_column: Optional column name in start entity to anchor the connection.
            end_column: Optional column name in end entity to anchor the connection.
            label: Optional relationship label text.
            style: Optional Style object for the relationship line.
            routing: Routing strategy ("orthogonal" or "direct").
            padding: Gap distance between entity borders and line ends.
        """
        valid_cardinalities = {"1:*", "1:1", "1:1..*", "1:0..1", "0..1:1", "0..1:*", "*:*"}
        if cardinality not in valid_cardinalities:
            raise ValueError(
                f"Invalid cardinality: {cardinality!r}. Must be one of {sorted(valid_cardinalities)}."
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
        self.cardinality: Cardinality = cardinality
        self.start_side: Side = start_side
        self.end_side: Side = end_side
        self.start_column = start_column
        self.end_column = end_column
        self.label = label
        self.style = style
        self.routing: RoutingType = routing
        self.padding: PaddingType = padding

        self._diagram: ERDiagram | None = None
