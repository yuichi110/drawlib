# Original Network Icons Plan (`drawlib.icons.original_network`)

## 1. Objective & Scope

Add 22 vendor-neutral, 2D flat Drawlib pastel network topology icons under `drawlib.icons.original_network` (`OriginalNetworkIcon`), plus 34 shorthand aliases.

- **Module**: `drawlib.icons.original_network`
- **Architecture Enum**: `OriginalNetworkIcon`
- **Release Asset Package**: `icon_original_network` (`tools/release_assets/v0.3/icons/original_network/`)
- **Visual Style**: Clean **2D flat** Drawlib Original aesthetic (`PASTEL_BLUE = "#86A4F7"`, `PASTEL_BLUE_LIGHT = "#ACC2FA"`, `PASTEL_GREEN = "#7AD69E"`, `WHITE = "#FFFFFF"`, `DARK = "#323A48"`, `ORIG_STROKE = 2.7`).
- **Rule on `original_cloud`**: Do NOT modify `tools/icons_src/original_cloud/router_default.py` or `switch_default.py` during this task; propose alignment options to the user after `original_network` is complete.

---

## 2. Canonical Icon Lineup (22 Icons)

| # | Canonical Name | Shorthand Aliases | Category | 2D Pastel Motif |
| :- | :--- | :--- | :--- | :--- |
| 1 | `router` | `branch_router`, `isr_router` | Routing | 2D circular disc (`PASTEL_BLUE` ring / `WHITE` center) + 4 `DARK` routing arrows (2 horizontal inward, 2 vertical outward) & `PASTEL_GREEN` center/status accent |
| 2 | `wan_router` | `sd_wan`, `edge_router` | Routing | 2D router disc/card (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` wireframe WAN globe in center & 4 routing arrows around it |
| 3 | `core_router` | `carrier_router`, `chassis_router` | Routing | Tall 2D multi-slot carrier chassis (`PASTEL_BLUE` frame, `WHITE` upper routing bay with 4 routing arrows, lower `WHITE` vertical blade slots & `PASTEL_GREEN` LEDs) |
| 4 | `l2_switch` | `switch`, `access_switch`, `workgroup_switch` | Switching | Wide 2D horizontal rack switch (`PASTEL_BLUE` body, `WHITE` inner panel) + 4 alternating left/right horizontal arrows & `PASTEL_GREEN` status LEDs |
| 5 | `l3_switch` | `multilayer_switch` | Switching | Square 2D switch card (`PASTEL_BLUE` outer frame, `WHITE` inner plate) + `PASTEL_GREEN` center circle & 8 radial outward `DARK` arrows |
| 6 | `datacenter_switch` | `spine_leaf_switch`, `fabric_switch` | Switching | Wide 2D spine/leaf switch (`PASTEL_BLUE` body) + crossing X-fabric arrows with horizontal arrow tips & `PASTEL_GREEN` center fabric hub |
| 7 | `core_switch` | `chassis_switch` | Switching | Tall 2D modular chassis (`PASTEL_BLUE` frame) + upper X-fabric switching bay & lower 8-way radial L3 star bay with `PASTEL_GREEN` accents |
| 8 | `optical_transport` | `dwdm`, `roadm`, `fiber_switch` | Optical/WAN | 2D optical shelf (`PASTEL_BLUE` body, `WHITE` optical ring) + `PASTEL_GREEN` prism triangle & 3 parallel horizontal wavelength arrows |
| 9 | `wireless_ap` | `ap`, `wifi_ap`, `access_point` | Wireless | 2D rounded AP unit (`PASTEL_BLUE` base) + `PASTEL_GREEN` transmitter dot & concentric `DARK` Wi-Fi radio wave arcs |
| 10 | `wireless_controller` | `wlc`, `wlan_controller` | Wireless | 2D controller rack box (`PASTEL_BLUE` lower bar with `PASTEL_GREEN` LEDs) + 3 converging control arrows & upper Wi-Fi radio waves |
| 11 | `wireless_router` | `wifi_router` | Wireless | 2D router body (`PASTEL_BLUE` with 4 routing arrows on `WHITE` panel) + 2 vertical antennas with `PASTEL_GREEN` tips & radio arcs |
| 12 | `firewall` | `network_firewall`, `ngfw` | Security | 2D staggered brick wall (`PASTEL_BLUE` & `PASTEL_BLUE_LIGHT` bricks, `DARK` mortar) + front `PASTEL_GREEN` & `WHITE` security shield |
| 13 | `vpn_gateway` | `vpn_concentrator`, `vpn` | Security | 2D horizontal encrypted tunnel pipe (`PASTEL_BLUE` / `WHITE`) + central `PASTEL_GREEN` padlock & left/right tunnel arrows |
| 14 | `ids_ips` | `ips`, `ids`, `intrusion_prevention` | Security | 2D network inspection barrier (`PASTEL_BLUE` frame, `WHITE` sensor ring) + `PASTEL_GREEN` shield blocking/inspecting a horizontal packet arrow |
| 15 | `nac_server` | `aaa_server`, `ise`, `radius_server` | Security | Tall 2D identity appliance (`PASTEL_BLUE` body, `WHITE` badge) + user silhouette & `PASTEL_GREEN` checkmark/key badge |
| 16 | `web_security` | `secure_web_gateway`, `swg`, `proxy_appliance` | Security | 2D `PASTEL_BLUE` wireframe globe (`DARK` meridians/parallels) + bottom-right `PASTEL_GREEN` & `WHITE` protective shield |
| 17 | `load_balancer` | `adc`, `traffic_manager` | Services | 2D appliance card (`PASTEL_BLUE` frame, `WHITE` inner plate) + 1 input arrow splitting into 3 fan-out arrows to `PASTEL_GREEN` target dots |
| 18 | `wan_cloud` | `internet_cloud`, `mpls_cloud`, `carrier_cloud` | WAN | 2D puffy `PASTEL_BLUE` cloud silhouette (`DARK` outline) + 3 `WHITE` / `PASTEL_GREEN` interconnected routing nodes inside |
| 19 | `ip_phone` | `voip_phone` | Endpoints | 2D desk VoIP phone (`PASTEL_BLUE` body, `PASTEL_BLUE_LIGHT` handset on left, `WHITE` LCD screen, `PASTEL_GREEN` call key & `DARK` keypad dots) |
| 20 | `voice_gateway` | `pbx`, `call_manager`, `sip_gateway` | Endpoints | 2D gateway card (`PASTEL_BLUE` frame, `WHITE` center) + `PASTEL_GREEN` phone handset framed by 4 cardinal routing arrows |
| 21 | `server` | `network_server`, `rack_server` | Endpoints | Tall 2D vertical server tower (`PASTEL_BLUE` body, `WHITE` drive slots, `PASTEL_GREEN` status LED & power button) |
| 22 | `client_pc` | `workstation`, `desktop_pc` | Endpoints | 2D flat desktop monitor (`PASTEL_BLUE` screen bezel, `WHITE` inner screen, `PASTEL_GREEN` accent) + stand & horizontal `WHITE` keyboard bar |
