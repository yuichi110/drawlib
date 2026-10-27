# Drawlib Network Icons Guidelines (`lib-icons-network`)

API specification and complete catalog for `drawlib.icons.network` (`NetworkIcon`, **70** icons: **48** official networking/CDN/proxy/VPN brand logos + **22** `cisco_*` topology icons with `"classic"` and `"modern"` variants) and `drawlib.icons.original_network` (`OriginalNetworkIcon`, **70** flat 2D pastel icons: **48** brand twins + **22** vendor-neutral L2/L3 network topology icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature, Twin Module Structure & Cisco `variant` Options

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument. In addition, the **22 `cisco_*` functions** in `drawlib.icons.network` accept `variant="default" | "classic" | "modern"`:

```python
from drawlib.diagrams.architecture import NetworkIcon, Node, OriginalNetworkIcon
from drawlib.icons import network, network_icon, original_network, original_network_icon
from drawlib.styles import Styles

# 1. Networking brand icons (48 identical function names in both suites)
network.cloudflare((25, 25), width=9.0, style=Styles.Primary)
original_network.cloudflare((50, 25), width=9.0, style=Styles.Primary)

# 2. Cisco topology icons support variant="classic" ("default") or variant="modern"
network.cisco_core_router((75, 25), width=9.0, style=Styles.Primary, variant="classic")
network.cisco_core_router((100, 25), width=9.0, style=Styles.Primary, variant="modern")

# 3. Vendor-neutral 2D pastel topology twin in original_network (no cisco_ prefix)
original_network.core_router((125, 25), width=9.0, style=Styles.Primary)

# 4. High-level ArchitectureDiagram Node integration via Enum
fw_node = Node("Perimeter FW", width=24, height=18, icon=NetworkIcon.CISCO_FIREWALL, icon_size=7.5)
sw_node = Node("L3 Switch", width=24, height=18, icon=OriginalNetworkIcon.L3_SWITCH, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.network` | `NetworkIcon` | **70** (`48` + `22` `cisco_*`) | `icon_network` | Official networking vendor/OSS logos + 22 Cisco L2/L3 topology icons (`variant="classic" \| "modern"`). |
| `drawlib.icons.original_network` | `OriginalNetworkIcon` | **70** (`48` + `22` concepts) | `icon_original_network` | Flat 2D pastel twins for all 48 brands + 22 vendor-neutral network topology icons. |

---

## 2. Complete 48 Shared Networking Brand Icons (`network.*` & `original_network.*`)

| Category | Count | Canonical Function Names (`network.*` & `original_network.*`) |
| :--- | :---: | :--- |
| **Enterprise & Campus Network Hardware Vendors** | 15 | `arista`, `aruba`, `asus`, `cisco`, `d_link`, `frrouting`, `juniper`, `linksys`, `meraki`, `mikrotik`, `netgear`, `openwrt`, `tp_link`, `ubiquiti`, `yamaha` |
| **Next-Gen Firewalls (NGFW), Zero-Trust VPN & SASE** | 11 | `checkpoint`, `fortinet`, `netbird`, `opnsense`, `openvpn`, `palo_alto`, `pfsense`, `tailscale`, `wireguard`, `zerotier`, `zscaler` |
| **CDNs, Load Balancers, Reverse Proxies & API Gateways** | 12 | `akamai`, `apisix`, `caddy`, `cloudflare`, `f5`, `fastly`, `haproxy`, `kong`, `nginx`, `squid`, `traefik`, `varnish` |
| **DNS Servers, Ad-Blockers, TLS CAs & Domain Registrars** | 10 | `adguard`, `bind`, `digicert`, `godaddy`, `lets_encrypt`, `namecheap`, `pi_hole`, `porkbun`, `powerdns`, `unbound` |

---

## 3. Complete 22 Network Topology Icons (`network.cisco_*` vs. `original_network.*`)

*(Note: `network.cisco_ise` maps to `original_network.nac_server`, and `network.cisco_nexus_switch` maps to `original_network.datacenter_switch`.)*

| `network.cisco_*` (`classic` / `modern`) | `NetworkIcon` Enum | `original_network.*` Twin | `OriginalNetworkIcon` Enum | Network Topology Role |
| :--- | :--- | :--- | :--- | :--- |
| `cisco_client_pc` | `CISCO_CLIENT_PC` | `client_pc` | `CLIENT_PC` | End-user desktop client host |
| `cisco_core_router` | `CISCO_CORE_ROUTER` | `core_router` | `CORE_ROUTER` | High-capacity backbone BGP/MPLS router |
| `cisco_core_switch` | `CISCO_CORE_SWITCH` | `core_switch` | `CORE_SWITCH` | Campus or distribution core chassis switch |
| `cisco_firewall` | `CISCO_FIREWALL` | `firewall` | `FIREWALL` | Perimeter L3/L4/L7 stateful firewall |
| `cisco_ids_ips` | `CISCO_IDS_IPS` | `ids_ips` | `IDS_IPS` | Intrusion detection and prevention sensor |
| `cisco_ip_phone` | `CISCO_IP_PHONE` | `ip_phone` | `IP_PHONE` | VoIP desk telephone endpoint |
| `cisco_ise` | `CISCO_ISE` | `nac_server` | `NAC_SERVER` | Network Access Control (NAC / Cisco ISE) |
| `cisco_l2_switch` | `CISCO_L2_SWITCH` | `l2_switch` | `L2_SWITCH` | Access-layer Ethernet VLAN switch |
| `cisco_l3_switch` | `CISCO_L3_SWITCH` | `l3_switch` | `L3_SWITCH` | Multilayer inter-VLAN routing switch |
| `cisco_load_balancer` | `CISCO_LOAD_BALANCER` | `load_balancer` | `LOAD_BALANCER` | Server load balancer / ADC appliance |
| `cisco_nexus_switch` | `CISCO_NEXUS_SWITCH` | `datacenter_switch` | `DATACENTER_SWITCH` | Leaf-spine data center fabric switch |
| `cisco_optical_transport` | `CISCO_OPTICAL_TRANSPORT` | `optical_transport` | `OPTICAL_TRANSPORT` | DWDM / fiber-optic metro transport node |
| `cisco_router` | `CISCO_ROUTER` | `router` | `ROUTER` | Standard branch or edge IP router |
| `cisco_server` | `CISCO_SERVER` | `server` | `SERVER` | Rack or tower application server host |
| `cisco_voice_gateway` | `CISCO_VOICE_GATEWAY` | `voice_gateway` | `VOICE_GATEWAY` | SIP / PSTN voice gateway |
| `cisco_vpn_gateway` | `CISCO_VPN_GATEWAY` | `vpn_gateway` | `VPN_GATEWAY` | Site-to-site IPsec / SSL VPN concentrator |
| `cisco_wan_cloud` | `CISCO_WAN_CLOUD` | `wan_cloud` | `WAN_CLOUD` | Public Internet, MPLS carrier, or ISP transit |
| `cisco_wan_router` | `CISCO_WAN_ROUTER` | `wan_router` | `WAN_ROUTER` | SD-WAN / wide-area edge router |
| `cisco_web_security` | `CISCO_WEB_SECURITY` | `web_security` | `WEB_SECURITY` | Secure web gateway (SWG) proxy |
| `cisco_wireless_ap` | `CISCO_WIRELESS_AP` | `wireless_ap` | `WIRELESS_AP` | Wi-Fi wireless access point (AP) |
| `cisco_wireless_controller` | `CISCO_WIRELESS_CONTROLLER` | `wireless_controller` | `WIRELESS_CONTROLLER` | Centralized WLAN controller (WLC) |
| `cisco_wireless_router` | `CISCO_WIRELESS_ROUTER` | `wireless_router` | `WIRELESS_ROUTER` | SOHO integrated Wi-Fi gateway router |

```drawlib code=fold align=center file=icons_network_rules_arch.png caption="Enterprise Perimeter & Campus Network Topology Using NetworkIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, NetworkIcon, Node, NodeGroup
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

wan = d.add(
    Node("Cloudflare\nAnycast Edge", width=24, height=18, icon=NetworkIcon.CLOUDFLARE, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
dmz = d.add(NodeGroup(title="Corporate DMZ & Core Network", padding=4.5), xy=(42, 4))
fw = dmz.add(Node("Cisco Firewall\n(ASA / NGFW)", width=24, height=18, icon=NetworkIcon.CISCO_FIREWALL, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(14, 14))
sw = dmz.add(Node("Cisco L3\nCore Switch", width=24, height=18, icon=NetworkIcon.CISCO_L3_SWITCH, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(54, 14))

d.connect(wan, fw, label="BGP", padding=1.5)
d.connect(fw, sw, label="10GbE", padding=1.5)
d.draw(xy=(4, 4))
save()
```
