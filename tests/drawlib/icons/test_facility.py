# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Facility icons."""

from pathlib import Path

from drawlib._icons.png_icons.facility._base import FACILITY_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, FacilityIcon, Node
from drawlib.icons import facility
from drawlib.styles import Styles
from drawlib.types import Style


class TestFacilityIcons:
    """Tests for official Facility icon provider and diagram enum."""

    def test_facility_all_icons(self, tmp_path: Path) -> None:
        """Verify all 49 official facility, carrier, and semiconductor icons render cleanly."""
        clear()
        names = [
            "equinix",
            "digital_realty",
            "ntt_gdc",
            "cyrusone",
            "coresite",
            "vantage_dc",
            "iron_mountain",
            "qts",
            "switch_dc",
            "at_tokyo",
            "megaport",
            "packetfabric",
            "console_connect",
            "de_cix",
            "linx",
            "jpnap",
            "jpix",
            "bbix",
            "starlink",
            "intelsat",
            "ntt",
            "kddi",
            "softbank",
            "iij",
            "colt",
            "att",
            "verizon",
            "lumen",
            "orange",
            "deutsche_telekom",
            "schneider_electric",
            "apc",
            "vertiv",
            "eaton",
            "rittal",
            "panduit",
            "commscope",
            "corning",
            "axis",
            "hid_global",
            "tsmc",
            "globalfoundries",
            "rapidus",
            "asml",
            "tokyo_electron",
            "applied_materials",
            "foxconn",
            "murata",
            "kyocera",
        ]
        assert len(names) == 49
        for idx, name in enumerate(names):
            col = idx % 10
            row = idx // 10
            fn = getattr(facility, name)
            fn(xy=(8 + col * 9.2, 85 - row * 17), width=7, style=Style(), variant="default")

        out = tmp_path / "test_facility_all.png"
        save(str(out))
        assert out.is_file()

    def test_facility_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical facility icons."""
        clear()
        facility.eqix(xy=(15, 70), width=10, style=Style())
        facility.dlr(xy=(30, 70), width=10, style=Style())
        facility.ntt_datacenter(xy=(45, 70), width=10, style=Style())
        facility.decix(xy=(60, 70), width=10, style=Style())
        facility.at_and_t(xy=(75, 70), width=10, style=Style())
        facility.schneider(xy=(90, 70), width=10, style=Style())
        facility.liebert(xy=(15, 45), width=10, style=Style())
        facility.hid(xy=(30, 45), width=10, style=Style())
        facility.taiwan_semiconductor(xy=(45, 45), width=10, style=Style())
        facility.gf(xy=(60, 45), width=10, style=Style())
        facility.tel(xy=(75, 45), width=10, style=Style())
        facility.amat(xy=(90, 45), width=10, style=Style())
        facility.hon_hai(xy=(15, 20), width=10, style=Style())

        out = tmp_path / "test_facility_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_facility_architecture_enum(self, tmp_path: Path) -> None:
        """Verify FacilityIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Equinix", width=20, height=20, icon=FacilityIcon.EQUINIX), (20, 50))
        n2 = diag.add(Node("Megaport", width=20, height=20, icon=FacilityIcon.MEGAPORT), (50, 50))
        n3 = diag.add(Node("NTT", width=20, height=20, icon=FacilityIcon.NTT), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_facility.png"
        save(str(out))
        assert out.is_file()

    def test_facility_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert FACILITY_PROVIDER.name == "facility"
        assert FACILITY_PROVIDER.package_name == "icon_facility"
        assert FACILITY_PROVIDER.aliases["eqix"] == "equinix"
        assert FACILITY_PROVIDER.aliases["dlr"] == "digital_realty"
        assert FACILITY_PROVIDER.aliases["schneider"] == "schneider_electric"
