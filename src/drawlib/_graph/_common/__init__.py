# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common models, abstractions, renderers, and edge routing for graph solvers."""

from __future__ import annotations

from drawlib._graph._common._base import BaseGraph
from drawlib._graph._common._code_generator import generate_code
from drawlib._graph._common._models import (
    Cluster,
    ClusterLayout,
    Edge,
    EdgeLayout,
    GraphLayout,
    Node,
    NodeLayout,
)
from drawlib._graph._common._renderer import render_layout
from drawlib._graph._common._routing import route_orthogonal_edge, route_straight_edge

__all__ = [
    "BaseGraph",
    "Cluster",
    "ClusterLayout",
    "Edge",
    "EdgeLayout",
    "GraphLayout",
    "Node",
    "NodeLayout",
    "generate_code",
    "render_layout",
    "route_orthogonal_edge",
    "route_straight_edge",
]
