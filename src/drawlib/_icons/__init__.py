# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for font_icon() function and icon modules."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from drawlib._icons.font_icons import (
        font_icon,
        phosphor,
    )
    from drawlib._icons.png_icons import (
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
        security,
        server,
        social,
        workspace,
    )

_PNG_SUITES: Final[frozenset[str]] = frozenset(
    {
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
        "security",
        "server",
        "social",
        "workspace",
    }
)


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load icon suites and font_icon helper on first access (PEP 562)."""
    if name == "phosphor":
        module = importlib.import_module("drawlib._icons.font_icons.phosphor")
        globals()[name] = module
        return module
    if name == "font_icon":
        from drawlib._icons.font_icons._font_icon import font_icon  # noqa: PLC0415

        globals()[name] = font_icon
        return font_icon
    if name in _PNG_SUITES:
        module = importlib.import_module(f"drawlib._icons.png_icons.{name}")
        globals()[name] = module
        return module
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
