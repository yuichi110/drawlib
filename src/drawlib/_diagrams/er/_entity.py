# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Entity model for ER diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Union

from drawlib._diagrams.er._relationship import Relationship
from drawlib._diagrams.er._types import Cardinality, ColumnInfo, RoutingType, Side

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.er._diagram import ERDiagram

PaddingType = Union[float, tuple[float, float]]


class Entity:
    """Represents a database table / entity in an ER diagram."""

    def __init__(
        self,
        name: str,
        width: float = 25.0,
        height: float | None = None,
        size: tuple[float, float] | None = None,
        header_height: float = 4.0,
        row_height: float = 3.2,
        style: Style | None = None,
        header_style: Style | None = None,
    ) -> None:
        """Initialize Entity.

        Args:
            name: Table / Entity name.
            width: Width of the entity box (default: 25.0).
            height: Optional fixed height of the entity box. If provided and larger than content,
                extra space is left blank. If None, height auto-fits all columns.
            size: Optional shorthand tuple (width, height) overriding width and height arguments.
            header_height: Height of the header section (default: 4.0).
            row_height: Height of each column row (default: 3.2).
            style: Optional Style for the main entity box and border.
            header_style: Optional Style for the entity header background and text.
        """
        if size is not None:
            self.width = float(size[0])
            self.height = float(size[1])
        else:
            self.width = float(width)
            self.height = float(height) if height is not None else None

        self.name = name
        self.header_height = float(header_height)
        self.row_height = float(row_height)
        self.style = style
        self.header_style = header_style

        self.columns: list[ColumnInfo] = []
        self._local_xy: tuple[float, float] = (0.0, 0.0)
        self._diagram: ERDiagram | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get relative center coordinate (cx, cy) of the entity."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get center coordinate (cx, cy) of the entity."""
        return self._local_xy

    @property
    def effective_height(self) -> float:
        """Get the actual rendered height of the entity."""
        content_height = self.header_height + max(len(self.columns), 1) * self.row_height
        if self.height is not None:
            return max(self.height, content_height)
        return content_height

    def add_column(
        self,
        name: str,
        type: str = "",
        pk: bool = False,
        fk: bool = False,
        nullable: bool = True,
    ) -> Entity:
        """Add a column to the entity.

        Args:
            name: Column name.
            type: Column data type (e.g. 'INT', 'VARCHAR(255)').
            pk: Whether column is Primary Key.
            fk: Whether column is Foreign Key.
            nullable: Whether column is nullable.

        Returns:
            Entity: self for chaining.
        """
        col = ColumnInfo(
            name=name,
            type=type,
            pk=pk,
            fk=fk,
            nullable=nullable,
        )
        self.columns.append(col)
        return self

    def add_columns(
        self,
        columns: Sequence[Union[Sequence[Any], ColumnInfo]],
    ) -> Entity:
        """Add multiple columns in batch.

        Args:
            columns: Sequence of ColumnInfo or tuples (name, [type, pk, fk, nullable]).

        Returns:
            Entity: self for chaining.
        """
        for item in columns:
            if isinstance(item, ColumnInfo):
                self.columns.append(item)
            else:
                name = str(item[0])
                type_ = str(item[1]) if len(item) > 1 else ""
                pk = bool(item[2]) if len(item) > 2 else False
                fk = bool(item[3]) if len(item) > 3 else False
                nullable = bool(item[4]) if len(item) > 4 else True
                self.add_column(name=name, type=type_, pk=pk, fk=fk, nullable=nullable)
        return self

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get visual bounding box [min_x, min_y, max_x, max_y] relative to entity center (0, 0).

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        half_w = self.width / 2.0
        half_h = self.effective_height / 2.0
        return (-half_w, -half_h, half_w, half_h)

    def get_anchor(self, side: Side, column_name: str | None = None) -> tuple[float, float]:
        """Get anchor coordinate on the entity boundary or column row.

        Args:
            side: Attachment side ("left", "right", "top", "bottom", "auto").
            column_name: Optional column name for anchoring to a specific row.

        Returns:
            Absolute or diagram-local coordinate (x, y) for attachment.
        """
        cx, cy = self._local_xy
        w = self.width
        h = self.effective_height
        half_w = w / 2.0
        half_h = h / 2.0

        if side == "top":
            return (cx, cy + half_h)
        if side == "bottom":
            return (cx, cy - half_h)

        # For left or right with column_name
        target_y = cy
        if column_name is not None and (side in {"left", "right", "auto"}):
            for idx, col in enumerate(self.columns):
                if col.name == column_name:
                    top_y = cy + half_h
                    row_top_y = top_y - self.header_height - idx * self.row_height
                    target_y = row_top_y - self.row_height / 2.0
                    break

        if side == "left":
            return (cx - half_w, target_y)
        if side == "right":
            return (cx + half_w, target_y)

        # "auto" fallback defaults to center
        return (cx, target_y)

    def connect(
        self,
        target: Entity,
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
        """Connect this entity to a target entity.

        Args:
            target: Target Entity to connect to.
            cardinality: Relationship multiplicity ("1:*", "1:1", "1:1..*", "1:0..1", "0..1:1", "0..1:*", "*:*").
            start_side: Attachment side on start entity ("left", "right", "top", "bottom", "auto").
            end_side: Attachment side on end entity ("left", "right", "top", "bottom", "auto").
            start_column: Optional column name in start entity.
            end_column: Optional column name in end entity.
            label: Optional relationship label.
            style: Optional Style for the line.
            routing: Path routing strategy ("orthogonal" or "direct").
            padding: Gap distance between entity and line ends.

        Returns:
            Relationship: Newly created relationship object.
        """
        rel = Relationship(
            start=self,
            end=target,
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
        if self._diagram is not None:
            self._diagram.add_relationship(rel)
        elif target._diagram is not None:
            target._diagram.add_relationship(rel)
        return rel
