# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_WORKSPACE_ALIASES: dict[str, str] = {
    "accounting": "billing_invoice",
    "acrobat": "adobe_acrobat",
    "adobe": "adobe_acrobat",
    "agile_board": "kanban_board",
    "back_office": "erp",
    "box_storage": "box",
    "brainstorm": "whiteboard",
    "broadcast": "announcement",
    "canvas_board": "whiteboard",
    "cisco_webex": "webex",
    "contract_sign": "e_signature",
    "customer_management": "crm",
    "digital_sign": "e_signature",
    "dynamics": "dynamics_365",
    "employee_directory": "hr_portal",
    "enterprise_resource": "erp",
    "feedback_form": "form_survey",
    "file_sync": "cloud_drive",
    "gantt": "project_plan",
    "gcal": "google_calendar",
    "gchat": "google_chat",
    "gdocs": "google_docs",
    "gdrive": "google_drive",
    "gforms": "google_forms",
    "gmeet": "google_meet",
    "gsheets": "google_sheets",
    "gslides": "google_slides",
    "gsuite": "google_workspace",
    "human_resources": "hr_portal",
    "inbox": "email",
    "instant_message": "chat_message",
    "internal_docs": "knowledge_base",
    "itsm": "helpdesk",
    "m365": "microsoft_365",
    "mail": "email",
    "meeting_invite": "calendar",
    "monday_com": "monday",
    "ms_excel": "excel",
    "ms_flow": "power_automate",
    "ms_onedrive": "onedrive",
    "ms_outlook": "outlook",
    "ms_powerpoint": "powerpoint",
    "ms_sharepoint": "sharepoint",
    "ms_teams": "microsoft_teams",
    "ms_word": "word",
    "newsletter": "announcement",
    "no_code_flow": "workflow_automation",
    "office_365": "microsoft_365",
    "online_meeting": "video_meeting",
    "online_shop": "ecommerce_store",
    "payment": "billing_invoice",
    "pdf_file": "pdf_document",
    "phone_call": "voice_call",
    "power_apps": "power_automate",
    "powerbi": "power_bi",
    "ppt": "powerpoint",
    "questionnaire": "form_survey",
    "report_pdf": "pdf_document",
    "roadmap": "project_plan",
    "sales_lead": "crm",
    "schedule": "calendar",
    "sfdc": "salesforce",
    "shared_drive": "cloud_drive",
    "sheet": "spreadsheet",
    "shopping_cart": "ecommerce_store",
    "slide_deck": "presentation",
    "slides": "presentation",
    "snow": "servicenow",
    "support_ticket": "helpdesk",
    "table_doc": "spreadsheet",
    "task_board": "kanban_board",
    "team_chat": "chat_message",
    "teams": "microsoft_teams",
    "text_doc": "document",
    "video_call": "video_meeting",
    "voip": "voice_call",
    "wiki": "knowledge_base",
    "word_doc": "document",
    "zap": "workflow_automation",
}

ORIGINAL_WORKSPACE_PROVIDER = PngIconProvider(
    name="original_workspace",
    package_name="icon_original_workspace",
    asset_subdir="icons/original_workspace",
    aliases=ORIGINAL_WORKSPACE_ALIASES,
)

_write = ORIGINAL_WORKSPACE_PROVIDER.write
