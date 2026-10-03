# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Slide presentation layout and SmartArt module."""

from __future__ import annotations

from drawlib._slide.base import BoundingBox, SmartArtComponent
from drawlib._slide.compiler import build_slide
from drawlib._slide.default import ChevronProcess, Timeline
from drawlib._slide.google import CurvedAgenda
from drawlib._slide.resolver import register_smartart, resolve_smartart

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
