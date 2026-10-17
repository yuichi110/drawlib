# Facility Icons Plan (`drawlib.icons.facility` & `drawlib.icons.original_facility`)

## 1. Objective & Scope

Add a dedicated physical site, building, data center, telecom carrier, and facility infrastructure icon suite under `drawlib.icons.facility` (`FacilityIcon`) for official operator/manufacturer logos, and `drawlib.icons.original_facility` (`OriginalFacilityIcon`) combining vendor-neutral building/site/facility concept icons with 2D flat pastel counterparts of the official logos.

- **Modules**:
  - `drawlib.icons.facility` (`FacilityIcon`) — 40 official data center, IX, telecom carrier, and facility equipment brand logos (+ shorthand aliases).
  - `drawlib.icons.original_facility` (`OriginalFacilityIcon`) — 24 vendor-neutral building, site, and facility concept icons + 40 2D flat pastel vendor counterparts (64 canonical icons total + shorthand aliases).
- **Release Asset Packages**:
  - `icon_facility` (`tools/release_assets/v0.3/icons/facility/`)
  - `icon_original_facility` (`tools/release_assets/v0.3/icons/original_facility/`)
- **Code Reuse & Independent PNG Folders**:
  - Overlapping hardware vendor `apc` reuses the Python drawing script from `server` (`tools/icons_src/server/apc_default.py` and `tools/icons_src/original_server/apc_default.py`).
  - Rendered PNG files and manifests remain completely independent inside `facility/` and `original_facility/`.

---

## 2. Canonical `facility` Icons (40 Official Operator, Carrier & Facility Hardware Logos)

| Category | # | Canonical Name | Operator / Brand | Shorthand Aliases / Overlap |
| :--- | :- | :--- | :--- | :--- |
| **1. Data Center & Colocation** | 1 | `equinix` | Equinix | `eqix` |
| | 2 | `digital_realty` | Digital Realty | `dlr` |
| | 3 | `ntt_gdc` | NTT Global Data Centers | `ntt_datacenter` |
| | 4 | `cyrusone` | CyrusOne | — |
| | 5 | `coresite` | CoreSite | — |
| | 6 | `vantage_dc` | Vantage Data Centers | `vantage` |
| | 7 | `iron_mountain` | Iron Mountain Data Centers | — |
| | 8 | `qts` | QTS Data Centers | — |
| | 9 | `switch_dc` | Switch Data Centers | — |
| | 10 | `at_tokyo` | AT TOKYO (アット東京) | `attokyo` |
| **2. Interconnection (NaaS), IX & Satellite** | 11 | `megaport` | Megaport | — |
| | 12 | `packetfabric` | PacketFabric | — |
| | 13 | `console_connect` | Console Connect (PCCW) | — |
| | 14 | `de_cix` | DE-CIX Internet Exchange | `decix` |
| | 15 | `linx` | LINX (London Internet Exchange) | — |
| | 16 | `jpnap` | JPNAP (Internet Multifeed) | — |
| | 17 | `jpix` | JPIX (Japan Internet Exchange) | — |
| | 18 | `bbix` | BBIX | — |
| | 19 | `starlink` | SpaceX Starlink | — |
| | 20 | `intelsat` | Intelsat Satellite Network | — |
| **3. Telecom & WAN Carriers** | 21 | `ntt` | NTT (NTT Com / NTT East & West) | `ntt_com`, `ntt_docomo` |
| | 22 | `kddi` | KDDI | `au` |
| | 23 | `softbank` | SoftBank | — |
| | 24 | `iij` | IIJ (Internet Initiative Japan) | — |
| | 25 | `colt` | Colt Technology Services | — |
| | 26 | `att` | AT&T Business | `at_and_t` |
| | 27 | `verizon` | Verizon Business | — |
| | 28 | `lumen` | Lumen Technologies (CenturyLink) | `centurylink` |
| | 29 | `orange` | Orange Business | `orange_business` |
| | 30 | `deutsche_telekom` | Deutsche Telekom / T-Systems | `t_systems` |
| **4. Facility Power, Rack, Cooling & Security** | 31 | `schneider_electric` | Schneider Electric | `schneider` |
| | 32 | `apc` | APC by Schneider Electric | Reuses `server/apc` |
| | 33 | `vertiv` | Vertiv (Liebert / Avocent) | `liebert` |
| | 34 | `eaton` | Eaton Power Management | — |
| | 35 | `rittal` | Rittal Racks & Cooling | — |
| | 36 | `panduit` | Panduit Physical Infrastructure | — |
| | 37 | `commscope` | CommScope Fiber & Cabling | — |
| | 38 | `corning` | Corning Optical Communications | — |
| | 39 | `axis` | Axis Communications (Network Cameras) | `axis_camera` |
| | 40 | `hid_global` | HID Global Physical Access Control | `hid` |

---

## 3. Canonical `original_facility` Icons (24 Concept Icons + 40 Pastel Logos = 64 Icons)

### Part A: Vendor-Neutral Building, Site & Facility Concept Icons (24 Icons)

| Category | # | Canonical Name | Shorthand Aliases | 2D Pastel Motif (`PASTEL_BLUE` / `PASTEL_GREEN` / `WHITE`) |
| :--- | :- | :--- | :--- | :--- |
| **1. IT & Telecom Sites** | 1 | `datacenter` | `data_center`, `dc_site` | Heavy windowless fortress building (`PASTEL_BLUE`) + `WHITE` / `PASTEL_GREEN` server rack bay |
| | 2 | `server_room` | `computer_room`, `mdf_idf` | Room interior frame (`WHITE`) containing dual `PASTEL_BLUE` 19-inch racks & `PASTEL_GREEN` LEDs |
| | 3 | `colocation` | `carrier_hotel`, `ix_site` | Multi-tenant DC building (`PASTEL_BLUE`) + `PASTEL_GREEN` cross-connect hub ring |
| | 4 | `cell_tower` | `base_station`, `radio_mast`, `5g_tower` | Lattice radio tower (`PASTEL_BLUE` / `DARK`) + radiating `PASTEL_GREEN` wireless signal arcs |
| | 5 | `satellite_station` | `earth_station`, `ground_station` | Parabolic satellite dish (`WHITE` / `PASTEL_BLUE`) pointing skyward with `PASTEL_GREEN` beam |
| | 6 | `cable_landing` | `submarine_cable`, `landing_station` | Coastal station (`WHITE` / `PASTEL_BLUE`) + undersea `PASTEL_GREEN` fiber cable under waves |
| **2. Offices & Workplaces** | 7 | `headquarters` | `hq`, `corporate_tower`, `skyscraper` | Tall stepped glass skyscraper (`PASTEL_BLUE` / `PASTEL_BLUE_LIGHT` + `WHITE` window grid) |
| | 8 | `branch_office` | `office`, `office_building` | Clean 3-story mid-rise office building (`WHITE` facade, `PASTEL_BLUE` roof & door) |
| | 9 | `campus` | `tech_campus`, `office_park` | Paired modern buildings (`PASTEL_BLUE` & `WHITE`) connected by a plaza + `PASTEL_GREEN` tree |
| | 10 | `shared_office` | `coworking`, `hot_desk` | Open office floor (`WHITE`) with shared desk silhouette & `PASTEL_GREEN` Wi-Fi arc |
| | 11 | `home_office` | `remote_worker`, `wfh`, `house` | Residential house with pitched roof (`PASTEL_BLUE` / `WHITE`) + `PASTEL_GREEN` Wi-Fi / laptop |
| | 12 | `mobile_site` | `field_vehicle`, `broadcast_van` | Field command van (`PASTEL_BLUE` / `WHITE`) with roof-mounted `PASTEL_GREEN` antenna dish |
| **3. Industrial & Public** | 13 | `factory` | `plant`, `smart_factory`, `manufacturing` | Sawtooth industrial roof (`PASTEL_BLUE` / `WHITE`) + smokestack & `PASTEL_GREEN` automation gear |
| | 14 | `warehouse` | `logistics_center`, `distribution_center` | Wide gable warehouse (`PASTEL_BLUE` roof, `WHITE` wall) + open bay with `PASTEL_GREEN` boxes |
| | 15 | `retail_store` | `shop`, `storefront`, `pos_store` | Storefront (`WHITE`) with striped `PASTEL_BLUE` / `PASTEL_GREEN` awning & display window |
| | 16 | `hospital` | `medical_center`, `clinic` | Multi-story medical building (`WHITE` / `PASTEL_BLUE`) + top `PASTEL_GREEN` medical cross badge |
| | 17 | `school` | `university`, `education_site` | Classic campus building (`WHITE` / `PASTEL_BLUE`) with pediment & `PASTEL_GREEN` clock / cap |
| | 18 | `public_building` | `government`, `bank`, `city_hall` | Classical columned building (`WHITE` pillars, `PASTEL_BLUE` pediment & stepped base) |
| **4. Facility Infrastructure** | 19 | `rack_cabinet` | `server_rack`, `19inch_rack` | Tall 42U rack cabinet (`PASTEL_BLUE` frame, `WHITE` rails) with `PASTEL_GREEN` status bar |
| | 20 | `ups_power` | `ups`, `battery_backup`, `pdu` | Power cabinet (`PASTEL_BLUE` / `WHITE`) + central `PASTEL_GREEN` lightning bolt |
| | 21 | `generator` | `backup_generator`, `diesel_generator` | Industrial generator engine housing (`PASTEL_BLUE`) + `PASTEL_GREEN` turbine / power bolt |
| | 22 | `cooling_hvac` | `crac`, `chiller`, `air_conditioning` | HVAC / fan unit (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` snowflake / cool air waves |
| | 23 | `security_gate` | `turnstile`, `access_gate`, `badge_gate` | Entry gate pillars (`PASTEL_BLUE` / `WHITE`) + `PASTEL_GREEN` swing barrier & badge sensor |
| | 24 | `surveillance_camera` | `cctv`, `security_camera`, `ip_camera` | Wall-mounted bullet/dome camera (`WHITE` / `PASTEL_BLUE`) with `PASTEL_GREEN` lens ring |

### Part B: 2D Flat Pastel Logos (40 Icons)
- Every icon in `facility` (1–40) has a matching 2D flat pastel counterpart in `original_facility`.
- **Mandatory Brand Color Rule**: Each `original_facility` vendor icon preserves its official brand color palette softened into Drawlib pastel tones with `DARK = "#323A48"` outlines (`w = 1.9`).

---

## 4. Implementation & Verification Workflow

1. **Phase 1 — Official Reference Collection & Provider Wiring**:
   - Download official SVG/PNG brand logos for all 40 `facility` icons into `tools/original_assets/facility/` and rasterize `.drawlib/scratch/facility_ref/<name>_ref.png`.
   - Wire `facility` (`FacilityIcon`) and `original_facility` (`OriginalFacilityIcon`) across `src/drawlib/_icons/png_icons/`, `src/drawlib/icons.py`, `src/drawlib/diagrams/architecture.py`, `src/drawlib/diagrams/sequence.py`, and `tools/dcli/codegen/`.
2. **Phase 2 — `facility` Official Logos (4 Parallel Batches of 10)**:
   - Reuse `apc_default.py` from `server` and author the remaining 39 scripts in `tools/icons_src/facility/<name>_default.py`.
   - Verify each with `-g` grid inspection against `_ref.png` and render the 40-icon `facility_icons_contact_sheet.png`.
3. **Phase 3 — `original_facility` Concepts (24) & Pastel Logos (40)**:
   - Author the 24 concept icons first, verify on a 24-icon concept sheet, then author the 40 2D flat pastel vendor logos.
   - Run `./dcli codegen icon-facility` and `./dcli codegen icon-original-facility`, sync `_cached_assets` and `_release_assets.py`, run `./dcli code-check all` and `./dcli test target icons diagrams`.
