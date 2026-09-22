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

import drawlib._diagrams.class_diagram._renderer as _renderer_module
from drawlib._diagrams.class_diagram._class_node import ClassNode
from drawlib._diagrams.class_diagram._relationship import ClassRelationship

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class ClassDiagram:
    """Top-level container managing classes, relationships, and layout for Class diagrams."""

    def __init__(
        self,
        title: str = "",
        style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
        margin: float = 5.0,
    ) -> None:
        """Initialize ClassDiagram.

        Args:
            title: Optional title displayed above the diagram.
            style: Optional Style overriding diagram background.
            width: Optional fixed canvas width. If None, auto-calculated from content.
            height: Optional fixed canvas height. If None, auto-calculated from content.
            margin: Outer margin padding surrounding all classes (default: 5.0).
        """
        self.title = title
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
    ) -> ClassNode:
        """Add a ClassNode to the diagram at the specified relative center coordinate.

        Args:
            class_node: ClassNode to register.
            xy: Center placement coordinate (cx, cy).

        Returns:
            ClassNode: The added class node for chaining.
        """
        class_node._local_xy = (float(xy[0]), float(xy[1]))
        class_node._diagram = self
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

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render the complete class diagram onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y).
        """
        _renderer_module.draw_class_diagram(self, xy)
