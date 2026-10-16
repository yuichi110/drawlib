# Server, Virtualization & Storage Icons Plan (`drawlib.icons.server`)

## 1. Objective & Scope

Add 26 vendor-based server, virtualization, and enterprise storage icons under `drawlib.icons.server` (`ServerIcon`), combining **Dell EMC (`dell_*`, 12 icons)** for physical servers, storage arrays, and backup appliances with **VMware (`vmware_*`, 14 icons)** for server virtualization, clusters, and virtual storage.

- **Module**: `drawlib.icons.server`
- **Architecture Enum**: `ServerIcon`
- **Release Asset Package**: `icon_server` (`tools/release_assets/v0.3/icons/server/`)
- **Function Signature**: `(xy: Coordinate, width: PosFloat, *, style: Style, variant: Literal["default"] = "default") -> None`
- **Visual Style**: Clean 2D flat vendor-colored iconography on the `100x100` icon canvas (`setup_icon()`), normalized to `512x512` PNG (`460x460` inner bounding box).

---

## 2. Color Palettes (`tools/icons_src/utils.py`)

- **Dell Palette (`dell_*`)**:
  - `DELL_BLUE = "#0076CE"` (Official Dell Blue primary fill/accent)
  - `DELL_SLATE = "#1E293B"` (Dark bezel / chassis frame / stroke)
  - `DELL_STEEL = "#E2E8F0"` (Light metallic chassis panel / drive bay fill)
  - `DELL_TEAL = "#00B2A9"` (Status LED / storage highlight accent)
- **VMware Palette (`vmware_*`)**:
  - `VMWARE_NAVY = "#1D428A"` (VMware Deep Navy primary fill/stroke)
  - `VMWARE_CYAN = "#0091DA"` (vSphere / Horizon Sky Cyan primary fill)
  - `VMWARE_GREEN = "#64B145"` (vSAN / Health / Active Green accent)
  - `VMWARE_LIGHT = "#E6F4FA"` (Soft light cyan inner background / card fill)

---

## 3. Canonical Icon Lineup (26 Icons + 31 Aliases = 57 Functions)

### Part A: Dell EMC (`dell_*` — Physical Servers, Storage & Backup: 12 Icons)

| # | Canonical Name | Shorthand Aliases | Category | 2D Flat Motif |
| :- | :--- | :--- | :--- | :--- |
| 1 | `dell_rack_server` | `dell_poweredge` | Compute | Wide 1U/2U rack server front bezel (`DELL_SLATE` body, `DELL_BLUE` side ears, `DELL_STEEL` drive bays & `DELL_TEAL` LED) |
| 2 | `dell_blade_chassis` | `dell_mx_chassis` | Compute | Modular blade enclosure (`DELL_SLATE` frame, 4 vertical `DELL_STEEL` / `DELL_BLUE` server blades with LEDs) |
| 3 | `dell_tower_server` | — | Compute | Vertical tower server chassis (`DELL_SLATE` tower, `DELL_BLUE` front accent bar, optical/drive slots & power LED) |
| 4 | `dell_gpu_server` | `dell_ai_server` | Compute | High-density rack server (`DELL_SLATE` chassis) + upper `DELL_BLUE` / `DELL_TEAL` 4-GPU accelerator card grid |
| 5 | `dell_hci_appliance` | `dell_vxrail` | HCI | 2U HCI rack node combining left `DELL_BLUE` compute chip and right `DELL_TEAL` storage disk bays |
| 6 | `dell_bmc_management` | `dell_idrac`, `dell_openmanage` | Management | Out-of-band BMC card/server bezel with `DELL_BLUE` gear/pulse monitor screen & health indicator |
| 7 | `dell_san_storage` | `dell_powerstore`, `dell_powermax` | Storage | Enterprise SAN storage array (3 stacked `DELL_SLATE` / `DELL_BLUE` disk shelves with vertical drive slots & `DELL_TEAL` LEDs) |
| 8 | `dell_nas_storage` | `dell_powerscale`, `dell_isilon` | Storage | Scale-out NAS array (`DELL_SLATE` storage shelves + foreground `DELL_BLUE` / `WHITE` shared file folder badge) |
| 9 | `dell_object_storage` | `dell_ecs` | Storage | Enterprise object storage enclosure (`DELL_SLATE` / `DELL_STEEL` frame + 3 `DELL_BLUE` / `DELL_TEAL` geometric object cubes/hexagons) |
| 10 | `dell_backup_appliance` | `dell_datadomain` | Backup | Deduplication backup storage array (`DELL_SLATE` shelves + foreground `DELL_BLUE` / `DELL_TEAL` circular restore arrow shield) |
| 11 | `dell_tape_library` | `dell_lto_tape` | Backup | Automated tape library (`DELL_SLATE` enclosure, `WHITE` window with dual `DELL_BLUE` tape reels & magnetic tape path) |
| 12 | `dell_fc_switch` | `dell_san_switch`, `dell_connectrix` | SAN Fabric | Fibre Channel SAN director/switch (`DELL_SLATE` 1U chassis, `DELL_BLUE` bezel + crossing `DELL_TEAL` optical fabric paths) |

### Part B: VMware (`vmware_*` — Server Virtualization, Cluster & Virtual Storage: 14 Icons)

| # | Canonical Name | Shorthand Aliases | Category | 2D Flat Motif |
| :- | :--- | :--- | :--- | :--- |
| 13 | `vmware_rack_server` | `vmware_physical_server` | Compute | VMware-styled physical x86 rack host (`VMWARE_NAVY` body, `VMWARE_LIGHT` drive slots, `VMWARE_CYAN` accent & `VMWARE_GREEN` LED) |
| 14 | `vmware_esxi_host` | `vmware_hypervisor` | Virtualization | Bare-metal server base (`VMWARE_NAVY`) + `VMWARE_CYAN` hypervisor layer supporting 2 `WHITE` / `VMWARE_GREEN` VM blocks above |
| 15 | `vmware_vm` | `vmware_virtual_machine` | Virtualization | Crisp 2D Virtual Machine card (`VMWARE_CYAN` frame, `WHITE` inner card, `VMWARE_NAVY` title bar & `VMWARE_GREEN` status badge) |
| 16 | `vmware_vm_group` | `vmware_vapp` | Virtualization | Cascading stack of 3 Virtual Machine cards (`VMWARE_NAVY` back, `VMWARE_CYAN` mid, `WHITE`/`VMWARE_CYAN` front with `VMWARE_GREEN` dot) |
| 17 | `vmware_template` | `vmware_vm_template` | Virtualization | VM master blueprint (`VMWARE_NAVY` dashed outer frame surrounding a crisp `VMWARE_CYAN` / `WHITE` VM card) |
| 18 | `vmware_snapshot` | `vmware_vm_snapshot` | Virtualization | VM card (`VMWARE_CYAN`) + bottom-right `VMWARE_GREEN` / `WHITE` clock/branch state snapshot badge |
| 19 | `vmware_vcenter` | `vmware_management_server` | Management | Central management console (`VMWARE_NAVY` hub / server + `VMWARE_CYAN` & `VMWARE_GREEN` connected managed nodes) |
| 20 | `vmware_cluster` | `vmware_ha_cluster`, `vmware_drs_cluster` | Cluster | 3 grouped `VMWARE_NAVY` / `VMWARE_CYAN` host nodes inside a `VMWARE_GREEN` / `VMWARE_CYAN` cluster ring |
| 21 | `vmware_resource_pool` | — | Cluster | Logical resource pool container (`VMWARE_CYAN` rounded frame + CPU/Memory gauge bars in `VMWARE_NAVY` & `VMWARE_GREEN`) |
| 22 | `vmware_vmotion` | `vmware_live_migration` | Cluster | Live migration of a `VMWARE_CYAN` VM card moving left-to-right with `VMWARE_GREEN` motion lines & arrow between two host pillars |
| 23 | `vmware_vswitch` | `vmware_dvs`, `vmware_nsx_switch` | Virtual Network | Virtual switch badge (`VMWARE_NAVY` / `VMWARE_CYAN` horizontal switch plate + 2x2 switching arrows & virtual port dots) |
| 24 | `vmware_datastore` | `vmware_vmfs` | Virtual Storage | Storage cylinder (`VMWARE_NAVY` / `VMWARE_CYAN` tiers) + foreground `VMWARE_GREEN` / `WHITE` VM badge |
| 25 | `vmware_vsan` | `vmware_hci_storage` | Virtual Storage | Distributed HCI storage pool (3 `VMWARE_CYAN` / `VMWARE_NAVY` storage blocks linked in a triangle with `VMWARE_GREEN` center hub) |
| 26 | `vmware_storage_array` | `vmware_san_nas` | Storage | External shared SAN/NAS storage array (`VMWARE_NAVY` stacked disk shelves with `VMWARE_CYAN` bays & `VMWARE_GREEN` LEDs) |

---

## 4. Implementation & Verification Workflow

1. **Phase 1 (Shared Foundation)**:
   - Add Dell & VMware color constants to `tools/icons_src/utils.py`.
   - Wire `server` provider across `src/drawlib/_icons/png_icons/server/`, `src/drawlib/icons.py`, `src/drawlib/_diagrams/`, and `tools/dcli/codegen/`.
2. **Phase 2 (Parallel Subagents — 4 Batches)**:
   - Batch 1: `dell_*` 1–6 (Compute, HCI & Management)
   - Batch 2: `dell_*` 7–12 (Storage, Backup & SAN Fabric)
   - Batch 3: `vmware_*` 13–19 (Host, VM, Template, Snapshot & vCenter)
   - Batch 4: `vmware_*` 20–26 (Cluster, Resource Pool, vMotion, vSwitch, Datastore, vSAN & Storage Array)
   - Each subagent writes its `.py` files and performs Stage 1 & Stage 2 grid inspection (`drawlib show ... -g`).
3. **Phase 3 (Unified Build, Codegen, Asset Sync & Contact Sheet Review)**:
   - Render all 26 icons, run `./dcli codegen icon-server`, sync `_cached_assets` and `_release_assets.py`, build `icon_server.zip`, inspect the 26-icon contact sheet, add tests (`tests/drawlib/icons/test_server.py`), update rules, and run `./dcli code-check all` & `./dcli test target icons` / `diagrams`.
