# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.diagrams.class_diagram."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.class_diagram import (
    AttributeInfo,
    ClassDiagram,
    ClassNode,
    ClassRelationship,
    MethodInfo,
    RelationshipType,
    Side,
)


class TestClassNode:
    """Unit tests for ClassNode model."""

    def test_class_node_initialization(self) -> None:
        """Verify default initialization of ClassNode."""
        node = ClassNode(name="User")
        assert node.name == "User"
        assert node.stereotype == ""
        assert node.is_abstract is False
        assert node.width == 28.0
        assert node.height is None
        assert node.header_height == 5.2
        assert node.row_height == 3.2
        assert len(node.attributes) == 0
        assert len(node.methods) == 0
        assert node.xy == (0.0, 0.0)
        assert node.center == (0.0, 0.0)

    def test_class_node_stereotype_initialization(self) -> None:
        """Verify header height adjustment when stereotype is present."""
        node = ClassNode(name="Payable", stereotype="interface")
        assert node.stereotype == "interface"
        assert node.header_height == 6.5

    def test_class_node_size_shorthand(self) -> None:
        """Verify size tuple shorthand."""
        node = ClassNode(name="Item", size=(35.0, 45.0))
        assert node.width == 35.0
        assert node.height == 45.0

    def test_add_attribute(self) -> None:
        """Verify adding attributes individually."""
        node = ClassNode(name="Account")
        node.add_attribute("id", type="int", is_public=True)
        node.add_attribute("balance", type="float", is_public=False)
        node.add_attribute("secret", visibility="#")
        node.add_attribute("count", type="int", is_static=True, default_value="0")

        assert len(node.attributes) == 4
        attr0 = node.attributes[0]
        assert attr0.name == "id"
        assert attr0.type == "int"
        assert attr0.symbol == "+"
        assert attr0.display_text == "+ id: int"

        attr1 = node.attributes[1]
        assert attr1.symbol == "-"
        assert attr1.display_text == "- balance: float"

        attr2 = node.attributes[2]
        assert attr2.symbol == "#"

        attr3 = node.attributes[3]
        assert attr3.is_static is True
        assert attr3.display_text == "+ count: int = 0"

    def test_add_attributes_batch(self) -> None:
        """Verify batch adding attributes from tuples and AttributeInfo."""
        node = ClassNode(name="Order")
        node.add_attributes([
            ("order_id", "str", True),
            ("total", "float", False),
            AttributeInfo(name="created_at", type="datetime", is_public=True),
        ])
        assert len(node.attributes) == 3
        assert node.attributes[0].name == "order_id"
        assert node.attributes[0].symbol == "+"
        assert node.attributes[1].symbol == "-"
        assert node.attributes[2].name == "created_at"

    def test_add_method(self) -> None:
        """Verify adding methods individually."""
        node = ClassNode(name="Service")
        node.add_method("start", return_type="void", is_public=True)
        node.add_method("stop()", return_type="bool", is_public=False)
        node.add_method("reset", params="hard: bool = False", return_type="void")
        node.add_method("create", params="config: dict", return_type="Service", is_static=True)
        node.add_method("execute", return_type="void", is_abstract=True)

        assert len(node.methods) == 5
        m0 = node.methods[0]
        assert m0.display_text == "+ start(): void"
        m1 = node.methods[1]
        assert m1.display_text == "- stop(): bool"
        m2 = node.methods[2]
        assert m2.display_text == "+ reset(hard: bool = False): void"
        m3 = node.methods[3]
        assert m3.is_static is True
        assert m3.display_text == "+ create(config: dict): Service"
        m4 = node.methods[4]
        assert m4.is_abstract is True

    def test_add_methods_batch(self) -> None:
        """Verify batch adding methods from tuples and MethodInfo."""
        node = ClassNode(name="Controller")
        node.add_methods([
            ("index", "Response", ""),
            ("save", "bool", "entity: Any", False),
            MethodInfo(name="delete", params="id: int", return_type="void"),
        ])
        assert len(node.methods) == 3
        assert node.methods[0].name == "index"
        assert node.methods[1].symbol == "-"
        assert node.methods[2].name == "delete"

    def test_effective_height(self) -> None:
        """Verify effective height calculation with attributes and methods."""
        node = ClassNode(name="Simple", header_height=5.0, row_height=3.0)
        # Empty class -> header (5.0) + minimal body (3.0) = 8.0
        assert node.effective_height == 8.0

        node.add_attribute("x", "int")
        node.add_attribute("y", "int")
        # 5.0 + (2 * 3.0 + 1.5) = 12.5
        assert node.effective_height == 12.5

        node.add_method("move", params="dx: int, dy: int")
        # 5.0 + (2 * 3.0 + 1.5) + (1 * 3.0 + 1.5) = 17.0
        assert node.effective_height == 17.0

        # Fixed height larger than content
        node_fixed = ClassNode(name="Fixed", height=30.0, header_height=5.0)
        assert node_fixed.effective_height == 30.0

    def test_get_bounds(self) -> None:
        """Verify bounding box relative to center."""
        node = ClassNode(name="Box", width=20.0, height=10.0)
        min_x, min_y, max_x, max_y = node.get_bounds()
        assert min_x == -10.0
        assert min_y == -5.0
        assert max_x == 10.0
        assert max_y == 5.0

    def test_get_anchor(self) -> None:
        """Verify anchor coordinates on card boundary."""
        node = ClassNode(name="Card", width=20.0, height=10.0)
        node._local_xy = (40.0, 60.0)

        assert node.get_anchor("top") == (40.0, 65.0)
        assert node.get_anchor("bottom") == (40.0, 55.0)
        assert node.get_anchor("left") == (30.0, 60.0)
        assert node.get_anchor("right") == (50.0, 60.0)


class TestClassRelationship:
    """Unit tests for ClassRelationship model and verb methods."""

    def test_valid_relationship(self) -> None:
        """Verify valid relationship creation."""
        c1 = ClassNode("Parent")
        c2 = ClassNode("Child")
        rel = ClassRelationship(
            start=c2,
            end=c1,
            relationship_type="inheritance",
            start_side="top",
            end_side="bottom",
        )
        assert rel.start is c2
        assert rel.end is c1
        assert rel.relationship_type == "inheritance"
        assert rel.start_side == "top"
        assert rel.end_side == "bottom"

    def test_invalid_type(self) -> None:
        """Verify ValueError on invalid relationship type."""
        c1 = ClassNode("A")
        c2 = ClassNode("B")
        with pytest.raises(ValueError, match="Invalid relationship_type"):
            ClassRelationship(start=c1, end=c2, relationship_type="unknown")  # type: ignore

    def test_invalid_side(self) -> None:
        """Verify ValueError on invalid side."""
        c1 = ClassNode("A")
        c2 = ClassNode("B")
        with pytest.raises(ValueError, match="Invalid start_side"):
            ClassRelationship(start=c1, end=c2, start_side="diagonal")  # type: ignore
        with pytest.raises(ValueError, match="Invalid end_side"):
            ClassRelationship(start=c1, end=c2, end_side="diagonal")  # type: ignore

    def test_invalid_routing(self) -> None:
        """Verify ValueError on invalid routing."""
        c1 = ClassNode("A")
        c2 = ClassNode("B")
        with pytest.raises(ValueError, match="Invalid routing"):
            ClassRelationship(start=c1, end=c2, routing="curved")  # type: ignore

    def test_verb_methods(self) -> None:
        """Verify verb methods create correct relationship types."""
        c_animal = ClassNode("Animal")
        c_dog = ClassNode("Dog")
        c_runnable = ClassNode("Runnable", stereotype="interface")
        c_car = ClassNode("Car")
        c_engine = ClassNode("Engine")
        c_dept = ClassNode("Department")
        c_emp = ClassNode("Employee")
        c_doc = ClassNode("Document")
        c_printer = ClassNode("Printer")

        rel_inherit = c_dog.inherit(c_animal)
        assert rel_inherit.relationship_type == "inheritance"

        rel_realize = c_dog.realize(c_runnable)
        assert rel_realize.relationship_type == "realization"

        rel_comp = c_car.composite(c_engine, start_multiplicity="1", end_multiplicity="1")
        assert rel_comp.relationship_type == "composition"
        assert rel_comp.start_multiplicity == "1"
        assert rel_comp.end_multiplicity == "1"

        rel_agg = c_dept.aggregate(c_emp, start_multiplicity="1", end_multiplicity="*")
        assert rel_agg.relationship_type == "aggregation"

        rel_assoc = c_dog.associate(c_car, label="rides_in")
        assert rel_assoc.relationship_type == "association"
        assert rel_assoc.label == "rides_in"

        rel_dep = c_doc.depend(c_printer, label="prints_with")
        assert rel_dep.relationship_type == "dependency"
        assert rel_dep.directed is True


class TestClassDiagram:
    """Unit tests for ClassDiagram container."""

    def test_diagram_add_and_connect(self) -> None:
        """Verify adding classes and relationships."""
        cd = ClassDiagram(title="UML Diagram")
        c1 = cd.add(ClassNode("User"), xy=(20.0, 50.0))
        c2 = cd.add(ClassNode("Profile"), xy=(60.0, 50.0))

        assert len(cd.classes) == 2
        assert c1.xy == (20.0, 50.0)
        assert c2.xy == (60.0, 50.0)

        rel = c1.associate(c2, label="has_profile")
        assert len(cd.relationships) == 1
        assert rel.start is c1
        assert rel.end is c2
        assert rel.label == "has_profile"

    def test_get_size(self) -> None:
        """Verify automatic and custom diagram dimensions."""
        cd_fixed = ClassDiagram(width=150.0, height=120.0)
        assert cd_fixed.get_size() == (150.0, 120.0)

        cd_auto = ClassDiagram(margin=5.0)
        cd_auto.add(ClassNode("NodeA", width=20.0, height=10.0), xy=(20.0, 20.0))
        cd_auto.add(ClassNode("NodeB", width=20.0, height=10.0), xy=(60.0, 60.0))
        # bounds: min_x = 20 - 10 = 10, max_x = 60 + 10 = 70. span_x = 60 (+ 2 * 5.0 = 70.0)
        # bounds: min_y = 20 - 5 = 15, max_y = 60 + 5 = 65. span_y = 50 (+ 2 * 5.0 = 60.0)
        w, h = cd_auto.get_size()
        assert w == 70.0
        assert h == 60.0


class TestClassDiagramRendering:
    """Integration tests verifying class diagram canvas rendering."""

    def test_render_basic_diagram(self) -> None:
        """Verify basic class diagram rendering and image export."""
        canvas.initialize()

        cd = ClassDiagram(title="E-Commerce Domain Model")
        user = cd.add(ClassNode(name="User", width=28.0), xy=(25.0, 65.0))
        user.add_attribute("id", type="int", is_public=True)
        user.add_attribute("email", type="str", is_public=True)
        user.add_attribute("password_hash", type="str", is_public=False)
        user.add_method("login", params="password: str", return_type="bool")
        user.add_method("logout", return_type="void")

        customer = cd.add(ClassNode(name="Customer", width=28.0), xy=(25.0, 25.0))
        customer.add_attribute("shipping_address", type="str")
        customer.add_method("place_order", return_type="Order")

        order = cd.add(ClassNode(name="Order", width=28.0), xy=(75.0, 25.0))
        order.add_attribute("order_id", type="str")
        order.add_attribute("total", type="float")
        order.add_method("calculate_total", return_type="float")

        # Customer inherits User
        customer.inherit(user, start_side="top", end_side="bottom")

        # Customer composes Order
        customer.composite(
            order,
            start_side="right",
            end_side="left",
            start_multiplicity="1",
            end_multiplicity="*",
            label="places",
        )

        cd.draw(xy=(0.0, 0.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_cd_basic.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_all_relationships_gallery(self) -> None:
        """Verify rendering all 6 UML relationship types."""
        canvas.initialize()

        cd = ClassDiagram(title="UML Relationship Gallery")
        types: list[RelationshipType] = [
            "inheritance",
            "realization",
            "composition",
            "aggregation",
            "association",
            "dependency",
        ]

        for idx, rel_type in enumerate(types):
            y = 85.0 - idx * 13.0
            c_src = cd.add(ClassNode(name=f"Src_{idx}", width=20.0, height=7.0), xy=(25.0, y))
            c_tgt = cd.add(ClassNode(name=f"Tgt_{idx}", width=20.0, height=7.0), xy=(75.0, y))

            c_src.connect(
                c_tgt,
                relationship_type=rel_type,
                start_side="right",
                end_side="left",
                label=rel_type,
                start_multiplicity="1" if rel_type in {"composition", "aggregation"} else "",
                end_multiplicity="*" if rel_type in {"composition", "aggregation"} else "",
            )

        cd.draw()

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_rel_gallery.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles_and_direct_routing(self) -> None:
        """Verify rendering with custom styles, abstract classes, and direct routing."""
        canvas.initialize()

        cd = ClassDiagram(
            title="Payment Processing",
            style=Style(fill_color=Colors.White),
        )

        processor = cd.add(
            ClassNode(
                name="PaymentProcessor",
                stereotype="interface",
                width=30.0,
                header_style=Style(fill_color=Colors.Teal, text_color=Colors.White),
            ),
            xy=(50.0, 75.0),
        )
        processor.add_method("process", params="amount: float", return_type="bool")

        stripe = cd.add(
            ClassNode(
                name="StripePayment",
                width=26.0,
                header_style=Style(fill_color=Colors.Navy, text_color=Colors.White),
            ),
            xy=(25.0, 30.0),
        )
        stripe.add_attribute("api_key", type="str", is_public=False)
        stripe.add_method("process", params="amount: float", return_type="bool")

        paypal = cd.add(
            ClassNode(
                name="PayPalPayment",
                width=26.0,
                header_style=Style(fill_color=Colors.Blue, text_color=Colors.White),
            ),
            xy=(75.0, 30.0),
        )
        paypal.add_attribute("client_id", type="str", is_public=False)
        paypal.add_method("process", params="amount: float", return_type="bool")

        # Realization relationships with direct routing
        stripe.realize(
            processor,
            routing="direct",
            style=Style(line_color=Colors.Navy, line_width=2.0),
            padding=1.0,
        )
        paypal.realize(
            processor,
            routing="direct",
            style=Style(line_color=Colors.Blue, line_width=2.0),
            padding=1.0,
        )

        cd.draw()

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_styled_cd.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
