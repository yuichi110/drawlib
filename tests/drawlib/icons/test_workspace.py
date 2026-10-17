# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Workspace icons."""

from pathlib import Path

from drawlib._icons.png_icons.workspace._base import WORKSPACE_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, WorkspaceIcon
from drawlib.icons import workspace
from drawlib.styles import Styles
from drawlib.types import Style


class TestWorkspaceIcons:
    """Tests for official Workspace icon provider and diagram enum."""

    def test_workspace_all_icons(self, tmp_path: Path) -> None:
        """Verify all 50 official workplace, collaboration, and business SaaS icons render cleanly."""
        clear()
        names = [
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
        for idx, name in enumerate(names):
            col = idx % 10
            row = idx // 10
            fn = getattr(workspace, name)
            fn(xy=(8 + col * 9.3, 82 - row * 16), width=7, style=Style(), variant="default")

        out = tmp_path / "test_workspace_all.png"
        save(str(out))
        assert out.is_file()

    def test_workspace_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical workspace icons."""
        clear()
        workspace.m365(xy=(15, 70), width=10, style=Style())
        workspace.teams(xy=(30, 70), width=10, style=Style())
        workspace.gdrive(xy=(45, 70), width=10, style=Style())
        workspace.gdocs(xy=(60, 70), width=10, style=Style())
        workspace.sfdc(xy=(75, 70), width=10, style=Style())
        workspace.snow(xy=(90, 70), width=10, style=Style())

        out = tmp_path / "test_workspace_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_workspace_architecture_enum(self, tmp_path: Path) -> None:
        """Verify WorkspaceIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("M365", width=20, height=20, icon=WorkspaceIcon.MICROSOFT_365), (20, 50))
        n2 = diag.add(Node("Slack", width=20, height=20, icon=WorkspaceIcon.SLACK), (50, 50))
        n3 = diag.add(Node("Salesforce", width=20, height=20, icon=WorkspaceIcon.SALESFORCE), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_workspace.png"
        save(str(out))
        assert out.is_file()

    def test_workspace_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert WORKSPACE_PROVIDER.name == "workspace"
        assert WORKSPACE_PROVIDER.package_name == "icon_workspace"
        assert WORKSPACE_PROVIDER.aliases["m365"] == "microsoft_365"
        assert WORKSPACE_PROVIDER.aliases["teams"] == "microsoft_teams"
        assert WORKSPACE_PROVIDER.aliases["sfdc"] == "salesforce"
