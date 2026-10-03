# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Template resolver for modular slide SmartArt components."""

from __future__ import annotations

import importlib.util
import inspect
import os
import sys
from typing import Dict, Optional, Type

from drawlib._core.l1_core import logger
from drawlib._slide.base import SmartArtComponent

_BUILTIN_SMARTARTS: Dict[str, Type[SmartArtComponent]] = {}


def register_smartart(cls: Type[SmartArtComponent]) -> Type[SmartArtComponent]:
    """Register a built-in SmartArt component class.

    Args:
        cls: SmartArtComponent subclass.

    Returns:
        The registered class.
    """
    if cls.name:
        _BUILTIN_SMARTARTS[cls.name] = cls
    return cls


def resolve_smartart(
    name: str,
    project_dir: Optional[str] = None,
) -> Optional[Type[SmartArtComponent]]:
    """Resolve a SmartArt component class by name.

    Resolution Order:
    1. Project-local directory: `{project_dir}/_slide_templates/{name}.py`
    2. Built-in registry: `_BUILTIN_SMARTARTS[name]`

    Args:
        name: Name of the SmartArt component (e.g., 'curved_agenda', 'timeline').
        project_dir: Optional path to the project or source directory.

    Returns:
        The resolved SmartArtComponent class, or None if not found.
    """
    # 1. Project-local resolution
    if project_dir:
        candidate_paths = [
            os.path.join(project_dir, "_slide_templates", f"{name}.py"),
            os.path.join(project_dir, "templates", f"{name}.py"),
        ]
        for template_path in candidate_paths:
            if os.path.isfile(template_path):
                component_cls = _load_component_from_file(template_path, name)
                if component_cls:
                    return component_cls

    # 2. Built-in registry lookup
    if name in _BUILTIN_SMARTARTS:
        return _BUILTIN_SMARTARTS[name]

    return None


def _load_component_from_file(
    file_path: str,
    expected_name: str,
) -> Optional[Type[SmartArtComponent]]:
    """Load a SmartArtComponent subclass from a python file.

    Args:
        file_path: Absolute or relative path to the python file.
        expected_name: Expected component name.

    Returns:
        The discovered SmartArtComponent subclass, or None.
    """
    module_name = f"_drawlib_custom_smartart_{expected_name}"
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Find any class inheriting from SmartArtComponent
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, SmartArtComponent) and obj is not SmartArtComponent:
                return obj

    except Exception as e:
        logger.warning(f"Failed to load custom slide SmartArt from '{file_path}': {e}")

    return None
