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
    ORIGINAL_FACILITY_ALIASES,
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
        """Verify all 86 canonical icons (37 concepts + 49 brands) and 120 aliases exist and render."""
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

        assert len(ORIGINAL_FACILITY_ALIASES) == 120
        for alias in ORIGINAL_FACILITY_ALIASES:
            assert hasattr(original_facility, alias), f"Missing alias function: {alias}"
            assert hasattr(OriginalFacilityIcon, alias.upper()), f"Missing alias enum: {alias.upper()}"

        out = tmp_path / "test_original_facility_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_facility_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical original_facility icons."""
        clear()
        original_facility.data_center(xy=(15, 70), width=10, style=Style())
        original_facility.pylon(xy=(30, 70), width=10, style=Style())
        original_facility.optical_fiber(xy=(45, 70), width=10, style=Style())
        original_facility.truck(xy=(60, 70), width=10, style=Style())
        original_facility.eqix(xy=(75, 70), width=10, style=Style())
        original_facility.dlr(xy=(90, 70), width=10, style=Style())
        original_facility.schneider(xy=(15, 45), width=10, style=Style())
        original_facility.cctv(xy=(30, 45), width=10, style=Style())
        original_facility.cleanroom(xy=(45, 45), width=10, style=Style())
        original_facility.taiwan_semiconductor(xy=(60, 45), width=10, style=Style())
        original_facility.tel(xy=(75, 45), width=10, style=Style())
        original_facility.amat(xy=(90, 45), width=10, style=Style())

        out = tmp_path / "test_original_facility_aliases.png"
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
        """Verify provider package name and aliases mapping."""
        assert ORIGINAL_FACILITY_PROVIDER.name == "original_facility"
        assert ORIGINAL_FACILITY_PROVIDER.package_name == "icon_original_facility"
        assert ORIGINAL_FACILITY_PROVIDER.asset_subdir == "icons/original_facility"
        assert ORIGINAL_FACILITY_PROVIDER.aliases["eqix"] == "equinix"
        assert ORIGINAL_FACILITY_PROVIDER.aliases["pylon"] == "transmission_tower"
        assert ORIGINAL_FACILITY_PROVIDER.aliases["truck"] == "cargo_truck"
