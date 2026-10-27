# Drawlib Facility Icons Guidelines (`lib-icons-facility`)

API specification and complete catalog for `drawlib.icons.facility` (`FacilityIcon`, **49** official colocation, IXP, telecom carrier, power/cooling, and semiconductor foundry brand icons) and `drawlib.icons.original_facility` (`OriginalFacilityIcon`, **86** flat 2D pastel icons: **49** brand twins + **37** vendor-neutral data center, power, telecom, and site concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import FacilityIcon, Node, OriginalFacilityIcon
from drawlib.icons import facility, facility_icon, original_facility, original_facility_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
facility.equinix((30, 25), width=9.0, style=Styles.Primary)
original_facility.equinix((55, 25), width=9.0, style=Styles.Primary)
original_facility.datacenter((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
facility_icon((30, 10), width=9.0, name="megaport", style=Styles.Primary)
original_facility_icon((55, 10), width=9.0, name="ups_power", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
colo_node = Node("Equinix IBX", width=24, height=18, icon=FacilityIcon.EQUINIX, icon_size=7.5)
ups_node = Node("2N Battery UPS", width=24, height=18, icon=OriginalFacilityIcon.UPS_POWER, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.facility` | `FacilityIcon` | **49** | `icon_facility` | Official logos for colocation operators, IXPs, global telecom carriers, power/HVAC OEMs, and semiconductor fabs. |
| `drawlib.icons.original_facility` | `OriginalFacilityIcon` | **86** (`49` + `37`) | `icon_original_facility` | Flat 2D pastel twins for all 49 brands plus **37 vendor-neutral data center, power, fiber & site concept icons**. |

---

## 2. Complete 49 Shared Brand Icons (`facility.*` & `original_facility.*`)

| Category | Count | Canonical Function Names (`facility.*` & `original_facility.*`) |
| :--- | :---: | :--- |
| **Colocation & Data Center Operators** | 10 | `at_tokyo`, `coresite`, `cyrusone`, `digital_realty`, `equinix`, `iron_mountain`, `ntt_gdc`, `qts`, `switch_dc`, `vantage_dc` |
| **Internet Exchanges (IXPs) & Cloud Interconnect** | 8 | `bbix`, `console_connect`, `de_cix`, `jpix`, `jpnap`, `linx`, `megaport`, `packetfabric` |
| **Global Telecom, Fiber & Satellite Carriers** | 12 | `att`, `colt`, `deutsche_telekom`, `iij`, `intelsat`, `kddi`, `lumen`, `ntt`, `orange`, `softbank`, `starlink`, `verizon` |
| **Power, Cooling, Racks, Cabling & Access Control** | 10 | `apc`, `axis`, `commscope`, `corning`, `eaton`, `hid_global`, `panduit`, `rittal`, `schneider_electric`, `vertiv` |
| **Semiconductor Foundries, Equipment & EMS** | 9 | `applied_materials`, `asml`, `foxconn`, `globalfoundries`, `kyocera`, `murata`, `rapidus`, `tokyo_electron`, `tsmc` |

---

## 3. Complete 37 Vendor-Neutral Facility Concept Icons (`original_facility.*` Only)

| Category | Count | Canonical Function Names (`original_facility.*` / `OriginalFacilityIcon.*`) |
| :--- | :---: | :--- |
| **Data Centers, Racks & Physical Security** | 8 | `colocation`, `datacenter`, `fire_suppression`, `patch_panel`, `rack_cabinet`, `security_gate`, `server_room`, `surveillance_camera` |
| **Power Generation, Grid & HVAC Cooling** | 7 | `cooling_hvac`, `generator`, `power_plant`, `solar_wind`, `substation`, `transmission_tower`, `ups_power` |
| **Telecom Outside Plant, Subsea & Satellite** | 6 | `cable_landing`, `cell_tower`, `fiber_optic`, `satellite_station`, `underground_conduit`, `utility_pole` |
| **Enterprise Offices, Public Buildings & Campuses** | 9 | `branch_office`, `campus`, `headquarters`, `home_office`, `hospital`, `public_building`, `retail_store`, `school`, `shared_office` |
| **Manufacturing, Cleanrooms & Logistics Fleet** | 7 | `cargo_plane`, `cargo_ship`, `cargo_truck`, `factory`, `semiconductor_fab`, `service_van`, `warehouse` |

```drawlib code=fold align=center file=icons_facility_rules_arch.png caption="Tier-IV Colocation Power & Fiber Interconnect Topology Using FacilityIcon and OriginalFacilityIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    FacilityIcon,
    Node,
    NodeGroup,
    OriginalFacilityIcon,
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

cls = d.add(
    Node("Subsea Cable\nLanding", width=24, height=18, icon=OriginalFacilityIcon.CABLE_LANDING, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
dc = d.add(NodeGroup(title="Equinix Colocation Data Hall", padding=4.5), xy=(42, 4))
mmr = dc.add(Node("Meet-Me Room\nPatch Panel", width=24, height=18, icon=OriginalFacilityIcon.PATCH_PANEL, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
rack = dc.add(Node("42U Server\nCabinet", width=24, height=18, icon=OriginalFacilityIcon.RACK_CABINET, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(cls, mmr, label="Dark Fiber", padding=1.5)
d.connect(mmr, rack, label="100G SMF", padding=1.5)
d.draw(xy=(4, 4))
save()
```
