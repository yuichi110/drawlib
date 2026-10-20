# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Original IT Service icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_itservice._base import (
    ORIGINAL_ITSERVICE_PROVIDER,
)
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalItserviceIcon
from drawlib.icons import original_itservice
from drawlib.styles import Styles
from drawlib.types import Style

ALL_20_CONCEPT_ICONS = [
    "architect_lead",
    "bpo_center",
    "client_enterprise",
    "dedicated_team",
    "escalation_flow",
    "it_consulting",
    "joint_venture",
    "msp_operations",
    "offshore_lab",
    "org_hierarchy",
    "pmo_office",
    "prime_contractor",
    "project_manager",
    "raci_matrix",
    "ses_engineer",
    "sla_contract",
    "staff_augmentation",
    "steering_committee",
    "support_operator",
    "system_integrator",
]

ALL_44_BRAND_ICONS = [
    "accenture",
    "adecco",
    "atos",
    "bain",
    "bcg",
    "booz_allen",
    "capgemini",
    "cgi",
    "cognizant",
    "concentrix",
    "deloitte",
    "dxc",
    "endava",
    "epam",
    "ey",
    "fujitsu",
    "genpact",
    "globant",
    "hcltech",
    "hitachi",
    "ibm",
    "indra",
    "infosys",
    "kpmg",
    "kyndryl",
    "leidos",
    "ltimindtree",
    "manpower",
    "mckinsey",
    "nec",
    "nri",
    "ntt_data",
    "pwc",
    "rackspace",
    "randstad",
    "slalom",
    "sopra_steria",
    "t_systems",
    "tcs",
    "tech_mahindra",
    "teksystems",
    "thoughtworks",
    "tietoevry",
    "wipro",
]


class TestOriginalItserviceIcons:
    """Tests for `drawlib.icons.original_itservice` and `OriginalItserviceIcon`."""

    def test_original_itservice_all_64_icons(self, tmp_path: Path) -> None:
        """Verify all 64 original IT service concepts and brand icons exist and render."""
        clear()
        all_64 = ALL_20_CONCEPT_ICONS + ALL_44_BRAND_ICONS
        assert len(all_64) == 64
        for idx, name in enumerate(all_64):
            assert hasattr(original_itservice, name), f"Missing canonical icon: {name}"
            assert hasattr(OriginalItserviceIcon, name.upper()), f"Missing enum: {name.upper()}"
            col = idx % 8
            row = idx // 8
            fn = getattr(original_itservice, name)
            fn(xy=(8 + col * 11.5, 90 - row * 11), width=7.5, style=Style(), variant="default")

        out = tmp_path / "test_original_itservice_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_itservice_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalItserviceIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(
            Node("Client", width=20, height=20, icon=OriginalItserviceIcon.CLIENT_ENTERPRISE),
            (20, 50),
        )
        n2 = diag.add(
            Node("Prime SIer", width=20, height=20, icon=OriginalItserviceIcon.PRIME_CONTRACTOR),
            (50, 50),
        )
        n3 = diag.add(
            Node("Accenture", width=20, height=20, icon=OriginalItserviceIcon.ACCENTURE),
            (80, 50),
        )
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_itservice.png"
        save(str(out))
        assert out.is_file()

    def test_original_itservice_provider_metadata(self) -> None:
        """Verify provider package name."""
        assert ORIGINAL_ITSERVICE_PROVIDER.name == "original_itservice"
        assert ORIGINAL_ITSERVICE_PROVIDER.package_name == "icon_original_itservice"
        assert ORIGINAL_ITSERVICE_PROVIDER.asset_subdir == "icons/original_itservice"
