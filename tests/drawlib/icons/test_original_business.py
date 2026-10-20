# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Original Business icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_business._base import (
    ORIGINAL_BUSINESS_PROVIDER,
)
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalBusinessIcon
from drawlib.icons import original_business
from drawlib.styles import Styles
from drawlib.types import Style

ALL_28_CONCEPT_ICONS = [
    "accounting_ledger",
    "approval_workflow",
    "bank_transfer",
    "billing_invoice",
    "call_center",
    "cms",
    "contract_management",
    "crm",
    "customer_data_platform",
    "e_signature",
    "ecommerce_store",
    "edi_exchange",
    "erp",
    "helpdesk",
    "hr_portal",
    "inventory_management",
    "itsm",
    "logistics_shipping",
    "loyalty_points",
    "marketing_automation",
    "notification_gateway",
    "order_management",
    "partner_portal",
    "payment_gateway",
    "procurement",
    "subscription_billing",
    "supply_chain",
    "tax_compliance",
]

ALL_48_BRAND_ICONS = [
    "adyen",
    "algolia",
    "bamboohr",
    "bigcommerce",
    "braze",
    "cloudsign",
    "concur",
    "contentful",
    "coupa",
    "deel",
    "docusign",
    "dynamics_365",
    "freee",
    "freshdesk",
    "genesys",
    "hubspot",
    "intercom",
    "kintone",
    "line",
    "magento",
    "mailgun",
    "marketo",
    "moneyforward",
    "netsuite",
    "odoo",
    "paypal",
    "paypay",
    "pipedrive",
    "plaid",
    "salesforce",
    "sanity",
    "sansan",
    "sap",
    "sendgrid",
    "servicenow",
    "shopify",
    "smarthr",
    "square",
    "strapi",
    "stripe",
    "twilio",
    "vonage",
    "woocommerce",
    "wordpress",
    "workday",
    "zendesk",
    "zoho",
    "zuora",
]


class TestOriginalBusinessIcons:
    """Tests for `drawlib.icons.original_business` and `OriginalBusinessIcon`."""

    def test_original_business_all_76_icons(self, tmp_path: Path) -> None:
        """Verify all 76 original business concepts and brand icons exist and render."""
        clear()
        all_76 = ALL_28_CONCEPT_ICONS + ALL_48_BRAND_ICONS
        assert len(all_76) == 76
        for idx, name in enumerate(all_76):
            assert hasattr(original_business, name), f"Missing canonical icon: {name}"
            assert hasattr(OriginalBusinessIcon, name.upper()), f"Missing enum: {name.upper()}"
            col = idx % 10
            row = idx // 10
            fn = getattr(original_business, name)
            fn(xy=(6 + col * 9.5, 90 - row * 11), width=6.5, style=Style(), variant="default")

        out = tmp_path / "test_original_business_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_business_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalBusinessIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(
            Node("CRM", width=20, height=20, icon=OriginalBusinessIcon.CRM),
            (20, 50),
        )
        n2 = diag.add(
            Node("ERP", width=20, height=20, icon=OriginalBusinessIcon.ERP),
            (50, 50),
        )
        n3 = diag.add(
            Node("SAP", width=20, height=20, icon=OriginalBusinessIcon.SAP),
            (80, 50),
        )
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_business.png"
        save(str(out))
        assert out.is_file()

    def test_original_business_provider_metadata(self) -> None:
        """Verify provider package name."""
        assert ORIGINAL_BUSINESS_PROVIDER.name == "original_business"
        assert ORIGINAL_BUSINESS_PROVIDER.package_name == "icon_original_business"
        assert ORIGINAL_BUSINESS_PROVIDER.asset_subdir == "icons/original_business"
