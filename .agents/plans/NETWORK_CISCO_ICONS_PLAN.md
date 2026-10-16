# Network (Cisco) Icons Plan (`drawlib.icons.network`)

## 1. Objective & Scope

Add vendor-official network topology icons under `drawlib.icons.network` (`NetworkIcon`), starting with **22 canonical Cisco topology icons** (plus shorthand aliases), each supporting both **Classic 3D (`default` / `classic`)** and **Modern 2D (`modern`)** variants (44 icon scripts in `tools/icons_src/network/`).

- **Module**: `drawlib.icons.network`
- **Architecture Enum**: `NetworkIcon`
- **Release Asset Package**: `icon_network` (`tools/release_assets/v0.3/icons/network/`)
- **Variants**: `variant: Literal["default", "classic", "modern"] = "default"`
  - `"default"` and `"classic"` both resolve to `<name>_default.png` (Cisco Classic 3D Blue topology icon).
  - `"modern"` resolves to `<name>_modern.png` (Cisco Modern 2D flat badge icon).

---

## 2. Visual Language & Color Palette

All scripts use `setup_icon()` (`100x100` coordinate space, `(0,0)` bottom-left, `200` DPI supersampling -> normalized to `512x512` PNG with `460x460` inner bounding box).

- **Cisco Palette (`tools/icons_src/utils.py`)**:
  - `CISCO_BLUE = "#026E97"` (Classic front face / primary tone)
  - `CISCO_LIGHT_BLUE = "#3892B8"` (Classic top face / highlight tone)
  - `CISCO_DARK_BLUE = "#005073"` (Classic right/shadow face & Modern badge primary fill)
  - `CISCO_CYAN = "#00BCEB"` (Modern secondary accent stroke/fill)
  - `WHITE = "#FFFFFF"` (Crisp internal seams, arrows, and iconography)
- **Classic 3D (`*_default.py`)**:
  - Uses 3D oblique boxes (`draw_cisco_3d_box`) and 3D cylinders (`draw_cisco_3d_cylinder`) with `CISCO_LIGHT_BLUE` top face, `CISCO_BLUE` front face, `CISCO_DARK_BLUE` side face, `WHITE` internal edge seams/arrows, and `CISCO_DARK_BLUE` outer border.
- **Modern 2D (`*_modern.py`)**:
  - Uses a clean rounded-square badge (`78x78`, `shape_r=16.0`, `CISCO_DARK_BLUE` fill with `CISCO_CYAN` subtle accent elements and `WHITE` 2D line iconography).

---

## 3. Canonical Icon Lineup (22 Icons × 2 Variants = 44 Scripts)

| # | Canonical Name | Shorthand Aliases | Category | Classic (`default`/`classic`) Motif | Modern (`modern`) Motif |
| :- | :--- | :--- | :--- | :--- | :--- |
| 1 | `cisco_router` | `cisco_isr_router` | Routing | Flat 3D cylinder + 4 white top arrows (2 in, 2 out) | Rounded badge + 4-arrow routing cross |
| 2 | `cisco_wan_router` | `cisco_sd_wan`, `cisco_edge_router` | Routing | 3D cylinder router + WAN globe/arc on front | Badge + WAN globe & routing arrows |
| 3 | `cisco_core_router` | `cisco_carrier_router`, `cisco_chassis_router` | Routing | Tall multi-slot 3D chassis/stacked cylinder + top 4 arrows | Badge + tall multi-blade chassis & routing cross |
| 4 | `cisco_l2_switch` | `cisco_access_switch`, `cisco_workgroup_switch` | Switching | Flat 3D oblique box + 4 alternating horizontal top arrows | Badge + 4 alternating left/right horizontal arrows |
| 5 | `cisco_l3_switch` | `cisco_multilayer_switch` | Switching | 3D cube + center circle & 8 radial front arrows | Badge + center circle & 8 radial outward arrows |
| 6 | `cisco_nexus_switch` | `cisco_datacenter_switch` | Switching | Wide 3D DC box + X-cross fabric arrows | Badge + high-speed X-cross fabric arrows |
| 7 | `cisco_core_switch` | `cisco_chassis_switch` | Switching | Tall 3D modular chassis (line-card bays) + 8-way radial star | Badge + modular chassis bays & radial switch star |
| 8 | `cisco_optical_transport` | `cisco_dwdm`, `cisco_roadm` | Optical/WAN | 3D optical shelf + fiber ring & wavelength waves | Badge + optical ring & multi-wavelength beams |
| 9 | `cisco_wireless_ap` | `cisco_ap`, `cisco_wifi_ap` | Wireless | Flat 3D AP box + radiating wireless wave arcs | Badge + concentric Wi-Fi wave arcs & AP dot |
| 10 | `cisco_wireless_controller` | `cisco_wlc` | Wireless | 3D controller box + top switch arrows & front radio waves | Badge + controller bars & wireless waves |
| 11 | `cisco_wireless_router` | — | Wireless | 3D cylinder router + 2 rear antennas & 4 top arrows | Badge + dual antennas, waves & routing cross |
| 12 | `cisco_firewall` | `cisco_asa`, `cisco_firepower` | Security | 3D oblique brick-wall block with white mortar lines | Badge + shield & brick-wall pattern |
| 13 | `cisco_vpn_gateway` | `cisco_vpn_concentrator` | Security | 3D gateway box + tunnel & padlock emblem on front | Badge + encrypted tunnel & padlock |
| 14 | `cisco_ids_ips` | `cisco_ips` | Security | 3D sensor box + brick wall & target/lens emblem | Badge + shield & inspection sensor eye |
| 15 | `cisco_ise` | `cisco_aaa_server`, `cisco_nac` | Security | 3D server appliance + identity card/key-check emblem | Badge + identity user shield & checkmark |
| 16 | `cisco_web_security` | `cisco_wsa`, `cisco_umbrella` | Security | 3D appliance + wireframe globe & security shield | Badge + globe & protective security arc |
| 17 | `cisco_load_balancer` | `cisco_content_switch` | Services | 3D box + 1 input arrow splitting into 3 output arrows | Badge + 1-to-3 load-balancing arrow fork |
| 18 | `cisco_wan_cloud` | `cisco_mpls_cloud`, `cisco_internet_cloud` | WAN | 3D shaded Cisco Blue cloud with white contour/nodes | Badge + clean cloud silhouette & node links |
| 19 | `cisco_ip_phone` | `cisco_voip_phone` | Endpoints | 3D angled desk IP phone (handset, LCD, keypad) | Badge + VoIP desk phone handset & screen |
| 20 | `cisco_voice_gateway` | `cisco_cucm` | Endpoints | 3D voice router/gateway + handset & routing arrows | Badge + handset & call-routing arrows |
| 21 | `cisco_server` | `cisco_ucs_server` | Endpoints | 3D vertical server tower with drive bays | Badge + 3 stacked server blades |
| 22 | `cisco_client_pc` | `cisco_workstation` | Endpoints | 3D desktop monitor, system unit & keyboard | Badge + desktop monitor & stand |

---

## 4. Parallel Execution & Verification Workflow

1. **Phase 1 (Shared Foundation)**:
   - Add Cisco palette and geometry helpers (`draw_cisco_3d_box`, `draw_cisco_3d_cylinder`, `draw_cisco_arrow`, `draw_cisco_modern_badge`) to `tools/icons_src/utils.py`.
   - Wire `network` provider in `src/drawlib/_icons/png_icons/_base.py` (`variant="classic"` -> `"default"` support), `src/drawlib/_icons/png_icons/network/`, `src/drawlib/icons.py`, `src/drawlib/_diagrams/`, and `tools/dcli/codegen/`.
2. **Phase 2 (Parallel Subagents — 4 Batches)**:
   - Batch 1: Icons 1–6 (`cisco_router` through `cisco_nexus_switch` — 12 scripts)
   - Batch 2: Icons 7–11 (`cisco_core_switch` through `cisco_wireless_router` — 10 scripts)
   - Batch 3: Icons 12–16 (`cisco_firewall` through `cisco_web_security` — 10 scripts)
   - Batch 4: Icons 17–22 (`cisco_load_balancer` through `cisco_client_pc` — 12 scripts)
   - Each subagent writes its `.py` files and performs Stage 1 & Stage 2 grid inspection (`drawlib show ... -g`).
3. **Phase 3 (Unified Build, Codegen, Asset Sync & Contact Sheet Review)**:
   - Render all 44 icons, normalize to `512x512`, run `./dcli codegen icon-network`, build `icon_network.zip`, sync `_release_assets.py`, inspect contact sheet, update rules/tests, and run `./dcli code-check all` & `./dcli test target icons` / `diagrams`.
