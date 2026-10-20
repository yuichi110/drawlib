# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Original Facility icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_facility._base import (
    ORIGINAL_FACILITY_PROVIDER,
)
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalFacilityIcon
from drawlib.icons import original_facility
from drawlib.styles import Styles
from drawlib.types import Style


class TestOriginalFacilityIcons:
    """Tests for `drawlib.icons.original_facility` and `OriginalFacilityIcon`."""

    def test_original_facility_all_icons(self, tmp_path: Path) -> None:
        """Verify all 86 canonical icons (37 concepts + 49 brands) exist and render."""
        clear()
        canonical_86 = [
            "datacenter",
            "server_room",
            "colocation",
            "cell_tower",
            "satellite_station",
            "cable_landing",
            "power_plant",
            "solar_wind",
            "substation",
            "transmission_tower",
            "ups_power",
            "generator",
            "fiber_optic",
            "patch_panel",
            "utility_pole",
            "underground_conduit",
            "rack_cabinet",
            "cooling_hvac",
            "headquarters",
            "branch_office",
            "campus",
            "shared_office",
            "home_office",
            "public_building",
            "factory",
            "semiconductor_fab",
            "warehouse",
            "retail_store",
            "hospital",
            "school",
            "fire_suppression",
            "cargo_truck",
            "service_van",
            "cargo_ship",
            "cargo_plane",
            "security_gate",
            "surveillance_camera",
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
        assert len(canonical_86) == 86
        for idx, name in enumerate(canonical_86):
            assert hasattr(original_facility, name), f"Missing canonical icon: {name}"
            assert hasattr(OriginalFacilityIcon, name.upper()), f"Missing enum: {name.upper()}"
            col = idx % 10
            row = idx // 10
            fn = getattr(original_facility, name)
            fn(xy=(8 + col * 9.0, 92 - row * 10), width=6.5, style=Style(), variant="default")

        out = tmp_path / "test_original_facility_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_facility_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalFacilityIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(
            Node("Power Plant", width=20, height=20, icon=OriginalFacilityIcon.POWER_PLANT),
            (20, 50),
        )
        n2 = diag.add(
            Node("Substation", width=20, height=20, icon=OriginalFacilityIcon.SUBSTATION),
            (50, 50),
        )
        n3 = diag.add(
            Node("Equinix DC", width=20, height=20, icon=OriginalFacilityIcon.EQUINIX),
            (80, 50),
        )
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_facility.png"
        save(str(out))
        assert out.is_file()

    def test_original_facility_provider_metadata(self) -> None:
        """Verify provider package name."""
        assert ORIGINAL_FACILITY_PROVIDER.name == "original_facility"
        assert ORIGINAL_FACILITY_PROVIDER.package_name == "icon_original_facility"
        assert ORIGINAL_FACILITY_PROVIDER.asset_subdir == "icons/original_facility"
