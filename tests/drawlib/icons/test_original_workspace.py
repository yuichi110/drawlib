# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Original Workspace icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_workspace._base import (
    ORIGINAL_WORKSPACE_ALIASES,
    ORIGINAL_WORKSPACE_PROVIDER,
)
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalWorkspaceIcon
from drawlib.icons import original_workspace
from drawlib.styles import Styles
from drawlib.types import Style


class TestOriginalWorkspaceIcons:
    """Tests for `drawlib.icons.original_workspace` and `OriginalWorkspaceIcon`."""

    def test_original_workspace_all_icons(self, tmp_path: Path) -> None:
        """Verify all 74 canonical icons (24 concepts + 50 brands) and 79 aliases exist and render."""
        clear()
        canonical_74 = [
            "email",
            "calendar",
            "chat_message",
            "video_meeting",
            "voice_call",
            "announcement",
            "document",
            "spreadsheet",
            "presentation",
            "pdf_document",
            "cloud_drive",
            "knowledge_base",
            "kanban_board",
            "project_plan",
            "whiteboard",
            "form_survey",
            "e_signature",
            "workflow_automation",
            "crm",
            "erp",
            "helpdesk",
            "hr_portal",
            "billing_invoice",
            "ecommerce_store",
            "microsoft_365",
            "microsoft_teams",
            "outlook",
            "word",
            "excel",
            "powerpoint",
            "onedrive",
            "sharepoint",
            "power_bi",
            "power_automate",
            "google_workspace",
            "gmail",
            "google_drive",
            "google_docs",
            "google_sheets",
            "google_slides",
            "google_calendar",
            "google_meet",
            "google_chat",
            "google_forms",
            "slack",
            "zoom",
            "webex",
            "discord",
            "notion",
            "confluence",
            "jira",
            "asana",
            "monday",
            "figma",
            "miro",
            "canva",
            "adobe_acrobat",
            "dropbox",
            "box",
            "docusign",
            "trello",
            "linear",
            "airtable",
            "zapier",
            "salesforce",
            "hubspot",
            "zendesk",
            "servicenow",
            "sap",
            "workday",
            "dynamics_365",
            "tableau",
            "stripe",
            "shopify",
        ]
        assert len(canonical_74) == 74
        for idx, name in enumerate(canonical_74):
            assert hasattr(original_workspace, name), f"Missing canonical icon: {name}"
            assert hasattr(OriginalWorkspaceIcon, name.upper()), f"Missing enum: {name.upper()}"
            col = idx % 10
            row = idx // 10
            fn = getattr(original_workspace, name)
            fn(xy=(8 + col * 9.0, 90 - row * 11), width=6.5, style=Style(), variant="default")

        assert len(ORIGINAL_WORKSPACE_ALIASES) == 79
        for alias in ORIGINAL_WORKSPACE_ALIASES:
            assert hasattr(original_workspace, alias), f"Missing alias function: {alias}"
            assert hasattr(OriginalWorkspaceIcon, alias.upper()), f"Missing alias enum: {alias.upper()}"

        out = tmp_path / "test_original_workspace_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_workspace_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical original_workspace icons."""
        clear()
        original_workspace.mail(xy=(15, 70), width=10, style=Style())
        original_workspace.wiki(xy=(30, 70), width=10, style=Style())
        original_workspace.gantt(xy=(45, 70), width=10, style=Style())
        original_workspace.itsm(xy=(60, 70), width=10, style=Style())
        original_workspace.m365(xy=(75, 70), width=10, style=Style())
        original_workspace.teams(xy=(90, 70), width=10, style=Style())
        original_workspace.gsuite(xy=(15, 45), width=10, style=Style())
        original_workspace.sfdc(xy=(30, 45), width=10, style=Style())

        out = tmp_path / "test_original_workspace_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_original_workspace_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalWorkspaceIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(
            Node("Helpdesk", width=20, height=20, icon=OriginalWorkspaceIcon.HELPDESK),
            (20, 50),
        )
        n2 = diag.add(
            Node("Workflow", width=20, height=20, icon=OriginalWorkspaceIcon.WORKFLOW_AUTOMATION),
            (50, 50),
        )
        n3 = diag.add(
            Node("Slack", width=20, height=20, icon=OriginalWorkspaceIcon.SLACK),
            (80, 50),
        )
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_workspace.png"
        save(str(out))
        assert out.is_file()

    def test_original_workspace_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert ORIGINAL_WORKSPACE_PROVIDER.name == "original_workspace"
        assert ORIGINAL_WORKSPACE_PROVIDER.package_name == "icon_original_workspace"
        assert ORIGINAL_WORKSPACE_PROVIDER.asset_subdir == "icons/original_workspace"
        assert ORIGINAL_WORKSPACE_PROVIDER.aliases["mail"] == "email"
        assert ORIGINAL_WORKSPACE_PROVIDER.aliases["m365"] == "microsoft_365"
        assert ORIGINAL_WORKSPACE_PROVIDER.aliases["sfdc"] == "salesforce"
