# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Business (ERP, CRM, ITSM, FinTech, E-Commerce, CPaaS, B2B SaaS) icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

BUSINESS_ALIASES: dict[str, str] = {
    "adobe_commerce": "magento",
    "adobe_marketo": "marketo",
    "bamboo_hr": "bamboohr",
    "bc": "bigcommerce",
    "big_commerce": "bigcommerce",
    "cloud_sign": "cloudsign",
    "cybozu_kintone": "kintone",
    "d365": "dynamics_365",
    "docu_sign": "docusign",
    "dynamics": "dynamics_365",
    "fresh_desk": "freshdesk",
    "genesys_cloud": "genesys",
    "line_messenger": "line",
    "mf": "moneyforward",
    "money_forward": "moneyforward",
    "ms_dynamics": "dynamics_365",
    "net_suite": "netsuite",
    "oracle_netsuite": "netsuite",
    "pay_pal": "paypal",
    "pay_pay": "paypay",
    "pipe_drive": "pipedrive",
    "sap_concur": "concur",
    "sap_erp": "sap",
    "send_grid": "sendgrid",
    "service_now": "servicenow",
    "sfdc": "salesforce",
    "smart_hr": "smarthr",
    "snow": "servicenow",
    "twilio_sendgrid": "sendgrid",
    "woo": "woocommerce",
    "woo_commerce": "woocommerce",
    "wp": "wordpress",
    "zoho_crm": "zoho",
}

BUSINESS_PROVIDER = PngIconProvider(
    name="business",
    package_name="icon_business",
    asset_subdir="icons/business",
    aliases=BUSINESS_ALIASES,
)

_write = BUSINESS_PROVIDER.write
