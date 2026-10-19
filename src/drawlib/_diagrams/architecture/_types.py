# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for architecture diagrams."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypeAlias, TypeVar

from PIL.Image import Image

from drawlib._core.l3_images import Dimage
from drawlib._diagrams.architecture._icons import (
    AiIcon,
    AwsIcon,
    AzureIcon,
    BusinessIcon,
    ClientIcon,
    CloudIcon,
    CnativeIcon,
    CodeIcon,
    CustomIcon,
    DataIcon,
    DevopsIcon,
    FacilityIcon,
    GcpIcon,
    ItserviceIcon,
    NetworkIcon,
    OriginalAiIcon,
    OriginalBusinessIcon,
    OriginalClientIcon,
    OriginalCloudIcon,
    OriginalCnativeIcon,
    OriginalCodeIcon,
    OriginalDataIcon,
    OriginalDevopsIcon,
    OriginalFacilityIcon,
    OriginalItserviceIcon,
    OriginalNetworkIcon,
    OriginalSecurityIcon,
    OriginalServerIcon,
    OriginalSocialIcon,
    OriginalWorkspaceIcon,
    PhosphorIcon,
    SecurityIcon,
    ServerIcon,
    SocialIcon,
    WorkspaceIcon,
)

if TYPE_CHECKING:
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
    from drawlib._diagrams.architecture._group import NodeGroup
    from drawlib._diagrams.architecture._junction import Junction
    from drawlib._diagrams.architecture._node import Node

# Connectable elements (can be start or end of an edge)
Connectable: TypeAlias = "Node | NodeGroup | Junction"

# Diagram / Group item that can be added
DiagramItem: TypeAlias = "Node | NodeGroup | Junction"
ItemT = TypeVar("ItemT", bound="DiagramItem")

# Edge routing strategy
RoutingType = Literal["orthogonal", "direct", "curved"]

# Arrowhead configuration
ArrowType = Literal["->", "<-", "<->", "-"] | str

# Edge padding type (float or (start_padding, end_padding))
PaddingType = float | tuple[float, float]

# Node icon types supported
IconFunction = Callable[..., object]
IconType: TypeAlias = (
    OriginalAiIcon
    | OriginalBusinessIcon
    | OriginalClientIcon
    | OriginalCloudIcon
    | OriginalCnativeIcon
    | OriginalCodeIcon
    | OriginalDataIcon
    | OriginalDevopsIcon
    | OriginalFacilityIcon
    | OriginalItserviceIcon
    | OriginalNetworkIcon
    | OriginalSecurityIcon
    | OriginalServerIcon
    | OriginalSocialIcon
    | OriginalWorkspaceIcon
    | AiIcon
    | AwsIcon
    | AzureIcon
    | BusinessIcon
    | ClientIcon
    | CloudIcon
    | CnativeIcon
    | CodeIcon
    | DataIcon
    | DevopsIcon
    | FacilityIcon
    | GcpIcon
    | ItserviceIcon
    | NetworkIcon
    | PhosphorIcon
    | SecurityIcon
    | ServerIcon
    | SocialIcon
    | WorkspaceIcon
    | CustomIcon
    | Dimage
    | Image
    | str
    | Path
    | IconFunction
    | None
)

DiagramT = TypeVar("DiagramT", bound="ArchitectureDiagram")
