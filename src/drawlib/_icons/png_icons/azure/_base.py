# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

AZURE_ALIASES: dict[str, str] = {
    "aad": "entra_id",
    "aca": "worker_container_app",
    "aci": "container_instances",
    "acr": "container_registries",
    "active_directory": "entra_id",
    "adf": "data_factories",
    "ai_search": "cognitive_search",
    "aks": "kubernetes_services",
    "api_management": "api_management_services",
    "apim": "api_management_services",
    "app_insights": "application_insights",
    "appgw": "application_gateways",
    "application_gateway": "application_gateways",
    "avd": "virtual_desktop",
    "azure_files": "storage_azure_files",
    "bastion": "bastions",
    "blob_storage": "storage_container",
    "cdn": "front_door_and_cdn_profiles",
    "container_apps": "worker_container_app",
    "data_factory": "data_factories",
    "event_grid": "event_grid_topics",
    "expressroute": "expressroute_circuits",
    "front_door": "front_door_and_cdn_profiles",
    "functions": "function_apps",
    "key_vault": "key_vaults",
    "kv": "key_vaults",
    "lb": "load_balancers",
    "log_analytics": "log_analytics_workspaces",
    "nat_gateway": "nat",
    "redis": "cache_redis",
    "synapse": "synapse_analytics",
    "virtual_machines": "virtual_machine",
    "vm": "virtual_machine",
    "vmss": "vm_scale_sets",
    "vnet": "virtual_networks",
    "waf": "web_application_firewall_policies_waf",
}

AZURE_PROVIDER = PngIconProvider(
    name="azure",
    package_name="icon_azure",
    asset_subdir="icons/azure",
    aliases=AZURE_ALIASES,
)

_write = AZURE_PROVIDER.write
