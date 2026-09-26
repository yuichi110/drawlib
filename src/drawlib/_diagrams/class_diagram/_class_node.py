# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""ClassNode model for UML Class diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Union

from drawlib._diagrams.class_diagram._relationship import ClassRelationship
from drawlib._diagrams.class_diagram._types import (
    AttributeInfo,
    MethodInfo,
    RelationshipType,
    RoutingType,
    Side,
)

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.class_diagram._diagram import ClassDiagram

PaddingType = Union[float, tuple[float, float]]


class ClassNode:
    """Represents a class, interface, or abstract class in a UML Class diagram."""

    def __init__(
        self,
        name: str,
        stereotype: str = "",
        is_abstract: bool = False,
        width: float = 28.0,
        height: float | None = None,
        size: tuple[float, float] | None = None,
        header_height: float | None = None,
        row_height: float = 3.2,
        style: Style | None = None,
        header_style: Style | None = None,
    ) -> None:
        """Initialize ClassNode.

        Args:
            name: Class name.
            stereotype: Optional UML stereotype (e.g. 'interface', 'abstract', 'enumeration').
            is_abstract: Whether the class is abstract (renders class name in italic).
            width: Width of the class card (default: 28.0).
            height: Optional fixed height of the class card. If None, auto-calculated from content.
            size: Optional shorthand tuple (width, height) overriding width and height arguments.
            header_height: Height of the header section. If None, automatically computed based on stereotype.
            row_height: Height of each attribute and method row (default: 3.2).
            style: Optional Style overriding the main box border and body fill.
            header_style: Optional Style overriding the header compartment background and text.
        """
        if size is not None:
            self.width = float(size[0])
            self.height = float(size[1])
        else:
            self.width = float(width)
            self.height = float(height) if height is not None else None

        self.name = name
        self.stereotype = stereotype
        self.is_abstract = is_abstract
        self.header_height = float(header_height) if header_height is not None else (6.5 if stereotype else 5.2)
        self.row_height = float(row_height)
        self.style = style
        self.header_style = header_style

        self.attributes: list[AttributeInfo] = []
        self.methods: list[MethodInfo] = []

        self._local_xy: tuple[float, float] = (0.0, 0.0)
        self._diagram: ClassDiagram | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get relative center coordinate (cx, cy) of the class card."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get relative center coordinate (cx, cy) of the class card."""
        return self._local_xy

    @property
    def effective_height(self) -> float:
        """Get the actual rendered height of the class card."""
        attr_h = len(self.attributes) * self.row_height + (1.5 if self.attributes else 0.0)
        meth_h = len(self.methods) * self.row_height + (1.5 if self.methods else 0.0)
        content_height = self.header_height + attr_h + meth_h
        if not self.attributes and not self.methods:
            # Minimal body height when only header exists
            content_height += 3.0

        if self.height is not None:
            return max(self.height, content_height)
        return content_height

    def add_attribute(
        self,
        name: str,
        type: str = "",
        is_public: bool = True,
        visibility: str | None = None,
        default_value: str = "",
        is_static: bool = False,
    ) -> ClassNode:
        """Add an attribute / field to the class.

        Args:
            name: Attribute name.
            type: Data type string (e.g. 'int', 'str', 'list[Item]').
            is_public: Whether the attribute is public (True -> '+') or private (False -> '-'). Defaults to True.
            visibility: Optional explicit UML visibility symbol ('+', '-', '#', '~'). Overrides is_public if set.
            default_value: Optional default value string.
            is_static: Whether the attribute is static.

        Returns:
            ClassNode: self for chaining.
        """
        attr = AttributeInfo(
            name=name,
            type=type,
            is_public=is_public,
            visibility=visibility,
            default_value=default_value,
            is_static=is_static,
        )
        self.attributes.append(attr)
        return self

    def add_attributes(
        self,
        attributes: Sequence[Union[Sequence[Any], AttributeInfo]],
    ) -> ClassNode:
        """Add multiple attributes in batch.

        Args:
            attributes: Sequence of AttributeInfo or tuples (name, [type, is_public, visibility, default_value]).

        Returns:
            ClassNode: self for chaining.
        """
        for item in attributes:
            if isinstance(item, AttributeInfo):
                self.attributes.append(item)
            else:
                name = str(item[0])
                type_ = str(item[1]) if len(item) > 1 else ""
                is_public = bool(item[2]) if len(item) > 2 else True
                visibility = str(item[3]) if len(item) > 3 and item[3] is not None else None
                default_val = str(item[4]) if len(item) > 4 else ""
                self.add_attribute(
                    name=name,
                    type=type_,
                    is_public=is_public,
                    visibility=visibility,
                    default_value=default_val,
                )
        return self

    def add_method(
        self,
        name: str,
        params: str = "",
        return_type: str = "",
        is_public: bool = True,
        visibility: str | None = None,
        is_static: bool = False,
        is_abstract: bool = False,
    ) -> ClassNode:
        """Add an operation / method to the class.

        Args:
            name: Method name (with or without parentheses).
            params: Parameter signature string.
            return_type: Return type string (e.g. 'bool', 'void').
            is_public: Whether the method is public (True -> '+') or private (False -> '-'). Defaults to True.
            visibility: Optional explicit UML visibility symbol ('+', '-', '#', '~'). Overrides is_public if set.
            is_static: Whether the method is static.
            is_abstract: Whether the method is abstract.

        Returns:
            ClassNode: self for chaining.
        """
        meth = MethodInfo(
            name=name,
            params=params,
            return_type=return_type,
            is_public=is_public,
            visibility=visibility,
            is_static=is_static,
            is_abstract=is_abstract,
        )
        self.methods.append(meth)
        return self

    def add_methods(
        self,
        methods: Sequence[Union[Sequence[Any], MethodInfo]],
    ) -> ClassNode:
        """Add multiple methods in batch.

        Args:
            methods: Sequence of MethodInfo or tuples (name, [return_type, params, is_public, visibility]).

        Returns:
            ClassNode: self for chaining.
        """
        for item in methods:
            if isinstance(item, MethodInfo):
                self.methods.append(item)
            else:
                name = str(item[0])
                return_type = str(item[1]) if len(item) > 1 else ""
                params = str(item[2]) if len(item) > 2 else ""
                is_public = bool(item[3]) if len(item) > 3 else True
                visibility = str(item[4]) if len(item) > 4 and item[4] is not None else None
                self.add_method(
                    name=name,
                    params=params,
                    return_type=return_type,
                    is_public=is_public,
                    visibility=visibility,
                )
        return self

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get visual bounding box [min_x, min_y, max_x, max_y] relative to class center (0, 0).

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        half_w = self.width / 2.0
        half_h = self.effective_height / 2.0
        return (-half_w, -half_h, half_w, half_h)

    def get_anchor(self, side: Side) -> tuple[float, float]:
        """Get anchor coordinate on the class card boundary.

        Args:
            side: Attachment side ('left', 'right', 'top', 'bottom', 'auto').

        Returns:
            Relative coordinate (x, y) on the class boundary.
        """
        cx, cy = self._local_xy
        half_w = self.width / 2.0
        half_h = self.effective_height / 2.0

        if side == "top":
            return (cx, cy + half_h)
        if side == "bottom":
            return (cx, cy - half_h)
        if side == "left":
            return (cx - half_w, cy)
        if side == "right":
            return (cx + half_w, cy)
        return (cx, cy)

    def inherit(
        self,
        target: ClassNode,
        start_side: Side = "auto",
        end_side: Side = "auto",
        label: str = "",
        style: Style | None = None,
        routing: RoutingType = "orthogonal",
        padding: PaddingType = 0.0,
    ) -> ClassRelationship:
        """Create an inheritance (generalization) relationship from self to target superclass."""
        return self.connect(
            target=target,
            relationship_type="inheritance",
            start_side=start_side,
            end_side=end_side,
            label=label,
            style=style,
            routing=routing,
            padding=padding,
        )

    inherits = inherit

    def realize(
        self,
        target: ClassNode,
        start_side: Side = "auto",
        end_side: Side = "auto",
        label: str = "",
        style: Style | None = None,
        routing: RoutingType = "orthogonal",
        padding: PaddingType = 0.0,
    ) -> ClassRelationship:
        """Create an implementation (realization) relationship from self to target interface."""
        return self.connect(
            target=target,
            relationship_type="realization",
            start_side=start_side,
            end_side=end_side,
            label=label,
            style=style,
            routing=routing,
            padding=padding,
        )

    realizes = realize

    def composite(
        self,
        target: ClassNode,
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
    ) -> ClassRelationship:
        """Create a composition relationship from whole (self) to part (target)."""
        return self.connect(
            target=target,
            relationship_type="composition",
            start_side=start_side,
            end_side=end_side,
            label=label,
            start_multiplicity=start_multiplicity,
            end_multiplicity=end_multiplicity,
            start_role=start_role,
            end_role=end_role,
            directed=directed,
            style=style,
            routing=routing,
            padding=padding,
        )

    composes = composite

    def aggregate(
        self,
        target: ClassNode,
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
    ) -> ClassRelationship:
        """Create an aggregation relationship from whole (self) to part (target)."""
        return self.connect(
            target=target,
            relationship_type="aggregation",
            start_side=start_side,
            end_side=end_side,
            label=label,
            start_multiplicity=start_multiplicity,
            end_multiplicity=end_multiplicity,
            start_role=start_role,
            end_role=end_role,
            directed=directed,
            style=style,
            routing=routing,
            padding=padding,
        )

    aggregates = aggregate

    def associate(
        self,
        target: ClassNode,
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
    ) -> ClassRelationship:
        """Create an association relationship between self and target."""
        return self.connect(
            target=target,
            relationship_type="association",
            start_side=start_side,
            end_side=end_side,
            label=label,
            start_multiplicity=start_multiplicity,
            end_multiplicity=end_multiplicity,
            start_role=start_role,
            end_role=end_role,
            directed=directed,
            style=style,
            routing=routing,
            padding=padding,
        )

    associates = associate

    def depend(
        self,
        target: ClassNode,
        start_side: Side = "auto",
        end_side: Side = "auto",
        label: str = "",
        start_multiplicity: str = "",
        end_multiplicity: str = "",
        start_role: str = "",
        end_role: str = "",
        style: Style | None = None,
        routing: RoutingType = "orthogonal",
        padding: PaddingType = 0.0,
    ) -> ClassRelationship:
        """Create a dependency relationship from self to target."""
        return self.connect(
            target=target,
            relationship_type="dependency",
            start_side=start_side,
            end_side=end_side,
            label=label,
            start_multiplicity=start_multiplicity,
            end_multiplicity=end_multiplicity,
            start_role=start_role,
            end_role=end_role,
            directed=True,
            style=style,
            routing=routing,
            padding=padding,
        )

    depends_on = depend

    def connect(
        self,
        target: ClassNode,
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
    ) -> ClassRelationship:
        """Connect this class to a target class."""
        rel = ClassRelationship(
            start=self,
            end=target,
            relationship_type=relationship_type,
            start_side=start_side,
            end_side=end_side,
            label=label,
            start_multiplicity=start_multiplicity,
            end_multiplicity=end_multiplicity,
            start_role=start_role,
            end_role=end_role,
            directed=directed,
            style=style,
            routing=routing,
            padding=padding,
        )
        if self._diagram is not None:
            self._diagram.add_relationship(rel)
        elif target._diagram is not None:
            target._diagram.add_relationship(rel)
        return rel
