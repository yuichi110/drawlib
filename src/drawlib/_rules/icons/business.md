# Drawlib Business Icons Guidelines (`lib-icons-business`)

API specification and complete catalog for `drawlib.icons.business` (`BusinessIcon`, **48** official enterprise SaaS, CRM, ERP, FinTech, and e-commerce brand icons) and `drawlib.icons.original_business` (`OriginalBusinessIcon`, **76** flat 2D pastel icons: **48** brand twins + **28** vendor-neutral enterprise concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import BusinessIcon, Node, OriginalBusinessIcon
from drawlib.icons import business, business_icon, original_business, original_business_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
business.salesforce((30, 25), width=9.0, style=Styles.Primary)
original_business.salesforce((55, 25), width=9.0, style=Styles.Primary)
original_business.payment_gateway((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
business_icon((30, 10), width=9.0, name="stripe", style=Styles.Primary)
original_business_icon((55, 10), width=9.0, name="erp", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
crm_node = Node("Salesforce CRM", width=24, height=18, icon=BusinessIcon.SALESFORCE, icon_size=7.5)
erp_node = Node("Core ERP", width=24, height=18, icon=OriginalBusinessIcon.ERP, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.business` | `BusinessIcon` | **48** | `icon_business` | Official logos for CRM, ERP, HR, FinTech, payments, e-commerce, and ITSM platforms. |
| `drawlib.icons.original_business` | `OriginalBusinessIcon` | **76** (`48` + `28`) | `icon_original_business` | Flat 2D pastel twins for all 48 brands plus **28 vendor-neutral enterprise domain concepts**. |

---

## 2. Complete 48 Shared Brand Icons (`business.*` & `original_business.*`)

| Category | Count | Canonical Function Names (`business.*` & `original_business.*`) |
| :--- | :---: | :--- |
| **CRM, Sales & Marketing Automation** | 8 | `braze`, `dynamics_365`, `hubspot`, `marketo`, `pipedrive`, `salesforce`, `sansan`, `zoho` |
| **ERP, Accounting & Spend Management** | 7 | `concur`, `coupa`, `freee`, `moneyforward`, `netsuite`, `odoo`, `sap` |
| **HR, Payroll & People Operations** | 4 | `bamboohr`, `deel`, `smarthr`, `workday` |
| **FinTech, Payments & Subscription Billing** | 7 | `adyen`, `paypal`, `paypay`, `plaid`, `square`, `stripe`, `zuora` |
| **E-Commerce, Headless CMS & Search** | 9 | `algolia`, `bigcommerce`, `contentful`, `magento`, `sanity`, `shopify`, `strapi`, `woocommerce`, `wordpress` |
| **Customer Support, ITSM & Contact Center** | 5 | `freshdesk`, `genesys`, `intercom`, `servicenow`, `zendesk` |
| **Communications, E-Signature & Workflow** | 8 | `cloudsign`, `docusign`, `kintone`, `line`, `mailgun`, `sendgrid`, `twilio`, `vonage` |

---

## 3. Complete 28 Vendor-Neutral Business Concept Icons (`original_business.*` Only)

| Category | Count | Canonical Function Names (`original_business.*` / `OriginalBusinessIcon.*`) |
| :--- | :---: | :--- |
| **Finance, ERP, Billing & Procurement** | 8 | `accounting_ledger`, `bank_transfer`, `billing_invoice`, `erp`, `payment_gateway`, `procurement`, `subscription_billing`, `tax_compliance` |
| **CRM, Marketing & Commerce** | 7 | `cms`, `crm`, `customer_data_platform`, `ecommerce_store`, `loyalty_points`, `marketing_automation`, `order_management` |
| **Supply Chain, Logistics & Inventory** | 3 | `inventory_management`, `logistics_shipping`, `supply_chain` |
| **Operations, Legal, HR & Support** | 10 | `approval_workflow`, `call_center`, `contract_management`, `e_signature`, `edi_exchange`, `helpdesk`, `hr_portal`, `itsm`, `notification_gateway`, `partner_portal` |

```drawlib code=fold align=center file=icons_business_rules_arch.png caption="Order-to-Cash (O2C) Commerce & ERP Topology Using BusinessIcon and OriginalBusinessIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    BusinessIcon,
    Node,
    NodeGroup,
    OriginalBusinessIcon,
)
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

store = d.add(
    Node("Shopify\nStorefront", width=24, height=18, icon=BusinessIcon.SHOPIFY, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
core = d.add(NodeGroup(title="Order & Settlement Platform", padding=4.5), xy=(42, 4))
psp = core.add(Node("Stripe\nPayments", width=24, height=18, icon=BusinessIcon.STRIPE, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
erp = core.add(Node("General\nLedger ERP", width=24, height=18, icon=OriginalBusinessIcon.ACCOUNTING_LEDGER, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(store, psp, label="Charge", padding=1.5)
d.connect(psp, erp, label="Journal", padding=1.5)
d.draw(xy=(4, 4))
save()
```
