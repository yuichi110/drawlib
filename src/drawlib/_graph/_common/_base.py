# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Abstract base class and core contract for declarative graph solvers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from drawlib._graph._common._code_generator import generate_code
from drawlib._graph._common._models import Cluster, Edge, GraphLayout, Node
from drawlib._graph._common._renderer import render_layout
from drawlib.fonts import Font
from drawlib.styles import Style, Styles


class BaseGraph(ABC):
    """Abstract base class for all declarative graph solvers.

    Provides node/edge/cluster registration methods and uniform interfaces
    for calculation (`calc`), direct drawing (`draw`), and code export (`export_code`).
    """

    def __init__(
        self,
        *,
        default_node_style: Style | None = None,
        default_node_text_style: Style | None = None,
        default_edge_style: Style | None = None,
        default_edge_text_style: Style | None = None,
        default_node_width: float = 20.0,
        default_node_height: float = 12.0,
    ) -> None:
        """Initialize base graph properties and defaults.

        Args:
            default_node_style: Default style applied to nodes without explicit styles.
            default_node_text_style: Default style applied to node labels. If None,
                relies on the node style's configured text styling.
            default_edge_style: Default style applied to connecting edges.
            default_edge_text_style: Default style applied to edge annotation labels.
            default_node_width: Default width for rectangular/rounded nodes.
            default_node_height: Default height for rectangular/rounded nodes.
        """
        self.default_node_style: Style = default_node_style or Styles.PrimaryFlat
        self.default_node_text_style: Style | None = default_node_text_style
        self.default_edge_style: Style = default_edge_style or Styles.DarkBold
        self.default_edge_text_style: Style = default_edge_text_style or Style(
            text_size=10,
            text_color=(50, 58, 72, 1.0),
            text_font=Font.SANSSERIF_BOLD,
            text_bg_fill_color=(255, 255, 255, 0.9),
        )
        self.default_node_width: float = default_node_width
        self.default_node_height: float = default_node_height

        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []
        self._clusters: dict[str, Cluster] = {}

    def node(
        self,
        id: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        shape: Literal["rectangle", "circle", "rounded_rectangle"] = "rectangle",
        icon: str | None = None,
        width: float | None = None,
        height: float | None = None,
        ring: int | None = None,
        row: int | None = None,
        col: int | None = None,
        layer: int | None = None,
        group: str | None = None,
        subgroup: str | None = None,
    ) -> Node:
        """Register a node in the graph.

        Args:
            id: Unique identifier string for the node.
            label: Text label displayed inside/beside the node. Defaults to id if None.
            style: Shape styling for this node.
            text_style: Text styling for the node label.
            shape: Shape geometry ("rectangle", "circle", "rounded_rectangle").
            icon: Optional icon name or path.
            width: Custom width for this node.
            height: Custom height for this node.
            ring: Optional concentric ring number (for radial layouts).
            row: Optional row index (for grid layouts).
            col: Optional column index (for grid layouts).
            layer: Optional layer/rank index (for layered layouts).
            group: Optional container/group ID (for architecture layouts).
            subgroup: Optional nested subgroup ID (for architecture layouts).

        Returns:
            The registered Node object.

        Raises:
            ValueError: If a node with the same id is already registered.
        """
        if id in self._nodes:
            raise ValueError(f"Node '{id}' is already registered in the graph.")

        n = Node(
            id=id,
            label=label if label is not None else id,
            style=style,
            text_style=text_style,
            shape=shape,
            icon=icon,
            width=width,
            height=height,
            ring=ring,
            row=row,
            col=col,
            layer=layer,
            group=group,
            subgroup=subgroup,
        )
        self._nodes[id] = n
        return n

    def edge(
        self,
        src: str,
        dst: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        arrow_head: Literal["->", "<-", "<->", "-"] = "->",
        line_style: Literal["solid", "dashed", "dotted"] | None = None,
    ) -> Edge:
        """Register a directed or undirected connection between two nodes.

        Args:
            src: Source node ID.
            dst: Destination node ID.
            label: Annotation text along the edge.
            style: Line styling for the connection.
            text_style: Text styling for the edge label.
            arrow_head: Arrowhead decoration ("->", "<-", "<->", "-").
            line_style: Stroke style ("solid", "dashed", "dotted").

        Returns:
            The registered Edge object.
        """
        e = Edge(
            src=src,
            dst=dst,
            label=label,
            style=style,
            text_style=text_style,
            arrow_head=arrow_head,
            line_style=line_style,
        )
        self._edges.append(e)
        return e

    def cluster(
        self,
        id: str,
        nodes: list[str],
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        padding: float = 4.0,
        parent: str | None = None,
        order: int | None = None,
        pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
    ) -> Cluster:
        """Register a grouping boundary surrounding a subset of nodes.

        Args:
            id: Unique identifier string for the cluster.
            nodes: List of node IDs contained within this cluster.
            label: Text title for the cluster boundary.
            style: Container border and fill style (defaults to Styles.MutedDashed).
            text_style: Text style for the cluster label.
            padding: Margin padding surrounding the member nodes.
            parent: Optional parent group/cluster ID for nested boundaries.
            order: Optional sequence index among peer containers.
            pos: Optional 2D macro spatial position ("top", "bottom", "left", "right", "center").

        Returns:
            The registered Cluster object.

        Raises:
            ValueError: If a cluster with the same id is already registered.
        """
        if id in self._clusters:
            raise ValueError(f"Cluster '{id}' is already registered in the graph.")

        c = Cluster(
            id=id,
            nodes=list(nodes),
            label=label,
            style=style if style is not None else Styles.MutedDashed,
            text_style=text_style,
            padding=padding,
            parent=parent,
            order=order,
            pos=pos,
        )
        self._clusters[id] = c
        return c

    def group(
        self,
        id: str,
        label: str | None = None,
        *,
        nodes: list[str] | None = None,
        style: Style | None = None,
        text_style: Style | None = None,
        padding: float = 4.0,
        parent: str | None = None,
        order: int | None = None,
        pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
    ) -> Cluster:
        """Register an architectural container / group (e.g. VPC, subnet, zone).

        Args:
            id: Unique identifier string for the container.
            label: Text title for the container. Defaults to id if None.
            nodes: Optional initial list of member node IDs.
            style: Container boundary and fill style (defaults to Styles.MutedDashed).
            text_style: Text style for the container label.
            padding: Margin padding surrounding member elements.
            parent: Optional parent container ID (e.g. Subnet in VPC).
            order: Optional ordering rank among peer containers.
            pos: Optional 2D macro spatial position ("top", "bottom", "left", "right", "center").

        Returns:
            The registered Cluster object.
        """
        return self.cluster(
            id=id,
            nodes=nodes or [],
            label=label if label is not None else id,
            style=style,
            text_style=text_style,
            padding=padding,
            parent=parent,
            order=order,
            pos=pos,
        )

    @abstractmethod
    def calc(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute node, edge, and cluster geometries without drawing.

        Args:
            width: Target canvas width.
            height: Target canvas height.
            margin: Outer margin surrounding the diagram.

        Returns:
            A GraphLayout containing all computed geometries.
        """

    def draw(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Calculate layout and render immediately onto the active Drawlib canvas.

        Args:
            width: Target canvas width.
            height: Target canvas height.
            margin: Outer margin surrounding the diagram.

        Returns:
            The calculated GraphLayout that was rendered.
        """
        layout = self.calc(width=width, height=height, margin=margin)
        render_layout(layout)
        return layout

    def export_code(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> str:
        """Calculate layout and export as standalone executable Drawlib Python code.

        Args:
            width: Target canvas width.
            height: Target canvas height.
            margin: Outer margin surrounding the diagram.

        Returns:
            Formatted Drawlib Python script.
        """
        layout = self.calc(width=width, height=height, margin=margin)
        return generate_code(layout)
