# Business & Original Business Icon Categories Plan

Create two new icon categories—`business` (official enterprise/B2B SaaS logos) and `original_business` (Drawlib Original pastel brand icons + enterprise abstract concept icons)—by first migrating existing business icons out of `workspace` / `original_workspace` and then adding 35 new brand logos and 19 new abstract concepts.

## 1. Execution Phases

| Phase | Scope | Deliverables |
| :--- | :--- | :--- |
| **Phase 1: Move & Register** | Move 10 brands + 7 concepts from `workspace` to `business` | `tools/icons_src/{business,original_business}/`, `tools/original_assets/business/`, `src/drawlib/icons.{business,original_business}`, `BusinessIcon`, `OriginalBusinessIcon`, unit tests |
| **Phase 2: Collect Original Logos** | Fetch official SVG reference logos for 35 new brands | `tools/original_assets/business/<brand>/<brand>.svg` |
| **Phase 3: Create `business` Icons** | Author 35 native Drawlib scripts from reference SVGs | `tools/icons_src/business/<brand>_default.py` (total 45 icons) |
| **Phase 4: Create `original_business` Icons** | Author 35 pastel brand icons + 19 abstract concept icons | `tools/icons_src/original_business/<name>_default.py` (total 71 icons) |

## 2. Target Inventory

### 2.1. Phase 1 — Migrated from `workspace` / `original_workspace`
- **Brands (10)**: `sap`, `salesforce`, `dynamics_365`, `servicenow`, `workday`, `hubspot`, `zendesk`, `shopify`, `stripe`, `docusign`
- **Abstract Concepts (7)**: `erp`, `crm`, `helpdesk`, `hr_portal`, `billing_invoice`, `e_signature`, `ecommerce_store`
- **Remaining in `workspace`**: 40 brands (and 17 concepts in `original_workspace` = 57 total)

### 2.2. Phase 2 & 3 — New Brand Logos for `business` (35 brands)
- **ERP / Finance / Procurement (7)**: `netsuite`, `odoo`, `concur`, `coupa`, `zuora`, `freee`, `moneyforward`
- **CRM / Marketing (5)**: `zoho`, `pipedrive`, `marketo`, `braze`, `sansan`
- **CS / ITSM (3)**: `intercom`, `freshdesk`, `genesys`
- **HR / Business Apps (4)**: `bamboohr`, `deel`, `smarthr`, `kintone`
- **Payments / FinTech (5)**: `paypal`, `square`, `adyen`, `plaid`, `paypay`
- **E-Commerce (3)**: `magento`, `woocommerce`, `bigcommerce`
- **CPaaS / Messaging (5)**: `twilio`, `sendgrid`, `mailgun`, `line`, `vonage`
- **CMS / Contract / Search (6)**: `contentful`, `sanity`, `strapi`, `wordpress`, `algolia`, `cloudsign`
Wait: 7 + 5 + 3 + 4 + 5 + 3 + 5 + 6 = 38! Let's check:
- ERP/Finance (7): `netsuite`, `odoo`, `concur`, `coupa`, `zuora`, `freee`, `moneyforward`
- CRM/Marketing (5): `zoho`, `pipedrive`, `marketo`, `braze`, `sansan`
- CS/ITSM (3): `intercom`, `freshdesk`, `genesys`
- HR/Business Apps (4): `bamboohr`, `deel`, `smarthr`, `kintone`
- Payments/FinTech (5): `paypal`, `square`, `adyen`, `plaid`, `paypay`
- E-Commerce (3): `magento`, `woocommerce`, `bigcommerce`
- CPaaS/Messaging (5): `twilio`, `sendgrid`, `mailgun`, `line`, `vonage`
- CMS/Contract/Search (6): `contentful`, `sanity`, `strapi`, `wordpress`, `algolia`, `cloudsign`
Total new brands = 38 (+ 10 moved = 48 brands).

### 2.3. Phase 4 — New Abstract Concepts for `original_business` (20 concepts)
- **Finance & Payment (5)**: `payment_gateway`, `accounting_ledger`, `bank_transfer`, `subscription_billing`, `tax_compliance`
- **Supply Chain & Order (5)**: `order_management`, `inventory_management`, `procurement`, `supply_chain`, `logistics_shipping`
- **Customer & Messaging (5)**: `marketing_automation`, `customer_data_platform`, `notification_gateway`, `call_center`, `loyalty_points`
- **Enterprise & B2B (6)**: `itsm`, `cms`, `contract_management`, `edi_exchange`, `partner_portal`, `approval_workflow`
Total concepts = 21 new + 7 moved = 28 concepts (+ 48 brands = 76 total in `original_business`).

## 3. Codebase Touchpoints
- **Source & Assets**:
  - `tools/original_assets/business/<brand>/`
  - `tools/icons_src/business/*_default.py`
  - `tools/icons_src/original_business/*_default.py`
  - `tools/release_assets/v0.3/icons/{business,original_business}/`
- **Codegen & Build**:
  - `tools/dcli/codegen/icons_build.py` (`PROVIDER_ALIASES`)
  - `tools/dcli/codegen/original_cloud_codegen.py` (`PROVIDER_LABELS`, `PROVIDER_ENUM_NAMES`)
  - `tools/dcli/codegen/cli.py` (`icon-business`, `icon-original-business`)
- **Library Facades & Diagrams**:
  - `src/drawlib/_icons/png_icons/{business,original_business}/` (`__init__.py`, `_base.py`, `_generated.py`)
  - `src/drawlib/_icons/png_icons/__init__.py`
  - `src/drawlib/_icons/__init__.py`
  - `src/drawlib/icons.py`
  - `src/drawlib/_diagrams/architecture/_icons.py` (`BusinessIcon`, `OriginalBusinessIcon`)
  - `src/drawlib/_diagrams/architecture/_types.py`
  - `src/drawlib/_diagrams/architecture/__init__.py`
  - `src/drawlib/diagrams/architecture.py`
  - `src/drawlib/_diagrams/sequence/_types.py`
  - `src/drawlib/_diagrams/sequence/_render_elements.py`
  - `src/drawlib/diagrams/sequence.py`
  - `src/drawlib/_diagrams/_common.py`
  - `src/drawlib/_release_assets.py` (via `./dcli release-assets sync`)
- **Rules & Tests**:
  - `src/drawlib/_rules/{api.md,lib_icons.md,lib_diagrams.md}`
  - `tests/drawlib/icons/{test_workspace.py,test_original_workspace.py,test_business.py,test_original_business.py}`
