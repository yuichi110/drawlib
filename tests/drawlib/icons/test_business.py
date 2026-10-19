# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Business icons."""

from pathlib import Path

from drawlib._icons.png_icons.business._base import BUSINESS_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, BusinessIcon, Node
from drawlib.icons import business
from drawlib.styles import Styles
from drawlib.types import Style

ALL_48_BUSINESS_ICONS = [
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


class TestBusinessIcons:
    """Tests for official Business icon provider and diagram enum."""

    def test_all_business_icons(self, tmp_path: Path) -> None:
        """Verify all 48 business SaaS and enterprise icons exist and render cleanly."""
        clear()
        assert len(ALL_48_BUSINESS_ICONS) == 48
        for idx, name in enumerate(ALL_48_BUSINESS_ICONS):
            assert hasattr(business, name), f"Missing business icon function: {name}"
            assert hasattr(BusinessIcon, name.upper()), f"Missing BusinessIcon enum: {name.upper()}"
            col = idx % 8
            row = idx // 8
            fn = getattr(business, name)
            fn(xy=(8 + col * 12, 85 - row * 14), width=8, style=Style(), variant="default")

        out = tmp_path / "test_business_all.png"
        save(str(out))
        assert out.is_file()

    def test_business_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical business icons."""
        clear()
        business.dynamics(xy=(15, 70), width=10, style=Style())
        business.sfdc(xy=(30, 70), width=10, style=Style())
        business.snow(xy=(45, 70), width=10, style=Style())
        business.mf(xy=(60, 70), width=10, style=Style())
        business.wp(xy=(75, 70), width=10, style=Style())
        business.woo(xy=(90, 70), width=10, style=Style())

        out = tmp_path / "test_business_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_business_architecture_enum(self, tmp_path: Path) -> None:
        """Verify BusinessIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("SAP", width=20, height=20, icon=BusinessIcon.SAP), (20, 50))
        n2 = diag.add(Node("Salesforce", width=20, height=20, icon=BusinessIcon.SALESFORCE), (50, 50))
        n3 = diag.add(Node("Stripe", width=20, height=20, icon=BusinessIcon.STRIPE), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_business.png"
        save(str(out))
        assert out.is_file()

    def test_business_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert BUSINESS_PROVIDER.name == "business"
        assert BUSINESS_PROVIDER.package_name == "icon_business"
        assert BUSINESS_PROVIDER.aliases["dynamics"] == "dynamics_365"
        assert BUSINESS_PROVIDER.aliases["mf"] == "moneyforward"
        assert BUSINESS_PROVIDER.aliases["sfdc"] == "salesforce"
        assert BUSINESS_PROVIDER.aliases["snow"] == "servicenow"
        assert BUSINESS_PROVIDER.aliases["woo"] == "woocommerce"
        assert BUSINESS_PROVIDER.aliases["wp"] == "wordpress"
