# Client Icons Plan (`drawlib.icons.client` & `drawlib.icons.original_client`)

## 1. Objective & Scope

Add a dedicated web browser, client operating system, PC/mobile OEM, smart device, streaming client, connected car, heavy machinery, factory automation, peripheral, printer, and client connectivity icon suite under `drawlib.icons.client` (`ClientIcon`) for official brand and standard logos, and `drawlib.icons.original_client` (`OriginalClientIcon`) combining vendor-neutral client device & field endpoint concept icons with 2D flat pastel counterparts of the official logos.

- **Modules**:
  - `drawlib.icons.client` (`ClientIcon`) — 60 official web browser, client OS, app store, PC/mobile OEM, smart device, wearable, gaming, streaming, connected car, heavy machinery, factory automation, peripheral, printer, and connectivity logos (+ 73 shorthand aliases = 133 functions).
  - `drawlib.icons.original_client` (`OriginalClientIcon`) — 30 vendor-neutral client device, display, smart home, vehicle, machinery, industrial & token concept icons + 60 2D flat pastel vendor counterparts (90 canonical icons total + shorthand aliases).
- **Release Asset Packages**:
  - `icon_client` (`tools/release_assets/v0.3/icons/client/`)
  - `icon_original_client` (`tools/release_assets/v0.3/icons/original_client/`)
- **Code Reuse & Independent PNG Folders**:
  - Overlapping OS and PC OEM brands (`windows`, `linux`, `ubuntu`, `apple`, `dell`, `lenovo`, `asus`) reuse the Python drawing scripts from `server` (`tools/icons_src/server/<name>_default.py` and `tools/icons_src/original_server/<name>_default.py`).
  - Rendered PNG files and manifests remain completely independent inside `client/` and `original_client/`.

---

## 2. Canonical `client` Icons (60 Official Browser, OS, Device, Smart Home, Gaming, Car, Industrial & Peripheral Logos)

| Category | # | Canonical Name | Product / Brand | Shorthand Aliases / Overlap |
| :--- | :- | :--- | :--- | :--- |
| **1. Web Browsers** | 1 | `chrome` | Google Chrome | `google_chrome` |
| | 2 | `safari` | Apple Safari | `apple_safari` |
| | 3 | `edge` | Microsoft Edge | `microsoft_edge`, `ms_edge` |
| | 4 | `firefox` | Mozilla Firefox | `mozilla_firefox` |
| | 5 | `brave` | Brave Browser | `brave_browser` |
| | 6 | `opera` | Opera Browser | `opera_browser` |
| | 7 | `vivaldi` | Vivaldi Browser | `vivaldi_browser` |
| | 8 | `arc` | Arc Browser | `arc_browser` |
| | 9 | `tor_browser` | Tor Browser | `tor` |
| | 10 | `chromium` | Chromium | `chromium_browser` |
| **2. Client OS & App Stores** | 11 | `windows` | Microsoft Windows 11 | `windows_11`, `ms_windows` (reuses `server/windows`) |
| | 12 | `macos` | Apple macOS (Finder) | `mac_os`, `finder` |
| | 13 | `ios` | Apple iOS | `ipados` |
| | 14 | `android` | Google Android | `google_android` |
| | 15 | `chromeos` | Google ChromeOS | `chrome_os`, `chromebook_os` |
| | 16 | `linux` | Linux (Tux) | `linux_desktop` (reuses `server/linux`) |
| | 17 | `ubuntu` | Ubuntu Desktop | `ubuntu_desktop` (reuses `server/ubuntu`) |
| | 18 | `app_store` | Apple App Store | `apple_app_store` |
| | 19 | `play_store` | Google Play Store | `google_play`, `google_play_store` |
| | 20 | `microsoft_store` | Microsoft Store | `ms_store` |
| **3. PC & Mobile Device Brands** | 21 | `apple` | Apple (Mac / iPhone / iPad) | `mac`, `iphone_brand` (reuses `server/apple`) |
| | 22 | `microsoft` | Microsoft (Surface / Client) | `surface`, `ms` |
| | 23 | `samsung` | Samsung (Galaxy / Displays) | `galaxy` |
| | 24 | `sony` | Sony (Xperia / Audio / Client) | `xperia` |
| | 25 | `panasonic` | Panasonic (Let's note / Toughbook) | `toughbook`, `lets_note` |
| | 26 | `dell` | Dell Client (Latitude / XPS) | `dell_client` (reuses `server/dell`) |
| | 27 | `hp` | HP Inc. (EliteBook / Pavilion) | `hp_inc` |
| | 28 | `lenovo` | Lenovo (ThinkPad) | `thinkpad` (reuses `server/lenovo`) |
| | 29 | `asus` | ASUS (Zenbook / ROG) | `zenbook` (reuses `server/asus`) |
| | 30 | `acer` | Acer (Swift / Aspire) | — |
| **4. Smart Devices, Wearables, Gaming & Streaming** | 31 | `kindle` | Amazon Kindle | `amazon_kindle` |
| | 32 | `amazon_fire` | Amazon Fire / Kindle Fire / Fire OS | `kindle_fire`, `fire_tablet`, `fire_os` |
| | 33 | `fire_tv` | Amazon Fire TV | `amazon_fire_tv`, `fire_tv_stick` |
| | 34 | `alexa` | Amazon Alexa / Echo | `amazon_alexa`, `echo`, `amazon_echo` |
| | 35 | `fitbit` | Fitbit (Wearables) | `google_fitbit` |
| | 36 | `switchbot` | SwitchBot (Smart Home) | `switch_bot` |
| | 37 | `netflix` | Netflix (Streaming Client) | — |
| | 38 | `youtube` | YouTube (Streaming Client) | `yt` |
| | 39 | `nintendo` | Nintendo (Switch / Consoles) | `switch`, `nintendo_switch` |
| | 40 | `playstation` | PlayStation (PS5 / PS4 / PSN) | `play_station`, `ps`, `ps5`, `ps4` |
| | 41 | `xbox` | Microsoft Xbox | `xbox_series`, `xbox_one` |
| **5. Connected Cars, Heavy Machinery & Factory Automation** | 42 | `toyota` | Toyota (Connected Car / Mobility) | `toyota_motor` |
| | 43 | `tesla` | Tesla (EV / Software-Defined Vehicle) | `tesla_motors` |
| | 44 | `bmw` | BMW (ConnectedDrive / Digital Car Key) | `bmw_connected` |
| | 45 | `caterpillar` | Caterpillar (CAT Heavy Machinery) | `cat` |
| | 46 | `komatsu` | Komatsu (Smart Construction / Heavy Machinery) | `komatsu_ltd` |
| | 47 | `john_deere` | John Deere (Precision Agriculture / Tractors) | `deere` |
| | 48 | `fanuc` | FANUC (Industrial Robots / CNC) | `fanuc_robot` |
| | 49 | `siemens` | Siemens (Factory Automation / SIMATIC PLC) | `simatic` |
| | 50 | `abb` | ABB (Industrial Robotics / Drives) | `abb_robotics` |
| **6. Peripherals, Printers & Connectivity** | 51 | `logitech` | Logitech / Logicool | `logicool` |
| | 52 | `canon` | Canon (Printers / Cameras) | — |
| | 53 | `epson` | Epson (Printers / Projectors) | — |
| | 54 | `brother` | Brother (Label / Office Printers) | — |
| | 55 | `ricoh` | Ricoh (MFPs / Office Devices) | — |
| | 56 | `zebra` | Zebra Technologies (Scanners / Handhelds) | `zebra_scanner` |
| | 57 | `honeywell` | Honeywell (Industrial Terminals) | `honeywell_scanner` |
| | 58 | `meta` | Meta (Quest VR / Smart Glasses) | `meta_quest`, `oculus` |
| | 59 | `bluetooth` | Bluetooth SIG | `ble` |
| | 60 | `usb` | USB-IF (Universal Serial Bus) | `usb_c` |

---

## 3. Canonical `original_client` Icons (30 Concept Icons + 60 Pastel Logos = 90 Icons)

### Part A: Vendor-Neutral Client Device, Display, Smart Home, Vehicle, Machinery & Token Concept Icons (30 Icons)

| Category | # | Canonical Name | Shorthand Aliases | 2D Pastel Motif (`PASTEL_BLUE` / `PASTEL_GREEN` / `WHITE`) |
| :--- | :- | :--- | :--- | :--- |
| **1. Personal Computers & Mobile** | 1 | `desktop_pc` | `pc`, `workstation` | Desktop tower + monitor (`WHITE` screen, `PASTEL_BLUE` stand/tower) + `PASTEL_GREEN` LED |
| | 2 | `laptop` | `notebook_pc`, `macbook` | Open clamshell laptop (`WHITE` screen, `PASTEL_BLUE` base) + `PASTEL_GREEN` screen bar |
| | 3 | `smartphone` | `mobile_phone`, `cell_phone` | Vertical phone bezel (`WHITE` screen, `PASTEL_BLUE` body) + `PASTEL_GREEN` app badge |
| | 4 | `tablet` | `ipad`, `slate_tablet` | Wide/portrait tablet (`WHITE` screen, `PASTEL_BLUE` frame) + `PASTEL_GREEN` stylus / widget |
| | 5 | `ereader` | `ebook_reader`, `digital_paper` | E-ink reader (`WHITE` paper screen, `PASTEL_BLUE` bezel) + `PASTEL_GREEN` bookmark / page lines |
| | 6 | `smartwatch` | `wearable`, `fitness_watch` | Rounded watch dial (`WHITE` face, `PASTEL_BLUE` straps) + `PASTEL_GREEN` activity ring |
| | 7 | `vr_headset` | `xr_headset`, `ar_glasses`, `hmd` | Front VR visor (`PASTEL_BLUE` / `PASTEL_BLUE_LIGHT`) + `PASTEL_GREEN` lens highlight |
| **2. Displays, Media & Smart Home** | 8 | `external_monitor` | `display`, `ultrawide_monitor` | Widescreen monitor on stand (`WHITE` screen, `PASTEL_BLUE` bezel) + `PASTEL_GREEN` window |
| | 9 | `smart_tv` | `television`, `digital_signage` | Large display on V-legs (`WHITE` screen, `PASTEL_BLUE` bezel) + `PASTEL_GREEN` play button |
| | 10 | `smart_speaker` | `voice_assistant`, `smart_home_hub` | Cylindrical smart speaker (`PASTEL_BLUE` body, `WHITE` top) + `PASTEL_GREEN` glowing voice ring |
| | 11 | `projector` | `beamer`, `meeting_projector` | Projector unit (`WHITE` chassis, `PASTEL_BLUE` lens barrel) + `PASTEL_GREEN` light beam |
| | 12 | `game_console` | `gamepad`, `controller` | Gamepad controller (`PASTEL_BLUE` body, `WHITE` D-pad) + `PASTEL_GREEN` action buttons |
| | 13 | `kiosk_terminal` | `self_service_kiosk`, `digital_kiosk` | Floor pedestal touch kiosk (`PASTEL_BLUE` stand, `WHITE` screen) + `PASTEL_GREEN` button |
| | 14 | `pos_terminal` | `cash_register`, `payment_terminal` | Countertop POS terminal (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` card reader / receipt |
| **3. Office, Audio/Video & Desk Peripherals** | 15 | `printer` | `mfp`, `office_printer` | Office printer (`PASTEL_BLUE` chassis, `WHITE` top/bottom paper sheets) + `PASTEL_GREEN` LED |
| | 16 | `barcode_scanner` | `handheld_scanner`, `pda_terminal` | Handheld barcode scanner (`PASTEL_BLUE` grip, `WHITE` window) + `PASTEL_GREEN` laser beam |
| | 17 | `ip_phone` | `desk_phone`, `voip_phone` | Desk VoIP phone (`PASTEL_BLUE` base & handset, `WHITE` LCD) + `PASTEL_GREEN` call key |
| | 18 | `webcam` | `conference_camera`, `usb_camera` | Monitor-clip circular webcam (`WHITE` body, `PASTEL_BLUE` lens ring) + `PASTEL_GREEN` LED |
| | 19 | `headset` | `headphones`, `usb_headset` | Over-ear headset (`PASTEL_BLUE` band/cups) + boom mic with `PASTEL_GREEN` tip |
| | 20 | `keyboard_mouse` | `input_devices`, `peripherals` | Compact keyboard (`WHITE` / `PASTEL_BLUE`) + wireless mouse with `PASTEL_GREEN` wheel |
| **4. Tokens, Cards, Tags & Field Endpoints** | 21 | `usb_drive` | `flash_drive`, `security_key`, `yubikey` | USB drive / security key (`PASTEL_BLUE` casing, `WHITE` connector) + `PASTEL_GREEN` touch/LED |
| | 22 | `smart_card` | `ic_card`, `sim_card`, `id_card_chip` | Contact chip card (`WHITE` card, `PASTEL_BLUE` stripe) + `PASTEL_GREEN` EMV contact pad |
| | 23 | `qr_code` | `matrix_barcode`, `two_d_code` | 2D QR finder squares (`PASTEL_BLUE` & `PASTEL_GREEN`) + `DARK` modules on `WHITE` plate |
| | 24 | `nfc_tag` | `rfid_tag`, `contactless` | Contactless card/tag (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` radio wave arcs |
| | 25 | `gps_tracker` | `location_device`, `navigation_device` | Portable GPS receiver (`WHITE` body, `PASTEL_BLUE` map) + `PASTEL_GREEN` location pin |
| | 26 | `drone` | `uav`, `quadcopter` | Quadcopter drone (`PASTEL_BLUE` body, 4 arms) + `PASTEL_GREEN` rotor discs & camera |
| | 27 | `connected_car` | `smart_car`, `electric_vehicle`, `ev`, `automobile` | Front/side modern car (`PASTEL_BLUE` body, `WHITE` windshield) + `PASTEL_GREEN` connectivity arcs |
| | 28 | `heavy_machinery` | `excavator`, `tractor`, `construction_machine` | Tracked excavator / heavy tractor (`PASTEL_BLUE` cab/arm, `WHITE` window) + `PASTEL_GREEN` sensor arc |
| | 29 | `industrial_robot` | `robot_arm`, `factory_robot` | Articulated 6-axis robot arm (`PASTEL_BLUE` segments, `WHITE` joints) + `PASTEL_GREEN` gripper |
| | 30 | `plc_controller` | `industrial_controller`, `hmi_panel` | DIN-rail PLC / HMI controller (`PASTEL_BLUE` module, `WHITE` panel) + `PASTEL_GREEN` status LEDs |

### Part B: 2D Flat Pastel Logos (60 Icons)
- Every icon in `client` (1–60) has a matching 2D flat pastel counterpart in `original_client`.
- **Mandatory Brand Color Rule**: Each `original_client` vendor icon preserves its official brand color palette softened into Drawlib pastel tones with `DARK = "#323A48"` outlines (`w = 1.9`).

---

## 4. Implementation & Verification Workflow

1. **Phase 1 — Official Reference Collection**:
   - Copy the 7 reused reference assets (`windows`, `linux`, `ubuntu`, `apple`, `dell`, `lenovo`, `asus`) from `tools/original_assets/server/` and download official SVG/PNG brand logos for the remaining 53 `client` icons into `tools/original_assets/client/<name>/`.
   - Rasterize all 60 logos to `.drawlib/scratch/client_ref/<name>_ref.png` (`512x512` RGBA, centered inside a `460x460` bounding box).
2. **Phase 2 — `client` Official Logos**:
   - Wire `client` (`ClientIcon`) across `src/drawlib/_icons/png_icons/`, `src/drawlib/icons.py`, `src/drawlib/diagrams/architecture.py`, `src/drawlib/diagrams/sequence.py`, and `tools/dcli/codegen/`.
   - Reuse the 7 scripts from `server` and author the remaining 53 scripts in `tools/icons_src/client/<name>_default.py`.
   - Run `./dcli codegen icon-client`, `./dcli release-assets build icon_client --tag v0.3`, `./dcli code-check all`, and unit tests.
3. **Phase 3 — `original_client` Concept & Pastel Logos**:
   - Wire `original_client` (`OriginalClientIcon`).
   - Author the 30 concept icons + 53 new pastel brand icons (reusing the 7 from `original_server`) in `tools/icons_src/original_client/<name>_default.py`.
   - Run `./dcli codegen icon-original-client`, `./dcli release-assets build icon_original_client --tag v0.3`, `./dcli code-check all`, and unit tests.
   - Present the finished 90-icon contact sheet for visual review.
