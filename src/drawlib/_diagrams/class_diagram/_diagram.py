# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Diagram container for UML Class diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import validate_call

import drawlib._diagrams.class_diagram._renderer as _renderer_module
from drawlib._core.l2_types import PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import transform
from drawlib._diagrams.class_diagram._class_node import ClassNode
from drawlib._diagrams.class_diagram._relationship import ClassRelationship
from drawlib._diagrams.class_diagram._types import PaddingType, RelationshipType, RoutingType, Side


class ClassDiagram:
    """Top-level container managing classes, relationships, and layout for Class diagrams."""

    @validate_call
    def __init__(
        self,
        *,
        node_style: Style,
        edge_style: Style,
        edge_text_style: Style,
        title: str = "",
        title_style: Style | None = None,
        style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
        margin: float = 5.0,
        header_style: Style | None = None,
    ) -> None:
        """Initialize ClassDiagram.

        Args:
            node_style: Mandatory base Style object for class cards in the diagram.
            edge_style: Mandatory base Style object for relationship edges in the diagram.
            edge_text_style: Mandatory base Style object for relationship labels in the diagram.
            title: Optional title displayed above the diagram.
            title_style: Optional Style object for the diagram title.
            style: Optional Style overriding diagram background.
            width: Optional fixed canvas width. If None, auto-calculated from content.
            height: Optional fixed canvas height. If None, auto-calculated from content.
            margin: Outer margin padding surrounding all classes (default: 5.0).
            header_style: Optional Style overriding class card header compartments.
        """
        self.node_style = node_style
        self.edge_style = edge_style
        self.edge_text_style = edge_text_style
        self.header_style = header_style
        self.title = title
        self.title_style = title_style
        self.style = style
        self.custom_width = float(width) if width is not None else None
        self.custom_height = float(height) if height is not None else None
        self.margin = float(margin)

        self.classes: list[ClassNode] = []
        self.relationships: list[ClassRelationship] = []

    def add(
        self,
        class_node: ClassNode,
        xy: tuple[float, float] = (0.0, 0.0),
        show: bool | None = None,
    ) -> ClassNode:
        """Add a ClassNode to the diagram at the specified relative center coordinate.

        Args:
            class_node: ClassNode to register.
            xy: Center placement coordinate (cx, cy).
            show: Optional visibility override for the class node.

        Returns:
            ClassNode: The added class node for chaining.
        """
        class_node._local_xy = (float(xy[0]), float(xy[1]))
        class_node._diagram = self
        if show is not None:
            class_node.show = show
        self.classes.append(class_node)
        return class_node

    def add_relationship(self, rel: ClassRelationship) -> ClassRelationship:
        """Add a ClassRelationship to the diagram.

        Args:
            rel: ClassRelationship to register.

        Returns:
            ClassRelationship: The added relationship.
        """
        rel._diagram = self
        if rel not in self.relationships:
            self.relationships.append(rel)
        return rel

    def connect(
        self,
        source: ClassNode,
        target: ClassNode,
        relationship_type: RelationshipType = "association",
        *,
        type: RelationshipType | None = None,
        label: str = "",
        start_side: Side = "auto",
        end_side: Side = "auto",
        start_multiplicity: str = "",
        end_multiplicity: str = "",
        start_role: str = "",
        end_role: str = "",
        directed: bool = False,
        style: Style | None = None,
        text_style: Style | None = None,
        routing: RoutingType = "orthogonal",
        padding: PaddingType = 0.0,
        show: bool = True,
    ) -> ClassRelationship:
        """Create and register a relationship between two classes.

        Args:
            source: Start ClassNode.
            target: End ClassNode.
            relationship_type: Type of relationship ('inheritance', 'realization', 'composition',
                'aggregation', 'association', 'dependency'). Defaults to 'association'.
            type: Optional alias for relationship_type.
            label: Optional relationship label text.
            start_side: Attachment side on start class ('left', 'right', 'top', 'bottom', 'auto').
            end_side: Attachment side on end class ('left', 'right', 'top', 'bottom', 'auto').
            start_multiplicity: Multiplicity string near start ('1', '0..1', '*', etc.).
            end_multiplicity: Multiplicity string near end ('1', '0..1', '*', etc.).
            start_role: Role name label near start.
            end_role: Role name label near end.
            directed: Whether to draw a directional navigability arrow.
            style: Style object overriding relationship line and symbols.
            text_style: Style object overriding relationship labels.
            routing: Line path routing strategy ('orthogonal', 'direct').
            padding: Gap distance between class borders and line ends.
            show: Whether to render this relationship.

        Returns:
            ClassRelationship: Newly created and registered relationship.
        """
        resolved_type = type if type is not None else relationship_type
        rel = ClassRelationship(
            start=source,
            end=target,
            relationship_type=resolved_type,
            start_side=start_side,
            end_side=end_side,
            label=label,
            start_multiplicity=start_multiplicity,
            end_multiplicity=end_multiplicity,
            start_role=start_role,
            end_role=end_role,
            directed=directed,
            style=style,
            text_style=text_style,
            routing=routing,
            padding=padding,
            show=show,
        )
        return self.add_relationship(rel)

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Compute the enclosing bounding box [min_x, min_y, max_x, max_y] of all registered classes.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        if not self.classes:
            return (0.0, 0.0, 0.0, 0.0)

        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        for c in self.classes:
            cx, cy = c._local_xy
            half_w = c.width / 2.0
            half_h = c.effective_height / 2.0
            min_x = min(min_x, cx - half_w)
            min_y = min(min_y, cy - half_h)
            max_x = max(max_x, cx + half_w)
            max_y = max(max_y, cy + half_h)

        return (min_x, min_y, max_x, max_y)

    def get_size(self) -> tuple[float, float]:
        """Compute overall dimensions (width, height) of the diagram.

        Returns:
            Tuple of (width, height).
        """
        if self.custom_width is not None and self.custom_height is not None:
            return (self.custom_width, self.custom_height)

        min_x, min_y, max_x, max_y = self.get_bounds()
        w = max_x - min_x + self.margin * 2.0
        h = max_y - min_y + self.margin * 2.0

        if self.custom_width is not None:
            w = self.custom_width
        if self.custom_height is not None:
            h = self.custom_height

        return (max(w, 10.0), max(h, 10.0))

    @validate_call
    def draw(self, xy: tuple[float, float] = (0.0, 0.0), *, scale: PosFloat = 1.0) -> None:
        """Render the complete class diagram onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y).
            scale: Proportional scale factor anchored at xy.
        """
        with transform(origin=xy, scale=scale):
            _renderer_module.draw_class_diagram(self, xy)
