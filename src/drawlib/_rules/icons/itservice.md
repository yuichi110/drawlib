# Drawlib IT Service Icons Guidelines (`lib-icons-itservice`)

API specification and complete catalog for `drawlib.icons.itservice` (`ItserviceIcon`, **44** official global consulting, Big Four advisory, and systems integrator brand icons) and `drawlib.icons.original_itservice` (`OriginalItserviceIcon`, **64** flat 2D pastel icons: **44** brand twins + **20** vendor-neutral ITSM, delivery, and program governance concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import ItserviceIcon, Node, OriginalItserviceIcon
from drawlib.icons import itservice, itservice_icon, original_itservice, original_itservice_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
itservice.ntt_data((30, 25), width=9.0, style=Styles.Primary)
original_itservice.ntt_data((55, 25), width=9.0, style=Styles.Primary)
original_itservice.pmo_office((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
itservice_icon((30, 10), width=9.0, name="accenture", style=Styles.Primary)
original_itservice_icon((55, 10), width=9.0, name="msp_operations", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
si_node = Node("Prime SI", width=24, height=18, icon=ItserviceIcon.NTT_DATA, icon_size=7.5)
msp_node = Node("24x7 MSP", width=24, height=18, icon=OriginalItserviceIcon.MSP_OPERATIONS, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.itservice` | `ItserviceIcon` | **44** | `icon_itservice` | Official brand marks for global consulting firms, Big Four advisories, and systems integrators (GSIs). |
| `drawlib.icons.original_itservice` | `OriginalItserviceIcon` | **64** (`44` + `20`) | `icon_original_itservice` | Flat 2D pastel twins for all 44 consulting/SI brands plus **20 vendor-neutral governance & ITSM concepts**. |

---

## 2. Complete 44 Shared Brand Icons (`itservice.*` & `original_itservice.*`)

| Category | Count | Canonical Function Names (`itservice.*` & `original_itservice.*`) |
| :--- | :---: | :--- |
| **Strategy & Big Four Advisory** | 9 | `accenture`, `bain`, `bcg`, `booz_allen`, `deloitte`, `ey`, `kpmg`, `mckinsey`, `pwc` |
| **Global Systems Integrators & Managed Infra** | 12 | `atos`, `capgemini`, `cgi`, `dxc`, `ibm`, `indra`, `kyndryl`, `leidos`, `rackspace`, `sopra_steria`, `t_systems`, `tietoevry` |
| **Japanese & APAC Systems Integrators** | 5 | `fujitsu`, `hitachi`, `nec`, `nri`, `ntt_data` |
| **Global Delivery & IT Services** | 7 | `cognizant`, `hcltech`, `infosys`, `ltimindtree`, `tcs`, `tech_mahindra`, `wipro` |
| **Digital Engineering & Cloud Native Consulting** | 5 | `endava`, `epam`, `globant`, `slalom`, `thoughtworks` |
| **BPO, Customer Operations & IT Staffing** | 6 | `adecco`, `concentrix`, `genpact`, `manpower`, `randstad`, `teksystems` |

---

## 3. Complete 20 Vendor-Neutral Governance & ITSM Concept Icons (`original_itservice.*` Only)

| Canonical Function (`original_itservice.*`) | `OriginalItserviceIcon` Enum | Governance / Delivery Role |
| :--- | :--- | :--- |
| `architect_lead` | `ARCHITECT_LEAD` | Principal / enterprise architect or technical review board |
| `bpo_center` | `BPO_CENTER` | Business process outsourcing (BPO) shared service center |
| `client_enterprise` | `CLIENT_ENTERPRISE` | Enterprise customer organization or executive sponsor |
| `dedicated_team` | `DEDICATED_TEAM` | Ring-fenced agile product engineering squad |
| `escalation_flow` | `ESCALATION_FLOW` | Tiered L1 $\to$ L2 $\to$ L3 incident escalation bridge |
| `it_consulting` | `IT_CONSULTING` | Technology strategy and advisory engagement |
| `joint_venture` | `JOINT_VENTURE` | Co-invested joint venture (JV) delivery entity |
| `msp_operations` | `MSP_OPERATIONS` | Managed Service Provider (MSP) 24x7 NOC/SRE operations |
| `offshore_lab` | `OFFSHORE_LAB` | Global delivery center (GDC) or nearshore/offshore lab |
| `org_hierarchy` | `ORG_HIERARCHY` | Organizational reporting tree and operating model |
| `pmo_office` | `PMO_OFFICE` | Program Management Office (PMO) tracking milestones & risk |
| `prime_contractor` | `PRIME_CONTRACTOR` | Primary contracting vendor accountable for delivery |
| `project_manager` | `PROJECT_MANAGER` | Engagement manager, scrum master, or delivery lead |
| `raci_matrix` | `RACI_MATRIX` | Responsible, Accountable, Consulted, Informed (RACI) matrix |
| `ses_engineer` | `SES_ENGINEER` | System Engineering Service (SES) resident specialist |
| `sla_contract` | `SLA_CONTRACT` | Service Level Agreement (SLA) and uptime target |
| `staff_augmentation` | `STAFF_AUGMENTATION` | Flexible specialist capacity embedded in internal teams |
| `steering_committee` | `STEERING_COMMITTEE` | Executive steering committee and program review board |
| `support_operator` | `SUPPORT_OPERATOR` | L1/L2 service desk operator or incident responder |
| `system_integrator` | `SYSTEM_INTEGRATOR` | Systems integrator (SI) coordinating multi-vendor delivery |

```drawlib code=fold align=center file=icons_itservice_rules_arch.png caption="Multi-Vendor SI Delivery & 24x7 MSP Governance Topology Using ItserviceIcon and OriginalItserviceIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    ItserviceIcon,
    Node,
    NodeGroup,
    OriginalItserviceIcon,
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

pmo = d.add(
    Node("Enterprise\nSponsor PMO", width=24, height=18, icon=OriginalItserviceIcon.PMO_OFFICE, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
ecosystem = d.add(NodeGroup(title="Prime SI & Managed Operations", padding=4.5), xy=(42, 4))
si = ecosystem.add(Node("Prime SI\n(NTT DATA)", width=24, height=18, icon=ItserviceIcon.NTT_DATA, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
msp = ecosystem.add(Node("24x7 MSP\nOperations", width=24, height=18, icon=OriginalItserviceIcon.MSP_OPERATIONS, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(pmo, si, label="Master SLA", padding=1.5)
d.connect(si, msp, label="Handover", padding=1.5)
d.draw(xy=(4, 4))
save()
```
