# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public icons module for drawlib."""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import sys
from types import ModuleType
from typing import TYPE_CHECKING, Any, Final, Sequence

if TYPE_CHECKING:
    from drawlib._icons import (
        ai,
        aws,
        azure,
        business,
        client,
        cloud,
        cnative,
        code,
        data,
        devops,
        facility,
        font_icon,
        gcp,
        itservice,
        network,
        original_ai,
        original_business,
        original_client,
        original_cloud,
        original_cnative,
        original_code,
        original_data,
        original_devops,
        original_facility,
        original_itservice,
        original_network,
        original_security,
        original_server,
        original_social,
        original_workspace,
        phosphor,
        security,
        server,
        social,
        workspace,
    )

# Expose __path__ so Python's import system treats `drawlib.icons` as a package
# for submodule imports (`import drawlib.icons.phosphor`, `from drawlib.icons.gcp import ...`).
__path__: list[str] = []

_ICON_SUBMODULE_TARGETS: Final[dict[str, str]] = {
    "phosphor": "drawlib._icons.font_icons.phosphor",
    "ai": "drawlib._icons.png_icons.ai",
    "aws": "drawlib._icons.png_icons.aws",
    "azure": "drawlib._icons.png_icons.azure",
    "business": "drawlib._icons.png_icons.business",
    "client": "drawlib._icons.png_icons.client",
    "cloud": "drawlib._icons.png_icons.cloud",
    "cnative": "drawlib._icons.png_icons.cnative",
    "code": "drawlib._icons.png_icons.code",
    "data": "drawlib._icons.png_icons.data",
    "devops": "drawlib._icons.png_icons.devops",
    "facility": "drawlib._icons.png_icons.facility",
    "gcp": "drawlib._icons.png_icons.gcp",
    "itservice": "drawlib._icons.png_icons.itservice",
    "network": "drawlib._icons.png_icons.network",
    "original_ai": "drawlib._icons.png_icons.original_ai",
    "original_business": "drawlib._icons.png_icons.original_business",
    "original_client": "drawlib._icons.png_icons.original_client",
    "original_cloud": "drawlib._icons.png_icons.original_cloud",
    "original_cnative": "drawlib._icons.png_icons.original_cnative",
    "original_code": "drawlib._icons.png_icons.original_code",
    "original_data": "drawlib._icons.png_icons.original_data",
    "original_devops": "drawlib._icons.png_icons.original_devops",
    "original_facility": "drawlib._icons.png_icons.original_facility",
    "original_itservice": "drawlib._icons.png_icons.original_itservice",
    "original_network": "drawlib._icons.png_icons.original_network",
    "original_security": "drawlib._icons.png_icons.original_security",
    "original_server": "drawlib._icons.png_icons.original_server",
    "original_social": "drawlib._icons.png_icons.original_social",
    "original_workspace": "drawlib._icons.png_icons.original_workspace",
    "security": "drawlib._icons.png_icons.security",
    "server": "drawlib._icons.png_icons.server",
    "social": "drawlib._icons.png_icons.social",
    "workspace": "drawlib._icons.png_icons.workspace",
}


def _load_icon_submodule(name: str) -> ModuleType:
    """Import an icon suite on demand and register its `drawlib.icons.<name>` alias."""
    module = importlib.import_module(_ICON_SUBMODULE_TARGETS[name])
    sys.modules[f"drawlib.icons.{name}"] = module
    globals()[name] = module
    return module


class _IconsSubmoduleLoader(importlib.abc.Loader):
    """Loader returning the underlying icon suite module for `drawlib.icons.<name>`."""

    def __init__(self, suite_name: str) -> None:
        self._suite_name = suite_name

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> ModuleType:  # noqa: ARG002
        return _load_icon_submodule(self._suite_name)

    def exec_module(self, module: ModuleType) -> None:
        pass


class _IconsSubmoduleFinder(importlib.abc.MetaPathFinder):
    """MetaPathFinder resolving `drawlib.icons.<suite>` lazily without eager imports."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,  # noqa: ARG002
        target: ModuleType | None = None,  # noqa: ARG002
    ) -> importlib.machinery.ModuleSpec | None:
        if fullname.startswith("drawlib.icons."):
            suite_name = fullname.removeprefix("drawlib.icons.")
            if suite_name in _ICON_SUBMODULE_TARGETS:
                return importlib.machinery.ModuleSpec(fullname, _IconsSubmoduleLoader(suite_name))
        return None


if not any(isinstance(f, _IconsSubmoduleFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, _IconsSubmoduleFinder())


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load icon suites and font_icon helper on first access (PEP 562)."""
    if name in _ICON_SUBMODULE_TARGETS:
        return _load_icon_submodule(name)
    if name == "font_icon":
        from drawlib._icons.font_icons._font_icon import font_icon  # noqa: PLC0415

        globals()[name] = font_icon
        return font_icon
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy icon suites appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "ai",
    "aws",
    "azure",
    "business",
    "client",
    "cloud",
    "cnative",
    "code",
    "data",
    "devops",
    "facility",
    "font_icon",
    "gcp",
    "itservice",
    "network",
    "original_ai",
    "original_business",
    "original_client",
    "original_cloud",
    "original_cnative",
    "original_code",
    "original_data",
    "original_devops",
    "original_facility",
    "original_itservice",
    "original_network",
    "original_security",
    "original_server",
    "original_social",
    "original_workspace",
    "phosphor",
    "security",
    "server",
    "social",
    "workspace",
]
