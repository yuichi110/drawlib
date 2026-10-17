# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Server (Dell EMC & VMware) icons drawing."""

from pathlib import Path

import pytest

from drawlib._icons.png_icons.original_server._base import ORIGINAL_SERVER_PROVIDER
from drawlib._icons.png_icons.server._base import SERVER_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalServerIcon, ServerIcon
from drawlib.icons import original_server, server
from drawlib.styles import Styles
from drawlib.types import Style


class TestServerIcons:
    """Tests for Server (Dell EMC & VMware) icon provider and architecture diagram enum."""

    def test_server_dell_icons(self, tmp_path: Path) -> None:
        """Verify Dell EMC server and storage icons with default variant."""
        clear()
        server.dell_rack_server(xy=(15, 75), width=12, style=Style(), variant="default")
        server.dell_blade_chassis(xy=(35, 75), width=12, style=Style())
        server.dell_tower_server(xy=(55, 75), width=12, style=Style())
        server.dell_gpu_server(xy=(75, 75), width=12, style=Style())

        server.dell_hci_appliance(xy=(15, 50), width=12, style=Style())
        server.dell_bmc_management(xy=(35, 50), width=12, style=Style())
        server.dell_san_storage(xy=(55, 50), width=12, style=Style())
        server.dell_nas_storage(xy=(75, 50), width=12, style=Style())

        server.dell_object_storage(xy=(15, 25), width=12, style=Style())
        server.dell_backup_appliance(xy=(35, 25), width=12, style=Style())
        server.dell_tape_library(xy=(55, 25), width=12, style=Style())
        server.dell_fc_switch(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_server_dell.png"
        save(str(out))
        assert out.is_file()

    def test_server_vmware_icons(self, tmp_path: Path) -> None:
        """Verify VMware virtualization, cluster, and storage icons."""
        clear()
        server.vmware_rack_server(xy=(15, 75), width=12, style=Style(), variant="default")
        server.vmware_esxi_host(xy=(35, 75), width=12, style=Style())
        server.vmware_vm(xy=(55, 75), width=12, style=Style())
        server.vmware_vm_group(xy=(75, 75), width=12, style=Style())

        server.vmware_template(xy=(15, 50), width=12, style=Style())
        server.vmware_snapshot(xy=(35, 50), width=12, style=Style())
        server.vmware_vcenter(xy=(55, 50), width=12, style=Style())
        server.vmware_cluster(xy=(75, 50), width=12, style=Style())

        server.vmware_resource_pool(xy=(15, 25), width=12, style=Style())
        server.vmware_vmotion(xy=(35, 25), width=12, style=Style())
        server.vmware_vswitch(xy=(55, 25), width=12, style=Style())
        server.vmware_datastore(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_server_vmware.png"
        save(str(out))
        assert out.is_file()

    def test_server_aliases(self, tmp_path: Path) -> None:
        """Verify Dell EMC and VMware shorthand aliases."""
        clear()
        server.dell_poweredge(xy=(20, 60), width=12, style=Style())
        server.dell_idrac(xy=(40, 60), width=12, style=Style())
        server.dell_powerstore(xy=(60, 60), width=12, style=Style())
        server.dell_powerscale(xy=(80, 60), width=12, style=Style())
        server.vmware_hypervisor(xy=(20, 30), width=12, style=Style())
        server.vmware_virtual_machine(xy=(40, 30), width=12, style=Style())
        server.vmware_dvs(xy=(60, 30), width=12, style=Style())
        server.vmware_vsan(xy=(80, 30), width=12, style=Style())
        out = tmp_path / "test_server_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_server_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify ServerIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("vCenter", width=20, height=20, icon=ServerIcon.VMWARE_VCENTER), (20, 50))
        n2 = diag.add(Node("ESXi", width=20, height=20, icon=ServerIcon.VMWARE_ESXI_HOST), (50, 50))
        n3 = diag.add(Node("SAN", width=20, height=20, icon=ServerIcon.DELL_SAN_STORAGE), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_server.png"
        save(str(out))
        assert out.is_file()

    def test_server_vendor_and_os_icons_and_aliases(self, tmp_path: Path) -> None:
        """Verify official server vendor, chip, SBC, OS, virtualization, and storage icons."""
        clear()
        server.dell(xy=(15, 80), width=12, style=Style())
        server.hpe(xy=(35, 80), width=12, style=Style())
        server.asus(xy=(55, 80), width=12, style=Style())
        server.mac_mini(xy=(75, 80), width=12, style=Style())

        server.raspberry_pi(xy=(15, 60), width=12, style=Style())
        server.linux(xy=(35, 60), width=12, style=Style())
        server.ubuntu(xy=(55, 60), width=12, style=Style())
        server.windows(xy=(75, 60), width=12, style=Style())

        server.proxmox(xy=(15, 40), width=12, style=Style())
        server.kvm(xy=(35, 40), width=12, style=Style())
        server.synology(xy=(55, 40), width=12, style=Style())
        server.veeam(xy=(75, 40), width=12, style=Style())

        # Shorthand aliases
        server.rpi(xy=(15, 20), width=12, style=Style())
        server.tux(xy=(35, 20), width=12, style=Style())
        server.pve(xy=(55, 20), width=12, style=Style())
        server.zfs(xy=(75, 20), width=12, style=Style())

        out = tmp_path / "test_server_vendors_os.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_server_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Server icon file."""
        with pytest.raises(FileNotFoundError):
            SERVER_PROVIDER.get_icon_path("non_existent_server_icon_xyz")


class TestOriginalServerIcons:
    """Tests for Original Server (2D pastel) icon provider and architecture diagram enum."""

    def test_original_server_canonical_icons(self, tmp_path: Path) -> None:
        """Verify canonical 2D Original Server icons."""
        clear()
        original_server.rack_server(xy=(15, 75), width=12, style=Style(), variant="default")
        original_server.blade_chassis(xy=(35, 75), width=12, style=Style())
        original_server.tower_server(xy=(55, 75), width=12, style=Style())
        original_server.gpu_server(xy=(75, 75), width=12, style=Style())

        original_server.hci_appliance(xy=(15, 50), width=12, style=Style())
        original_server.bmc(xy=(35, 50), width=12, style=Style())
        original_server.fc_switch(xy=(55, 50), width=12, style=Style())
        original_server.san_storage(xy=(75, 50), width=12, style=Style())

        original_server.hypervisor_host(xy=(15, 25), width=12, style=Style())
        original_server.virtual_machine(xy=(35, 25), width=12, style=Style())
        original_server.management_server(xy=(55, 25), width=12, style=Style())
        original_server.host_cluster(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_original_server.png"
        save(str(out))
        assert out.is_file()

    def test_original_server_aliases(self, tmp_path: Path) -> None:
        """Verify Original Server shorthand aliases (including san_switch, esxi_host, vcenter, vsan)."""
        clear()
        original_server.san_switch(xy=(20, 60), width=12, style=Style())
        original_server.esxi_host(xy=(40, 60), width=12, style=Style())
        original_server.vm(xy=(60, 60), width=12, style=Style())
        original_server.vcenter(xy=(80, 60), width=12, style=Style())
        original_server.vmotion(xy=(20, 30), width=12, style=Style())
        original_server.vswitch(xy=(40, 30), width=12, style=Style())
        original_server.vsan(xy=(60, 30), width=12, style=Style())
        original_server.block_storage(xy=(80, 30), width=12, style=Style())
        out = tmp_path / "test_original_server_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_original_server_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify OriginalServerIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Manager", width=20, height=20, icon=OriginalServerIcon.MANAGEMENT_SERVER), (20, 50))
        n2 = diag.add(Node("Host", width=20, height=20, icon=OriginalServerIcon.HYPERVISOR_HOST), (50, 50))
        n3 = diag.add(Node("SAN SW", width=20, height=20, icon=OriginalServerIcon.SAN_SWITCH), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_server.png"
        save(str(out))
        assert out.is_file()

    def test_original_server_vendor_and_os_icons_and_aliases(self, tmp_path: Path) -> None:
        """Verify 2D pastel server vendor, chip, SBC, OS, virtualization, and storage icons."""
        clear()
        original_server.dell(xy=(15, 80), width=12, style=Style())
        original_server.hpe(xy=(35, 80), width=12, style=Style())
        original_server.mac_mini(xy=(55, 80), width=12, style=Style())
        original_server.beaglebone(xy=(75, 80), width=12, style=Style())

        original_server.linux(xy=(15, 60), width=12, style=Style())
        original_server.redhat(xy=(35, 60), width=12, style=Style())
        original_server.openbsd(xy=(55, 60), width=12, style=Style())
        original_server.windows(xy=(75, 60), width=12, style=Style())

        original_server.proxmox(xy=(15, 40), width=12, style=Style())
        original_server.kvm(xy=(35, 40), width=12, style=Style())
        original_server.synology(xy=(55, 40), width=12, style=Style())
        original_server.openzfs(xy=(75, 40), width=12, style=Style())

        # Shorthand aliases
        original_server.rpi(xy=(15, 20), width=12, style=Style())
        original_server.tux(xy=(35, 20), width=12, style=Style())
        original_server.pve(xy=(55, 20), width=12, style=Style())
        original_server.beagleboard(xy=(75, 20), width=12, style=Style())

        out = tmp_path / "test_original_server_vendors_os.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_original_server_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Original Server icon file."""
        with pytest.raises(FileNotFoundError):
            ORIGINAL_SERVER_PROVIDER.get_icon_path("non_existent_orig_server_icon_xyz")
