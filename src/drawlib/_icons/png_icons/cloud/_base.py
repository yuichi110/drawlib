# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud (hyperscalers, cloud companies, global hosting/VPS/edge, modern PaaS/BaaS, Japan cloud) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

CLOUD_ALIASES: dict[str, str] = {
    "alibaba_group": "alibaba",
    "aliyun": "alibaba_cloud",
    "alphabet": "google",
    "amazon_corp": "amazon",
    "amazon_web_services": "aws",
    "cf": "cloudflare",
    "do": "digitalocean",
    "fjcloud": "nifcloud",
    "flyio": "fly_io",
    "gcp": "google_cloud",
    "gmo_conoha": "conoha",
    "huawei_corp": "huawei",
    "idcf_cloud": "idcf",
    "kagoya_cloud": "kagoya",
    "microsoft_azure": "azure",
    "ms_azure": "azure",
    "oci": "oracle_cloud",
    "oracle_corp": "oracle",
    "ovh": "ovhcloud",
    "railway_app": "railway",
    "render_cloud": "render",
    "sakura_cloud": "sakura",
    "sakura_internet": "sakura",
    "tencent_corp": "tencent",
}

CLOUD_PROVIDER = PngIconProvider(
    name="cloud",
    package_name="icon_cloud",
    asset_subdir="icons/cloud",
    aliases=CLOUD_ALIASES,
)

_write = CLOUD_PROVIDER.write
