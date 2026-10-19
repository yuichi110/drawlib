# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for IT Service icons."""

from pathlib import Path

from drawlib._icons.png_icons.itservice._base import ITSERVICE_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, ItserviceIcon, Node
from drawlib.icons import itservice
from drawlib.styles import Styles
from drawlib.types import Style

ALL_44_ITSERVICE_ICONS = [
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


class TestItserviceIcons:
    """Tests for official IT Service icon provider and diagram enum."""

    def test_all_itservice_icons(self, tmp_path: Path) -> None:
        """Verify all 44 IT service, consulting, SIer, BPO, and staffing icons exist and render cleanly."""
        clear()
        assert len(ALL_44_ITSERVICE_ICONS) == 44
        for idx, name in enumerate(ALL_44_ITSERVICE_ICONS):
            assert hasattr(itservice, name), f"Missing itservice icon function: {name}"
            assert hasattr(ItserviceIcon, name.upper()), f"Missing ItserviceIcon enum: {name.upper()}"
            col = idx % 8
            row = idx // 8
            fn = getattr(itservice, name)
            fn(xy=(8 + col * 12, 85 - row * 14), width=8, style=Style(), variant="default")

        out = tmp_path / "test_itservice_all.png"
        save(str(out))
        assert out.is_file()

    def test_itservice_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical itservice icons."""
        clear()
        itservice.acn(xy=(15, 70), width=10, style=Style())
        itservice.nttdata(xy=(30, 70), width=10, style=Style())
        itservice.tata_consultancy_services(xy=(45, 70), width=10, style=Style())
        itservice.hcl(xy=(60, 70), width=10, style=Style())
        itservice.ernst_and_young(xy=(75, 70), width=10, style=Style())
        itservice.bah(xy=(90, 70), width=10, style=Style())

        out = tmp_path / "test_itservice_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_itservice_architecture_enum(self, tmp_path: Path) -> None:
        """Verify ItserviceIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Accenture", width=20, height=20, icon=ItserviceIcon.ACCENTURE), (20, 50))
        n2 = diag.add(Node("NTT DATA", width=20, height=20, icon=ItserviceIcon.NTT_DATA), (50, 50))
        n3 = diag.add(Node("Wipro", width=20, height=20, icon=ItserviceIcon.WIPRO), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_itservice.png"
        save(str(out))
        assert out.is_file()

    def test_itservice_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert ITSERVICE_PROVIDER.name == "itservice"
        assert ITSERVICE_PROVIDER.package_name == "icon_itservice"
        assert ITSERVICE_PROVIDER.aliases["acn"] == "accenture"
        assert ITSERVICE_PROVIDER.aliases["bah"] == "booz_allen"
        assert ITSERVICE_PROVIDER.aliases["ernst_and_young"] == "ey"
        assert ITSERVICE_PROVIDER.aliases["hcl"] == "hcltech"
        assert ITSERVICE_PROVIDER.aliases["nttdata"] == "ntt_data"
        assert ITSERVICE_PROVIDER.aliases["tata_consultancy_services"] == "tcs"
