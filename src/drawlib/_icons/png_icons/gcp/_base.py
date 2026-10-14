# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

GCP_ALIASES: dict[str, str] = {
    "functions": "cloud_functions",
    "gce": "compute_engine",
    "gcs": "cloud_storage",
    "gke": "google_kubernetes_engine",
    "iam": "identity_and_access_management",
    "kms": "key_management_service",
    "vertexai": "vertex_ai",
    "vpc": "virtual_private_cloud",
    "load_balancing": "cloud_load_balancing",
    "cloud_pubsub": "pubsub",
}

GCP_PROVIDER = PngIconProvider(
    name="gcp",
    package_name="icon_gcp",
    asset_subdir="icons/gcp",
    aliases=GCP_ALIASES,
)

_write = GCP_PROVIDER.write
