# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_SERVER_ALIASES: dict[str, str] = {
    "accelerated_server": "gpu_server",
    "ai_server": "gpu_server",
    "backup_server": "backup_appliance",
    "blade_server": "blade_chassis",
    "block_storage_array": "san_storage",
    "checkpoint": "vm_snapshot",
    "cluster": "host_cluster",
    "compute_pool": "resource_pool",
    "dedup_appliance": "backup_appliance",
    "disk_array": "san_storage",
    "distributed_switch": "virtual_switch",
    "drs_cluster": "host_cluster",
    "dvs": "virtual_switch",
    "esxi_host": "hypervisor_host",
    "fibre_channel_switch": "fc_switch",
    "file_server": "nas_storage",
    "golden_image": "vm_template",
    "guest_os": "virtual_machine",
    "ha_cluster": "host_cluster",
    "hci_storage": "virtual_san",
    "hyperconverged_node": "hci_appliance",
    "idrac": "bmc_management",
    "ilo": "bmc_management",
    "ipmi": "bmc_management",
    "kvm_host": "hypervisor_host",
    "lto_tape": "tape_library",
    "lun": "datastore",
    "modular_chassis": "blade_chassis",
    "object_store": "object_storage",
    "out_of_band_management": "bmc_management",
    "pedestal_server": "tower_server",
    "physical_server": "rack_server",
    "s3_appliance": "object_storage",
    "san_switch": "fc_switch",
    "scale_out_nas": "nas_storage",
    "server": "rack_server",
    "shared_volume": "datastore",
    "snapshot": "vm_snapshot",
    "software_defined_storage": "virtual_san",
    "storage_array": "san_storage",
    "tape_archive": "tape_library",
    "tape_drive": "tape_library",
    "template": "vm_template",
    "vapp": "vm_group",
    "vcenter": "management_server",
    "vcpu_pool": "resource_pool",
    "virtualization_host": "hypervisor_host",
    "virtualization_manager": "management_server",
    "vm": "virtual_machine",
    "vm_folder": "vm_group",
    "vm_migration": "live_migration",
    "vmfs_datastore": "datastore",
    "vmotion": "live_migration",
    "vsan": "virtual_san",
    "vswitch": "virtual_switch",
    "x86_server": "rack_server",
}

ORIGINAL_SERVER_PROVIDER = PngIconProvider(
    name="original_server",
    package_name="icon_original_server",
    asset_subdir="icons/original_server",
    aliases=ORIGINAL_SERVER_ALIASES,
)

_write = ORIGINAL_SERVER_PROVIDER.write
