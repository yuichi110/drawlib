# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public sequence diagrams module."""

from __future__ import annotations

from drawlib._diagrams.architecture import _icons as icons
from drawlib._diagrams.architecture._icons import (
    AiIcon,
    AwsIcon,
    AzureIcon,
    ClientIcon,
    CloudIcon,
    CnativeIcon,
    CodeIcon,
    CustomIcon,
    DataIcon,
    DevopsIcon,
    FacilityIcon,
    GcpIcon,
    NetworkIcon,
    OriginalAiIcon,
    OriginalClientIcon,
    OriginalCloudIcon,
    OriginalCnativeIcon,
    OriginalCodeIcon,
    OriginalDataIcon,
    OriginalDevopsIcon,
    OriginalFacilityIcon,
    OriginalNetworkIcon,
    OriginalSecurityIcon,
    OriginalServerIcon,
    OriginalWorkspaceIcon,
    PhosphorIcon,
    SecurityIcon,
    ServerIcon,
    WorkspaceIcon,
)
from drawlib._diagrams.sequence import (
    Block,
    Message,
    Note,
    Participant,
    ParticipantGroup,
    SequenceDiagram,
)

__all__ = [
    "AiIcon",
    "AwsIcon",
    "AzureIcon",
    "Block",
    "ClientIcon",
    "CloudIcon",
    "CnativeIcon",
    "CodeIcon",
    "CustomIcon",
    "DataIcon",
    "DevopsIcon",
    "FacilityIcon",
    "GcpIcon",
    "Message",
    "NetworkIcon",
    "Note",
    "OriginalAiIcon",
    "OriginalClientIcon",
    "OriginalCloudIcon",
    "OriginalCnativeIcon",
    "OriginalCodeIcon",
    "OriginalDataIcon",
    "OriginalDevopsIcon",
    "OriginalFacilityIcon",
    "OriginalNetworkIcon",
    "OriginalSecurityIcon",
    "OriginalServerIcon",
    "OriginalWorkspaceIcon",
    "Participant",
    "ParticipantGroup",
    "PhosphorIcon",
    "SecurityIcon",
    "SequenceDiagram",
    "ServerIcon",
    "WorkspaceIcon",
    "icons",
]
