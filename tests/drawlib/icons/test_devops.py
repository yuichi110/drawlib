# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Official DevOps ecosystem icons drawing."""

from pathlib import Path

import pytest

from drawlib._icons.png_icons.devops._base import DEVOPS_PROVIDER
from drawlib._icons.png_icons.original_devops._base import ORIGINAL_DEVOPS_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, DevopsIcon, Node, OriginalDevopsIcon
from drawlib.diagrams.sequence import Participant, SequenceDiagram
from drawlib.icons import devops, original_devops
from drawlib.styles import Styles
from drawlib.types import Style


class TestDevopsIcons:
    """Tests for DevOps icon provider, aliases, and diagram enums."""

    def test_devops_cicd_and_iac_icons(self, tmp_path: Path) -> None:
        """Verify Source Control, CI/CD, IaC, and Secrets icons."""
        clear()
        devops.git(xy=(15, 75), width=12, style=Style(), variant="default")
        devops.github(xy=(35, 75), width=12, style=Style())
        devops.github_actions(xy=(55, 75), width=12, style=Style())
        devops.gitlab(xy=(75, 75), width=12, style=Style())

        devops.terraform(xy=(15, 50), width=12, style=Style())
        devops.opentofu(xy=(35, 50), width=12, style=Style())
        devops.pulumi(xy=(55, 50), width=12, style=Style())
        devops.ansible(xy=(75, 50), width=12, style=Style())

        devops.vault(xy=(15, 25), width=12, style=Style())
        devops.consul(xy=(35, 25), width=12, style=Style())
        devops.jfrog(xy=(55, 25), width=12, style=Style())
        devops.nexus(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_devops_cicd_iac.png"
        save(str(out))
        assert out.is_file()

    def test_devops_testing_security_and_observability_icons(self, tmp_path: Path) -> None:
        """Verify Testing, DevSecOps, Observability, and Collaboration icons."""
        clear()
        devops.sonarqube(xy=(15, 75), width=12, style=Style())
        devops.snyk(xy=(35, 75), width=12, style=Style())
        devops.trivy(xy=(55, 75), width=12, style=Style())
        devops.playwright(xy=(75, 75), width=12, style=Style())

        devops.datadog(xy=(15, 50), width=12, style=Style())
        devops.sentry(xy=(35, 50), width=12, style=Style())
        devops.loki(xy=(55, 50), width=12, style=Style())
        devops.pagerduty(xy=(75, 50), width=12, style=Style())

        devops.jira(xy=(30, 25), width=12, style=Style())
        devops.slack(xy=(60, 25), width=12, style=Style())

        out = tmp_path / "test_devops_sec_obs.png"
        save(str(out))
        assert out.is_file()

    def test_devops_aliases(self, tmp_path: Path) -> None:
        """Verify DevOps shorthand aliases (gh, gha, gl, tf, tofu, dd, pd, pw, sonar, bb, nr)."""
        clear()
        devops.gh(xy=(15, 70), width=12, style=Style())
        devops.gha(xy=(35, 70), width=12, style=Style())
        devops.gl(xy=(55, 70), width=12, style=Style())
        devops.bb(xy=(75, 70), width=12, style=Style())

        devops.tf(xy=(15, 45), width=12, style=Style())
        devops.tofu(xy=(35, 45), width=12, style=Style())
        devops.dd(xy=(55, 45), width=12, style=Style())
        devops.pd(xy=(75, 45), width=12, style=Style())

        devops.pw(xy=(25, 20), width=12, style=Style())
        devops.sonar(xy=(50, 20), width=12, style=Style())
        devops.nr(xy=(75, 20), width=12, style=Style())

        out = tmp_path / "test_devops_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_devops_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify DevopsIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("GitHub Actions", width=24, height=20, icon=DevopsIcon.GITHUB_ACTIONS), (20, 50))
        n2 = diag.add(Node("Terraform", width=22, height=20, icon=DevopsIcon.TERRAFORM), (50, 50))
        n3 = diag.add(Node("Datadog", width=22, height=20, icon=DevopsIcon.DATADOG), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_devops.png"
        save(str(out))
        assert out.is_file()

    def test_devops_sequence_diagram_enum(self, tmp_path: Path) -> None:
        """Verify DevopsIcon works inside SequenceDiagram participants."""
        clear()
        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        p1 = seq.add(Participant("Sentry", icon=DevopsIcon.SENTRY))
        p2 = seq.add(Participant("PagerDuty", icon=DevopsIcon.PAGERDUTY))
        p3 = seq.add(Participant("Slack", icon=DevopsIcon.SLACK))
        seq.request(p1, p2, "Trigger alert")
        seq.request(p2, p3, "Notify channel")
        seq.draw((10, 10))
        out = tmp_path / "test_seq_devops.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_devops_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid DevOps icon file."""
        with pytest.raises(FileNotFoundError):
            DEVOPS_PROVIDER.get_icon_path("non_existent_devops_icon_xyz")

    def test_original_devops_stylized_icons_and_aliases(self, tmp_path: Path) -> None:
        """Verify Drawlib-stylized Original DevOps icons and aliases."""
        clear()
        original_devops.jenkins(xy=(15, 75), width=12, style=Style())
        original_devops.tekton(xy=(35, 75), width=12, style=Style())
        original_devops.podman(xy=(55, 75), width=12, style=Style())
        original_devops.datadog(xy=(75, 75), width=12, style=Style())

        original_devops.snyk(xy=(15, 45), width=12, style=Style())
        original_devops.gha(xy=(35, 45), width=12, style=Style())
        original_devops.tf(xy=(55, 45), width=12, style=Style())
        original_devops.cicd(xy=(75, 45), width=12, style=Style())

        diag = ArchitectureDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("GitHub", width=22, height=20, icon=OriginalDevopsIcon.GITHUB), (25, 18))
        n2 = diag.add(Node("Jenkins", width=22, height=20, icon=OriginalDevopsIcon.JENKINS), (65, 18))
        diag.connect(n1, n2)
        diag.draw((5, 5))

        out = tmp_path / "test_original_devops_stylized.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_original_devops_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Original DevOps icon file."""
        with pytest.raises(FileNotFoundError):
            ORIGINAL_DEVOPS_PROVIDER.get_icon_path("non_existent_original_devops_icon_xyz")
