# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Workspace (M365, Google Workspace, collaboration, CRM/ERP, business SaaS) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

WORKSPACE_PROVIDER = PngIconProvider(
    name="workspace",
    package_name="icon_workspace",
    asset_subdir="icons/workspace",
)

_write = WORKSPACE_PROVIDER.write
