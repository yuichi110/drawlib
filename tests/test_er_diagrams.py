# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.diagrams.er."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.er import Cardinality, ColumnInfo, Entity, ERDiagram, Relationship, Side


class TestEntity:
    """Unit tests for Entity model."""

    def test_entity_initialization(self) -> None:
        """Verify entity default initialization."""
        ent = Entity(name="users")
        assert ent.name == "users"
        assert ent.width == 25.0
        assert ent.height is None
        assert ent.header_height == 4.0
        assert ent.row_height == 3.2
        assert len(ent.columns) == 0
        assert ent.xy == (0.0, 0.0)
        assert ent.center == (0.0, 0.0)

    def test_entity_size_shorthand(self) -> None:
        """Verify size tuple shorthand."""
        ent = Entity(name="orders", size=(30.0, 40.0))
        assert ent.width == 30.0
        assert ent.height == 40.0

    def test_add_column(self) -> None:
        """Verify adding columns individually."""
        ent = Entity(name="products")
        ent.add_column("id", type="INT", pk=True, nullable=False)
        ent.add_column("name", type="VARCHAR(100)", nullable=False)
        ent.add_column("category_id", type="INT", fk=True)

        assert len(ent.columns) == 3
        col0 = ent.columns[0]
        assert col0.name == "id"
        assert col0.type == "INT"
        assert col0.pk is True
        assert col0.fk is False
        assert col0.nullable is False

        col2 = ent.columns[2]
        assert col2.name == "category_id"
        assert col2.fk is True

    def test_add_columns_batch(self) -> None:
        """Verify batch adding columns from tuples and ColumnInfo."""
        ent = Entity(name="logs")
        ent.add_columns([
            ("id", "BIGINT", True),
            ("message", "TEXT", False, False, False),
            ColumnInfo(name="level", type="VARCHAR(10)", pk=False, fk=False, nullable=True),
        ])
        assert len(ent.columns) == 3
        assert ent.columns[0].pk is True
        assert ent.columns[1].nullable is False
        assert ent.columns[2].name == "level"

    def test_effective_height(self) -> None:
        """Verify effective height calculation with and without fixed height."""
        ent = Entity(name="users", header_height=4.0, row_height=3.0)
        # Empty entity content height = header (4.0) + max(0, 1) * 3.0 = 7.0
        assert ent.effective_height == 7.0

        ent.add_column("id")
        ent.add_column("email")
        # 4.0 + 2 * 3.0 = 10.0
        assert ent.effective_height == 10.0

        # Fixed height larger than content -> leaves blank space
        ent_fixed = Entity(name="users", height=20.0, header_height=4.0, row_height=3.0)
        ent_fixed.add_column("id")
        assert ent_fixed.effective_height == 20.0

        # Fixed height smaller than content -> expands to fit content
        ent_small = Entity(name="users", height=5.0, header_height=4.0, row_height=3.0)
        ent_small.add_column("id")
        ent_small.add_column("email")
        assert ent_small.effective_height == 10.0

    def test_get_bounds(self) -> None:
        """Verify bounding box relative to center."""
        ent = Entity(name="users", width=20.0, height=10.0)
        min_x, min_y, max_x, max_y = ent.get_bounds()
        assert min_x == -10.0
        assert min_y == -5.0
        assert max_x == 10.0
        assert max_y == 5.0

    def test_get_anchor(self) -> None:
        """Verify anchor coordinates on entity edges and columns."""
        ent = Entity(name="users", width=20.0, height=10.0, header_height=4.0, row_height=3.0)
        ent._local_xy = (50.0, 50.0)
        ent.add_column("id")
        ent.add_column("email")

        # Top anchor: cx, cy + half_h = (50.0, 55.0)
        assert ent.get_anchor("top") == (50.0, 55.0)

        # Bottom anchor: cx, cy - half_h = (50.0, 45.0)
        assert ent.get_anchor("bottom") == (50.0, 45.0)

        # Left / Right without column
        assert ent.get_anchor("left") == (40.0, 50.0)
        assert ent.get_anchor("right") == (60.0, 50.0)

        # Left with column anchor
        # top_y = 55.0, row 0 (id) center y = 55.0 - 4.0 - 1.5 = 49.5
        anchor_id = ent.get_anchor("right", column_name="id")
        assert anchor_id == (60.0, 49.5)


class TestRelationship:
    """Unit tests for Relationship model."""

    def test_valid_relationship(self) -> None:
        """Verify valid relationship creation."""
        e1 = Entity("users")
        e2 = Entity("orders")
        rel = Relationship(start=e1, end=e2, cardinality="1:*", start_side="right", end_side="left")
        assert rel.start is e1
        assert rel.end is e2
        assert rel.cardinality == "1:*"
        assert rel.start_side == "right"
        assert rel.end_side == "left"

    def test_invalid_cardinality(self) -> None:
        """Verify ValueError on invalid cardinality."""
        e1 = Entity("a")
        e2 = Entity("b")
        with pytest.raises(ValueError, match="Invalid cardinality"):
            Relationship(
                start=e1,
                end=e2,
                cardinality="invalid",  # type: ignore
            )

    def test_invalid_side(self) -> None:
        """Verify ValueError on invalid side."""
        e1 = Entity("a")
        e2 = Entity("b")
        with pytest.raises(ValueError, match="Invalid start_side"):
            Relationship(
                start=e1,
                end=e2,
                start_side="diagonal",  # type: ignore
            )
        with pytest.raises(ValueError, match="Invalid end_side"):
            Relationship(
                start=e1,
                end=e2,
                end_side="diagonal",  # type: ignore
            )


class TestERDiagram:
    """Unit tests for ERDiagram container."""

    def test_diagram_add_and_connect(self) -> None:
        """Verify adding entities and connecting them."""
        erd = ERDiagram(title="Test Diagram")
        u = Entity("users")
        o = Entity("orders")

        erd.add(u, xy=(20.0, 50.0))
        erd.add(o, xy=(70.0, 50.0))

        assert len(erd.entities) == 2
        assert u.xy == (20.0, 50.0)
        assert o.xy == (70.0, 50.0)

        rel = u.connect(o, cardinality="1:*", label="places")
        assert len(erd.relationships) == 1
        assert rel.start is u
        assert rel.end is o
        assert rel.label == "places"

    def test_get_size(self) -> None:
        """Verify automatic and fixed diagram size."""
        erd_fixed = ERDiagram(width=200.0, height=100.0)
        assert erd_fixed.get_size() == (200.0, 100.0)

        erd_auto = ERDiagram()
        u = Entity("users", width=20.0, height=10.0)
        erd_auto.add(u, xy=(50.0, 50.0))
        # max_x = 50 + 10 = 60 (+10 margin = 70.0)
        # max_y = 50 + 5 = 55 (+10 margin = 65.0)
        w, h = erd_auto.get_size()
        assert w == 70.0
        assert h == 65.0


class TestERDiagramRendering:
    """Integration tests verifying ER diagram canvas rendering."""

    def test_render_basic_diagram(self) -> None:
        """Verify basic ER diagram rendering and image file export."""
        canvas.initialize()

        erd = ERDiagram(title="Customer Order System")
        users = erd.add(Entity(name="users", width=25.0), xy=(25.0, 60.0))
        users.add_column("id", type="INT", pk=True)
        users.add_column("email", type="VARCHAR(255)", nullable=False)
        users.add_column("created_at", type="DATETIME")

        orders = erd.add(Entity(name="orders", width=25.0), xy=(75.0, 60.0))
        orders.add_column("id", type="INT", pk=True)
        orders.add_column("user_id", type="INT", fk=True)
        orders.add_column("order_date", type="DATE")

        users.connect(
            orders,
            cardinality="1:*",
            start_side="right",
            end_side="left",
            start_column="id",
            end_column="user_id",
            label="places",
        )

        erd.draw(xy=(0.0, 0.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_erd_basic.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_all_cardinalities(self) -> None:
        """Verify rendering for all supported IE Crow's foot cardinality notations."""
        canvas.initialize()

        cardinalities: list[Cardinality] = [
            "1:*",
            "1:1",
            "1:1..*",
            "1:0..1",
            "0..1:1",
            "0..1:*",
            "*:*",
        ]

        erd = ERDiagram(title="Cardinalities Gallery")
        for idx, card in enumerate(cardinalities):
            y = 85.0 - idx * 12.0
            e1 = erd.add(Entity(name=f"Src_{idx}", width=18.0, height=8.0), xy=(20.0, y))
            e1.add_column("id", type="INT", pk=True)

            e2 = erd.add(Entity(name=f"Tgt_{idx}", width=18.0, height=8.0), xy=(70.0, y))
            e2.add_column("ref_id", type="INT", fk=True)

            e1.connect(e2, cardinality=card, label=card)

        erd.draw()

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_cardinalities.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_with_custom_styles_and_padding(self) -> None:
        """Verify rendering with custom styles, excess height blank area, and direct routing."""
        canvas.initialize()

        erd = ERDiagram(
            title="Styled ERD",
            style=Style(shape_fill_color=Colors.White),
        )

        # Entity with excess height -> extra space left blank
        authors = erd.add(
            Entity(
                name="authors",
                width=24.0,
                height=25.0,
                header_style=Style(shape_fill_color=Colors.Navy, text_color=Colors.White),
            ),
            xy=(25.0, 50.0),
        )
        authors.add_column("id", type="INT", pk=True)
        authors.add_column("pen_name", type="VARCHAR(100)")

        books = erd.add(
            Entity(
                name="books",
                width=24.0,
                height=25.0,
                header_style=Style(shape_fill_color=Colors.Teal, text_color=Colors.White),
            ),
            xy=(75.0, 50.0),
        )
        books.add_column("id", type="INT", pk=True)
        books.add_column("author_id", type="INT", fk=True)
        books.add_column("title", type="VARCHAR(200)")

        authors.connect(
            books,
            cardinality="1:*",
            start_side="right",
            end_side="left",
            style=Style(line_color=Colors.Navy, line_width=2.0),
            routing="direct",
            padding=1.0,
        )

        erd.draw()

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_styled_erd.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
