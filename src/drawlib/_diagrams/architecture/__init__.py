# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Architecture diagram internal module package."""

from __future__ import annotations

from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
from drawlib._diagrams.architecture._edge import Edge
from drawlib._diagrams.architecture._group import NodeGroup
from drawlib._diagrams.architecture._icons import (
    AiIcon,
    AwsIcon,
    AzureIcon,
    CnativeIcon,
    CustomIcon,
    DataIcon,
    DevopsIcon,
    GcpIcon,
    NetworkIcon,
    OriginalAiIcon,
    OriginalCloudIcon,
    OriginalCnativeIcon,
    OriginalDataIcon,
    OriginalDevopsIcon,
    OriginalNetworkIcon,
    OriginalSecurityIcon,
    OriginalServerIcon,
    PhosphorIcon,
    SecurityIcon,
    ServerIcon,
)
from drawlib._diagrams.architecture._junction import Junction
from drawlib._diagrams.architecture._node import Node

__all__ = [
    "AiIcon",
    "ArchitectureDiagram",
    "AwsIcon",
    "AzureIcon",
    "CnativeIcon",
    "CustomIcon",
    "DataIcon",
    "DevopsIcon",
    "Edge",
    "GcpIcon",
    "Junction",
    "NetworkIcon",
    "Node",
    "NodeGroup",
    "OriginalAiIcon",
    "OriginalCloudIcon",
    "OriginalCnativeIcon",
    "OriginalDataIcon",
    "OriginalDevopsIcon",
    "OriginalNetworkIcon",
    "OriginalSecurityIcon",
    "OriginalServerIcon",
    "PhosphorIcon",
    "SecurityIcon",
    "ServerIcon",
]
