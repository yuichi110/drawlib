# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server, virtualization, and storage icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

SERVER_ALIASES: dict[str, str] = {
    "alma": "almalinux",
    "alpine": "alpine_linux",
    "arch": "arch_linux",
    "beagleboard": "beaglebone",
    "dell_ai_server": "dell_gpu_server",
    "dell_connectrix": "dell_fc_switch",
    "dell_datadomain": "dell_backup_appliance",
    "dell_ecs": "dell_object_storage",
    "dell_idrac": "dell_bmc_management",
    "dell_isilon": "dell_nas_storage",
    "dell_lto_tape": "dell_tape_library",
    "dell_mx_chassis": "dell_blade_chassis",
    "dell_openmanage": "dell_bmc_management",
    "dell_poweredge": "dell_rack_server",
    "dell_powermax": "dell_san_storage",
    "dell_powerscale": "dell_nas_storage",
    "dell_powerstore": "dell_san_storage",
    "dell_san_switch": "dell_fc_switch",
    "dell_server": "dell_rack_server",
    "dell_vxrail": "dell_hci_appliance",
    "esxi": "vmware",
    "hp_enterprise": "hpe",
    "incus": "lxc",
    "kali": "kali_linux",
    "lxd": "lxc",
    "macos": "apple",
    "microsoft_windows": "windows",
    "nix": "nixos",
    "opensuse": "suse",
    "proxmox_ve": "proxmox",
    "pve": "proxmox",
    "raspi": "raspberry_pi",
    "red_hat": "redhat",
    "rhel": "redhat",
    "riscv": "risc_v",
    "rocky": "rocky_linux",
    "rpi": "raspberry_pi",
    "sles": "suse",
    "tux": "linux",
    "vbox": "virtualbox",
    "vmware_drs_cluster": "vmware_cluster",
    "vmware_dvs": "vmware_vswitch",
    "vmware_ha_cluster": "vmware_cluster",
    "vmware_hci_storage": "vmware_vsan",
    "vmware_hypervisor": "vmware_esxi_host",
    "vmware_live_migration": "vmware_vmotion",
    "vmware_management_server": "vmware_vcenter",
    "vmware_nsx_switch": "vmware_vswitch",
    "vmware_physical_server": "vmware_rack_server",
    "vmware_san_nas": "vmware_storage_array",
    "vmware_vapp": "vmware_vm_group",
    "vmware_virtual_machine": "vmware_vm",
    "vmware_vm_snapshot": "vmware_snapshot",
    "vmware_vm_template": "vmware_template",
    "vmware_vmfs": "vmware_datastore",
    "wd": "western_digital",
    "windows_server": "windows",
    "zfs": "openzfs",
}

SERVER_PROVIDER = PngIconProvider(
    name="server",
    package_name="icon_server",
    asset_subdir="icons/server",
    aliases=SERVER_ALIASES,
)

_write = SERVER_PROVIDER.write
