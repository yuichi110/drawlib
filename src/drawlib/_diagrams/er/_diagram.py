# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""ERDiagram class implementation for ER diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

import drawlib._diagrams.er._relationship as _relationship_module
import drawlib._diagrams.er._renderer as _renderer_module
from drawlib._diagrams.er._types import Cardinality, RoutingType, Side

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.er._entity import Entity
    from drawlib._diagrams.er._relationship import Relationship

PaddingType = Union[float, tuple[float, float]]


class ERDiagram:
    """Top-level container for ER (Entity-Relationship) diagrams."""

    def __init__(
        self,
        title: str = "",
        width: float | None = None,
        height: float | None = None,
        style: Style | None = None,
    ) -> None:
        """Initialize ERDiagram.

        Args:
            title: Optional diagram title.
            width: Optional fixed width of the diagram.
            height: Optional fixed height of the diagram.
            style: Optional Style object for the diagram background.
        """
        self.title = title
        self.width = float(width) if width is not None else None
        self.height = float(height) if height is not None else None
        self.style = style

        self._entities: list[tuple[Entity, tuple[float, float]]] = []
        self._relationships: list[Relationship] = []

    @property
    def entities(self) -> list[Entity]:
        """Get list of entities registered in the diagram."""
        return [ent for ent, _ in self._entities]

    @property
    def relationships(self) -> list[Relationship]:
        """Get list of relationships registered in the diagram."""
        return list(self._relationships)

    def add(self, entity: Entity, xy: tuple[float, float]) -> Entity:
        """Add an Entity to the diagram at center coordinate xy.

        Args:
            entity: Entity instance to place.
            xy: Center coordinate (cx, cy) of the entity in the diagram.

        Returns:
            Entity: The added entity for chaining or assignment.
        """
        pt = (float(xy[0]), float(xy[1]))
        entity._local_xy = pt
        entity._diagram = self
        self._entities.append((entity, pt))
        return entity

    def add_relationship(self, relationship: Relationship) -> Relationship:
        """Register a Relationship connection with this diagram.

        Args:
            relationship: Relationship instance to register.

        Returns:
            Relationship: The registered relationship.
        """
        relationship._diagram = self
        if relationship not in self._relationships:
            self._relationships.append(relationship)
        return relationship

    def connect(
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
    ) -> Relationship:
        """Create and register a relationship between two entities.

        Args:
            start: Start Entity.
            end: End Entity.
            cardinality: Multiplicity ("1:*", "1:1", "1:1..*", "1:0..1", "0..1:1", "0..1:*", "*:*").
            start_side: Attachment side on start entity ("left", "right", "top", "bottom", "auto").
            end_side: Attachment side on end entity ("left", "right", "top", "bottom", "auto").
            start_column: Optional column name in start entity.
            end_column: Optional column name in end entity.
            label: Optional connection label text.
            style: Optional Style object for the line.
            routing: Path routing strategy ("orthogonal" or "direct").
            padding: Gap distance between entity borders and line ends.

        Returns:
            Relationship: Newly created and registered relationship.
        """
        rel = _relationship_module.Relationship(
            start=start,
            end=end,
            cardinality=cardinality,
            start_side=start_side,
            end_side=end_side,
            start_column=start_column,
            end_column=end_column,
            label=label,
            style=style,
            routing=routing,
            padding=padding,
        )
        self.add_relationship(rel)
        return rel

    def get_size(self) -> tuple[float, float]:
        """Get overall width and height of the diagram based on entities or fixed dimensions.

        Returns:
            Tuple of (width, height).
        """
        if self.width is not None and self.height is not None:
            return (self.width, self.height)

        if not self._entities:
            return (100.0, 100.0)

        max_x = 0.0
        max_y = 0.0
        for ent, (ix, iy) in self._entities:
            _, _, c_max_x, c_max_y = ent.get_bounds()
            max_x = max(max_x, ix + c_max_x)
            max_y = max(max_y, iy + c_max_y)

        final_w = self.width if self.width is not None else max_x + 10.0
        final_h = self.height if self.height is not None else max_y + 10.0
        return (final_w, final_h)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render the complete ER diagram onto the canvas at base coordinate xy.

        Args:
            xy: Base canvas coordinate (x, y) where diagram's bottom-left origin is placed.
        """
        _renderer_module.draw_er_diagram(self, xy)
