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

WORKSPACE_ALIASES: dict[str, str] = {
    "acrobat": "adobe_acrobat",
    "adobe": "adobe_acrobat",
    "box_storage": "box",
    "cisco_webex": "webex",
    "dynamics": "dynamics_365",
    "gcal": "google_calendar",
    "gchat": "google_chat",
    "gdocs": "google_docs",
    "gdrive": "google_drive",
    "gforms": "google_forms",
    "gmeet": "google_meet",
    "gsheets": "google_sheets",
    "gslides": "google_slides",
    "gsuite": "google_workspace",
    "m365": "microsoft_365",
    "monday_com": "monday",
    "ms_excel": "excel",
    "ms_flow": "power_automate",
    "ms_onedrive": "onedrive",
    "ms_outlook": "outlook",
    "ms_powerpoint": "powerpoint",
    "ms_sharepoint": "sharepoint",
    "ms_teams": "microsoft_teams",
    "ms_word": "word",
    "office_365": "microsoft_365",
    "power_apps": "power_automate",
    "powerbi": "power_bi",
    "ppt": "powerpoint",
    "sfdc": "salesforce",
    "snow": "servicenow",
    "teams": "microsoft_teams",
}

WORKSPACE_PROVIDER = PngIconProvider(
    name="workspace",
    package_name="icon_workspace",
    asset_subdir="icons/workspace",
    aliases=WORKSPACE_ALIASES,
)

_write = WORKSPACE_PROVIDER.write
