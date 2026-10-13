# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Verify all public drawlib module attributes have docstrings."""

from __future__ import annotations

import inspect
import typing

import drawlib.anim
import drawlib.canvas
import drawlib.charts
import drawlib.diagrams
import drawlib.fonts
import drawlib.graph
import drawlib.icons
import drawlib.images
import drawlib.lines
import drawlib.math
import drawlib.preset_colors
import drawlib.preset_styles
import drawlib.shapes
import drawlib.slide
import drawlib.smartarts
import drawlib.styles
import drawlib.text
import drawlib.types


def test_all_doc_exist() -> None:
    modules = [
        drawlib.anim,
        drawlib.canvas,
        drawlib.charts,
        drawlib.diagrams,
        drawlib.fonts,
        drawlib.graph,
        drawlib.icons,
        drawlib.images,
        drawlib.lines,
        drawlib.math,
        drawlib.preset_colors,
        drawlib.preset_styles,
        drawlib.shapes,
        drawlib.slide,
        drawlib.smartarts,
        drawlib.styles,
        drawlib.text,
        drawlib.types,
    ]
    all_drawlib_objects_have_doc = True
    for mod in modules:
        members = inspect.getmembers(mod)
        drawlib_members = [o[1] for o in members if not o[0].startswith("_") and o[0] != "annotations"]
        for drawlib_object in drawlib_members:
            if typing.get_origin(drawlib_object) is not None:
                continue
            if getattr(drawlib_object, "__doc__", None) is None:
                print(f"'{getattr(drawlib_object, '__name__', str(drawlib_object))}' in {mod.__name__} has no doc.")
                all_drawlib_objects_have_doc = False

    assert all_drawlib_objects_have_doc

