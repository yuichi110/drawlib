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

import sys

from drawlib._icons import (
    ai,
    aws,
    azure,
    cnative,
    data,
    devops,
    font_icon,
    gcp,
    network,
    original_ai,
    original_cloud,
    original_cnative,
    original_data,
    original_devops,
    original_network,
    original_security,
    original_server,
    phosphor,
    server,
)

# Allow submodule style imports: `import drawlib.icons.phosphor`, `import drawlib.icons.gcp`, etc.
sys.modules["drawlib.icons.phosphor"] = phosphor
sys.modules["drawlib.icons.ai"] = ai
sys.modules["drawlib.icons.aws"] = aws
sys.modules["drawlib.icons.azure"] = azure
sys.modules["drawlib.icons.cnative"] = cnative
sys.modules["drawlib.icons.data"] = data
sys.modules["drawlib.icons.devops"] = devops
sys.modules["drawlib.icons.gcp"] = gcp
sys.modules["drawlib.icons.network"] = network
sys.modules["drawlib.icons.original_ai"] = original_ai
sys.modules["drawlib.icons.original_cloud"] = original_cloud
sys.modules["drawlib.icons.original_cnative"] = original_cnative
sys.modules["drawlib.icons.original_data"] = original_data
sys.modules["drawlib.icons.original_devops"] = original_devops
sys.modules["drawlib.icons.original_network"] = original_network
sys.modules["drawlib.icons.original_security"] = original_security
sys.modules["drawlib.icons.original_server"] = original_server
sys.modules["drawlib.icons.server"] = server

__all__ = [
    "ai",
    "aws",
    "azure",
    "cnative",
    "data",
    "devops",
    "font_icon",
    "gcp",
    "network",
    "original_ai",
    "original_cloud",
    "original_cnative",
    "original_data",
    "original_devops",
    "original_network",
    "original_security",
    "original_server",
    "phosphor",
    "server",
]
