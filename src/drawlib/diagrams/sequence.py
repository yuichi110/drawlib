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
    ServerIcon,
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
    "CnativeIcon",
    "CustomIcon",
    "DataIcon",
    "DevopsIcon",
    "GcpIcon",
    "Message",
    "NetworkIcon",
    "Note",
    "OriginalAiIcon",
    "OriginalCloudIcon",
    "OriginalCnativeIcon",
    "OriginalDataIcon",
    "OriginalDevopsIcon",
    "OriginalNetworkIcon",
    "OriginalSecurityIcon",
    "OriginalServerIcon",
    "Participant",
    "ParticipantGroup",
    "PhosphorIcon",
    "SequenceDiagram",
    "ServerIcon",
    "icons",
]
