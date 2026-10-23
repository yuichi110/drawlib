# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public diagrams package for drawlib."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from drawlib.diagrams import (
        architecture,
        class_diagram,
        er,
        flow,
        sequence,
        state,
    )

_LAZY_MODULES: Final[dict[str, str]] = {
    "architecture": "drawlib.diagrams.architecture",
    "class_diagram": "drawlib.diagrams.class_diagram",
    "er": "drawlib.diagrams.er",
    "flow": "drawlib.diagrams.flow",
    "sequence": "drawlib.diagrams.sequence",
    "state": "drawlib.diagrams.state",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load diagram submodules on first access (PEP 562)."""
    if name in _LAZY_MODULES:
        module = importlib.import_module(_LAZY_MODULES[name])
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy diagram submodules appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "architecture",
    "class_diagram",
    "er",
    "flow",
    "sequence",
    "state",
]
