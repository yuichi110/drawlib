# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon functions."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.original_server._base import _write


def accelerated_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing accelerated server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="gpu_server", style=style, variant=variant)


def ai_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing ai server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="gpu_server", style=style, variant=variant)


def backup_appliance(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing backup appliance.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="backup_appliance", style=style, variant=variant)


def backup_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing backup server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="backup_appliance", style=style, variant=variant)


def blade_chassis(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing blade chassis.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="blade_chassis", style=style, variant=variant)


def blade_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing blade server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="blade_chassis", style=style, variant=variant)


def block_storage(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing block storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="san_storage", style=style, variant=variant)


def block_storage_array(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing block storage array.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="san_storage", style=style, variant=variant)


def bmc(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing bmc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="bmc", style=style, variant=variant)


def checkpoint(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing checkpoint.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_snapshot", style=style, variant=variant)


def cluster(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing cluster.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="host_cluster", style=style, variant=variant)


def compute_pool(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing compute pool.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="resource_pool", style=style, variant=variant)


def datastore(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing datastore.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datastore", style=style, variant=variant)


def dedup_appliance(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing dedup appliance.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="backup_appliance", style=style, variant=variant)


def disk_array(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing disk array.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="san_storage", style=style, variant=variant)


def distributed_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing distributed switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_switch", style=style, variant=variant)


def drs_cluster(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing drs cluster.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="host_cluster", style=style, variant=variant)


def dvs(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing dvs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_switch", style=style, variant=variant)


def esxi_host(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing esxi host.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hypervisor_host", style=style, variant=variant)


def fc_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing fc switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="fc_switch", style=style, variant=variant)


def fibre_channel_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing fibre channel switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="fc_switch", style=style, variant=variant)


def file_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing file server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nas_storage", style=style, variant=variant)


def file_storage(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing file storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nas_storage", style=style, variant=variant)


def golden_image(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing golden image.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_template", style=style, variant=variant)


def gpu_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing gpu server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="gpu_server", style=style, variant=variant)


def guest_os(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing guest os.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_machine", style=style, variant=variant)


def ha_cluster(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing ha cluster.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="host_cluster", style=style, variant=variant)


def hci_appliance(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing hci appliance.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hci_appliance", style=style, variant=variant)


def hci_storage(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing hci storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_san", style=style, variant=variant)


def host_cluster(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing host cluster.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="host_cluster", style=style, variant=variant)


def hyperconverged_node(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing hyperconverged node.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hci_appliance", style=style, variant=variant)


def hypervisor_host(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing hypervisor host.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hypervisor_host", style=style, variant=variant)


def kvm_host(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing kvm host.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hypervisor_host", style=style, variant=variant)


def live_migration(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing live migration.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="live_migration", style=style, variant=variant)


def lto_tape(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing lto tape.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tape_library", style=style, variant=variant)


def lun(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing lun.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datastore", style=style, variant=variant)


def management_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing management server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="management_server", style=style, variant=variant)


def modular_chassis(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing modular chassis.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="blade_chassis", style=style, variant=variant)


def nas_storage(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing nas storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nas_storage", style=style, variant=variant)


def object_storage(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing object storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="object_storage", style=style, variant=variant)


def object_store(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing object store.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="object_storage", style=style, variant=variant)


def pedestal_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing pedestal server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tower_server", style=style, variant=variant)


def physical_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing physical server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rack_server", style=style, variant=variant)


def rack_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing rack server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rack_server", style=style, variant=variant)


def resource_pool(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing resource pool.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="resource_pool", style=style, variant=variant)


def s3_appliance(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing s3 appliance.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="object_storage", style=style, variant=variant)


def san_storage(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing san storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="san_storage", style=style, variant=variant)


def san_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing san switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="fc_switch", style=style, variant=variant)


def scale_out_nas(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing scale out nas.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nas_storage", style=style, variant=variant)


def server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rack_server", style=style, variant=variant)


def shared_volume(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing shared volume.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datastore", style=style, variant=variant)


def snapshot(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing snapshot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_snapshot", style=style, variant=variant)


def software_defined_storage(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing software defined storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_san", style=style, variant=variant)


def storage_array(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing storage array.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="san_storage", style=style, variant=variant)


def tape_archive(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing tape archive.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tape_library", style=style, variant=variant)


def tape_drive(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing tape drive.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tape_library", style=style, variant=variant)


def tape_library(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing tape library.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tape_library", style=style, variant=variant)


def template(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing template.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_template", style=style, variant=variant)


def tower_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing tower server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tower_server", style=style, variant=variant)


def vapp(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vapp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_group", style=style, variant=variant)


def vcenter(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vcenter.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="management_server", style=style, variant=variant)


def vcpu_pool(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vcpu pool.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="resource_pool", style=style, variant=variant)


def virtual_machine(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing virtual machine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_machine", style=style, variant=variant)


def virtual_san(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing virtual san.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_san", style=style, variant=variant)


def virtual_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing virtual switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_switch", style=style, variant=variant)


def virtualization_host(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing virtualization host.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hypervisor_host", style=style, variant=variant)


def virtualization_manager(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing virtualization manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="management_server", style=style, variant=variant)


def vm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_machine", style=style, variant=variant)


def vm_folder(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vm folder.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_group", style=style, variant=variant)


def vm_group(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vm group.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_group", style=style, variant=variant)


def vm_migration(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vm migration.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="live_migration", style=style, variant=variant)


def vm_snapshot(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vm snapshot.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_snapshot", style=style, variant=variant)


def vm_template(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vm template.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vm_template", style=style, variant=variant)


def vmfs_datastore(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vmfs datastore.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datastore", style=style, variant=variant)


def vmotion(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vmotion.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="live_migration", style=style, variant=variant)


def vsan(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vsan.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_san", style=style, variant=variant)


def vswitch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing vswitch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="virtual_switch", style=style, variant=variant)


def x86_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Server concept icon representing x86 server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rack_server", style=style, variant=variant)
