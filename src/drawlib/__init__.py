# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Root package."""

import importlib
import importlib.metadata
import re
import sys
from typing import TYPE_CHECKING, Any, Final, List

LIB_NAME: Final[str] = "drawlib"


def _get_version() -> str:
    try:
        return importlib.metadata.version(LIB_NAME)
    except importlib.metadata.PackageNotFoundError:
        return "0.3.0.dev1"


LIB_VERSION: Final[str] = _get_version()


# please list active main committers (1+ commits per month)
AUTHORS: Final[List[str]] = [
    "Yuichi Ito <yuichi@yuichi.com>",
]

# please change accordingly
DESCRIPTION: Final[str] = "Python drawing library. Illustration as Code."
HOMEPAGE: Final[str] = "https://www.drawlib.com"
REPOSITORY: Final[str] = "https://github.com/yuichi110/drawlib"
README: Final[str] = "docs/README_PYPI.md"

__version__: Final[str] = LIB_VERSION


def _check_version_syntax() -> None:  # noqa: C901
    parts = tuple(int(part) if part.isdigit() else part for part in LIB_VERSION.split("."))

    if not isinstance(parts[0], int):
        raise ValueError(f"Major version must be int. But {LIB_VERSION}")

    if not isinstance(parts[1], int):
        raise ValueError(f"Minor version must be int. But {LIB_VERSION}")

    if not isinstance(parts[0], int):
        raise ValueError(f"Patch version must be int. But {LIB_VERSION}")

    if len(parts) == 3:
        return

    if len(parts) != 4:
        raise ValueError(
            f'Version syntax is "major.minor.patch" or "major.minor.patch.pre-release". But {LIB_VERSION}',
        )

    pre_version = parts[3]
    if not isinstance(pre_version, str):
        raise ValueError(f"Pre-release version can't be int. But {LIB_VERSION}")

    def get_dev_value(text: str) -> int:
        matches = re.findall(r"dev(\d+)", text)
        values = [int(match) for match in matches]
        if not values:
            return -1
        return values[0]

    def get_rc_value(text: str) -> int:
        matches = re.findall(r"rc(\d+)", text)
        values = [int(match) for match in matches]
        if not values:
            return -1
        return values[0]

    if get_dev_value(pre_version) >= 1:
        return

    if get_rc_value(pre_version) >= 1:
        return

    raise ValueError(f"Pre-release version must be dev<n> or rc<n>. But {LIB_VERSION}")


try:
    _check_version_syntax()
except ValueError as e:
    print(f"System Error. Version syntax has problem. {str(e)}")
    print("Please check drawlib.__init__.py")
    print("Abort.")
    sys.exit(1)

if TYPE_CHECKING:
    from drawlib import (
        tools,
    )

from drawlib import (  # noqa: E402
    anim,
    canvas,
    charts,
    diagrams,
    fonts,
    geo,
    graph,
    icons,
    images,
    lines,
    math,
    preset_colors,
    preset_styles,
    shapes,
    slide,
    smartarts,
    styles,
    text,
    types,
    utils,
)

_LAZY_MODULES: dict[str, str] = {
    "tools": "drawlib.tools",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load heavy modules only when explicitly accessed."""
    if name in _LAZY_MODULES:
        module = importlib.import_module(_LAZY_MODULES[name])
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy modules appear in dir() and REPL autocompletion."""
    return sorted(__all__)


__all__ = [
    "LIB_VERSION",
    "AUTHORS",
    "LIB_NAME",
    "DESCRIPTION",
    "HOMEPAGE",
    "REPOSITORY",
    "README",
    "anim",
    "canvas",
    "charts",
    "diagrams",
    "fonts",
    "geo",
    "graph",
    "icons",
    "images",
    "lines",
    "math",
    "preset_colors",
    "preset_styles",
    "shapes",
    "slide",
    "smartarts",
    "styles",
    "text",
    "tools",
    "types",
    "utils",
]
