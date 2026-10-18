# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Facility (data centers, IX, telecom carriers, facility hardware) icon provider configuration."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

FACILITY_ALIASES: dict[str, str] = {
    "amat": "applied_materials",
    "asml_holding": "asml",
    "at_and_t": "att",
    "attokyo": "at_tokyo",
    "au": "kddi",
    "axis_camera": "axis",
    "centurylink": "lumen",
    "decix": "de_cix",
    "dlr": "digital_realty",
    "eqix": "equinix",
    "gf": "globalfoundries",
    "global_foundries": "globalfoundries",
    "hid": "hid_global",
    "hon_hai": "foxconn",
    "kyocera_corp": "kyocera",
    "liebert": "vertiv",
    "murata_mfg": "murata",
    "ntt_com": "ntt",
    "ntt_datacenter": "ntt_gdc",
    "ntt_docomo": "ntt",
    "orange_business": "orange",
    "rapidus_corp": "rapidus",
    "schneider": "schneider_electric",
    "t_systems": "deutsche_telekom",
    "taiwan_semiconductor": "tsmc",
    "tel": "tokyo_electron",
    "vantage": "vantage_dc",
}

FACILITY_PROVIDER = PngIconProvider(
    name="facility",
    package_name="icon_facility",
    asset_subdir="icons/facility",
    aliases=FACILITY_ALIASES,
)

_write = FACILITY_PROVIDER.write
