# Drawlib Client Icons Guidelines (`lib-icons-client`)

API specification and complete catalog for `drawlib.icons.client` (`ClientIcon`, **60** official browser, OS, OEM, consumer media, and OT brand icons) and `drawlib.icons.original_client` (`OriginalClientIcon`, **92** flat 2D pastel icons: **60** brand twins + **32** vendor-neutral device, peripheral, POS, and robotics concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import ClientIcon, Node, OriginalClientIcon
from drawlib.icons import client, client_icon, original_client, original_client_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
client.chrome((30, 25), width=9.0, style=Styles.Primary)
original_client.chrome((55, 25), width=9.0, style=Styles.Primary)
original_client.smartphone((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
client_icon((30, 10), width=9.0, name="ios", style=Styles.Primary)
original_client_icon((55, 10), width=9.0, name="laptop", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
web_node = Node("Web Client", width=24, height=18, icon=ClientIcon.CHROME, icon_size=7.5)
pos_node = Node("POS Terminal", width=24, height=18, icon=OriginalClientIcon.POS_TERMINAL, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.client` | `ClientIcon` | **60** | `icon_client` | Official logos for web browsers, mobile/desktop OSs, PC/phone OEMs, smart home devices, and industrial OT vendors. |
| `drawlib.icons.original_client` | `OriginalClientIcon` | **92** (`60` + `32`) | `icon_original_client` | Flat 2D pastel twins for all 60 brands plus **32 vendor-neutral client device & endpoint concepts**. |

---

## 2. Complete 60 Shared Brand Icons (`client.*` & `original_client.*`)

| Category | Count | Canonical Function Names (`client.*` & `original_client.*`) |
| :--- | :---: | :--- |
| **Web Browsers** | 10 | `arc`, `brave`, `chrome`, `chromium`, `edge`, `firefox`, `opera`, `safari`, `tor_browser`, `vivaldi` |
| **Operating Systems & App Stores** | 10 | `android`, `app_store`, `chromeos`, `ios`, `linux`, `macos`, `microsoft_store`, `play_store`, `ubuntu`, `windows` |
| **PC, Mobile & Electronics OEMs** | 13 | `acer`, `apple`, `asus`, `dell`, `hp`, `lenovo`, `logitech`, `meta`, `microsoft`, `panasonic`, `samsung`, `sony`, `switchbot` |
| **Smart Home, Media & Gaming** | 10 | `alexa`, `amazon_fire`, `fire_tv`, `fitbit`, `kindle`, `netflix`, `nintendo`, `playstation`, `xbox`, `youtube` |
| **Printers, Scanners & Connectivity** | 7 | `bluetooth`, `brother`, `canon`, `epson`, `ricoh`, `usb`, `zebra` |
| **Automotive, Heavy Machinery & OT** | 10 | `abb`, `bmw`, `caterpillar`, `fanuc`, `honeywell`, `john_deere`, `komatsu`, `siemens`, `tesla`, `toyota` |

---

## 3. Complete 32 Vendor-Neutral Endpoint Concept Icons (`original_client.*` Only)

| Category | Count | Canonical Function Names (`original_client.*` / `OriginalClientIcon.*`) |
| :--- | :---: | :--- |
| **Personal Computing & Mobile Devices** | 5 | `desktop_pc`, `ereader`, `laptop`, `smartphone`, `tablet` |
| **Wearables, XR & Smart Home** | 6 | `game_console`, `smart_glasses`, `smart_ring`, `smart_speaker`, `smart_tv`, `smartwatch`, `vr_headset` |
| **Office Peripherals & USB Media** | 7 | `external_monitor`, `headset`, `ip_phone`, `keyboard_mouse`, `printer`, `projector`, `usb_drive`, `webcam` |
| **Retail POS, Identity & Scanners** | 6 | `barcode_scanner`, `kiosk_terminal`, `nfc_tag`, `pos_terminal`, `qr_code`, `smart_card` |
| **Automotive, Robotics & Industrial OT** | 6 | `connected_car`, `drone`, `gps_tracker`, `heavy_machinery`, `industrial_robot`, `plc_controller` |

```drawlib code=fold align=center file=icons_client_rules_arch.png caption="Omnichannel Client & Industrial Edge Ingestion Using ClientIcon and OriginalClientIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    ClientIcon,
    Node,
    NodeGroup,
    OriginalClientIcon,
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

clients = d.add(NodeGroup(title="Client Endpoints", padding=4.5), xy=(4, 4))
web = clients.add(Node("Chrome\nBrowser", width=24, height=18, icon=ClientIcon.CHROME, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
mobile = clients.add(Node("Mobile\nApp", width=24, height=18, icon=OriginalClientIcon.SMARTPHONE, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(52, 14))

pos = d.add(
    Node("Retail POS\nTerminal", width=24, height=18, icon=OriginalClientIcon.POS_TERMINAL, icon_size=7.5),
    xy=(102, 18),
)

d.connect(web, mobile, label="Sync", padding=1.5)
d.connect(mobile, pos, label="NFC Tap", padding=1.5)
d.draw(xy=(4, 4))
save()
```
