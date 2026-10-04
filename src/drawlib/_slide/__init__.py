# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Slide presentation stage and layout module."""

from __future__ import annotations

from drawlib._slide.base import (
    BoundingBox,
    SlideContext,
    current_slide,
    get_slide_context,
    has_slide_context,
    reset_slide_context,
    set_slide_context,
)
from drawlib._slide.compiler import build_slide

__all__ = [
    "BoundingBox",
    "SlideContext",
    "build_slide",
    "current_slide",
    "get_slide_context",
    "has_slide_context",
    "reset_slide_context",
    "set_slide_context",
]
