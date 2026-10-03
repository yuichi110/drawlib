# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public slide presentation and SmartArt module."""

from __future__ import annotations

from drawlib._slide import (
    BoundingBox,
    ChevronProcess,
    CurvedAgenda,
    SmartArtComponent,
    Timeline,
    build_slide,
    register_smartart,
    resolve_smartart,
)

__all__ = [
    "BoundingBox",
    "ChevronProcess",
    "CurvedAgenda",
    "SmartArtComponent",
    "Timeline",
    "build_slide",
    "register_smartart",
    "resolve_smartart",
]
