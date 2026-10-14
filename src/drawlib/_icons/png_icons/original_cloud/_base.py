# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_CLOUD_ALIASES: dict[str, str] = {
    "apigw": "api_gateway",
    "audit": "audit_compliance",
    "auth": "identity_auth",
    "backup": "backup_archive",
    "batch": "batch_job",
    "bi": "bi_dashboard",
    "browser": "web_browser",
    "bucket": "object_storage",
    "bus": "service_bus",
    "cache": "in_memory_cache",
    "cluster": "container_cluster",
    "cron": "scheduler",
    "db": "database",
    "ddos": "ddos_protection",
    "desktop": "desktop_app",
    "disk": "block_storage",
    "dwh": "data_warehouse",
    "etl": "etl_pipeline",
    "filestore": "file_storage",
    "function": "serverless_function",
    "graph_db": "graph_database",
    "iam": "identity_auth",
    "iap": "zero_trust_proxy",
    "iot": "iot_device",
    "k8s": "container_cluster",
    "kms": "secret_vault",
    "lb": "load_balancer",
    "mesh": "service_mesh",
    "mobile": "mobile_app",
    "mq": "message_queue",
    "nfs": "file_storage",
    "nosql": "nosql_database",
    "on_prem": "on_premises",
    "pubsub": "pub_sub",
    "queue": "message_queue",
    "rdbms": "database",
    "redis": "in_memory_cache",
    "replica": "db_replica",
    "search": "search_engine",
    "stream": "event_stream",
    "tls": "certificate_tls",
    "tsdb": "time_series_db",
    "users": "user_group",
    "vault": "secret_vault",
    "vector_db": "vector_database",
    "vm": "virtual_machine",
    "vpc": "virtual_network",
    "vpn": "vpn_tunnel",
    "worker": "batch_job",
    "workflow": "workflow_orchestrator",
    "zero_trust": "zero_trust_proxy",
}

ORIGINAL_CLOUD_PROVIDER = PngIconProvider(
    name="original_cloud",
    package_name="icon_original_cloud",
    asset_subdir="icons/original_cloud",
    aliases=ORIGINAL_CLOUD_ALIASES,
)

_write = ORIGINAL_CLOUD_PROVIDER.write
