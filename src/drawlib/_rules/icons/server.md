# Drawlib Server Icons Guidelines (`lib-icons-server`)

API specification and complete catalog for `drawlib.icons.server` (`ServerIcon`, **82** icons: **56** official OS/OEM/CPU/hypervisor/storage brand logos + **12** `dell_*` hardware appliance icons + **14** `vmware_*` vSphere icons) and `drawlib.icons.original_server` (`OriginalServerIcon`, **80** flat 2D pastel icons: **56** brand twins + **24** vendor-neutral server, storage, and virtualization concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import Node, OriginalServerIcon, ServerIcon
from drawlib.icons import original_server, original_server_icon, server, server_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
server.redhat((25, 25), width=9.0, style=Styles.Primary)
original_server.redhat((50, 25), width=9.0, style=Styles.Primary)
server.dell_rack_server((75, 25), width=9.0, style=Styles.Primary)
original_server.rack_server((100, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
server_icon((25, 10), width=9.0, name="ubuntu", style=Styles.Primary)
original_server_icon((50, 10), width=9.0, name="hypervisor_host", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
esxi_node = Node("ESXi Cluster", width=24, height=18, icon=ServerIcon.VMWARE_ESXI_HOST, icon_size=7.5)
san_node = Node("SAN Storage", width=24, height=18, icon=OriginalServerIcon.SAN_STORAGE, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.server` | `ServerIcon` | **82** (`56` + `12` `dell_*` + `14` `vmware_*`) | `icon_server` | Official Linux/OS/OEM/CPU/storage vendor logos + Dell hardware & VMware vSphere topology icons. |
| `drawlib.icons.original_server` | `OriginalServerIcon` | **80** (`56` + `24` concepts) | `icon_original_server` | Flat 2D pastel twins for all 56 brands plus **24 vendor-neutral physical server, VM, and storage concepts**. |

---

## 2. Complete 56 Shared Brand Icons (`server.*` & `original_server.*`)

| Category | Count | Canonical Function Names (`server.*` & `original_server.*`) |
| :--- | :---: | :--- |
| **Linux Distributions** | 13 | `almalinux`, `alpine_linux`, `arch_linux`, `centos`, `debian`, `fedora`, `kali_linux`, `linux`, `nixos`, `redhat`, `rocky_linux`, `suse`, `ubuntu` |
| **BSD, Desktop & Server OS** | 4 | `apple`, `freebsd`, `openbsd`, `windows` |
| **Enterprise Server OEMs** | 9 | `asus`, `dell`, `fujitsu`, `hitachi`, `hpe`, `ibm`, `lenovo`, `nec`, `supermicro` |
| **CPU & Silicon Architectures** | 4 | `amd`, `arm`, `intel`, `risc_v` |
| **SBC, Compact & Power Hardware** | 5 | `apc`, `arduino`, `beaglebone`, `mac_mini`, `raspberry_pi` |
| **Hypervisors, Virtualization & Cloud** | 10 | `citrix`, `kvm`, `lxc`, `nutanix`, `openstack`, `proxmox`, `qemu`, `virtualbox`, `vmware`, `xen` |
| **Enterprise Storage, NAS & Backup** | 11 | `buffalo`, `netapp`, `openzfs`, `pure_storage`, `qnap`, `rubrik`, `seagate`, `synology`, `truenas`, `veeam`, `western_digital` |

---

## 3. Hardware & Virtualization Topology Icons (`server` vs. `original_server`)

### 3.1. `drawlib.icons.server` — Dell Hardware (`12`) & VMware vSphere (`14`) Icons

| Sub-Suite | Count | Canonical Function Names (`server.*` / `ServerIcon.*`) |
| :--- | :---: | :--- |
| **Dell Server & Compute Hardware (`dell_*`)** | 7 | `dell_blade_chassis`, `dell_bmc_management`, `dell_fc_switch`, `dell_gpu_server`, `dell_hci_appliance`, `dell_rack_server`, `dell_tower_server` |
| **Dell Storage & Backup Appliances (`dell_*`)** | 5 | `dell_backup_appliance`, `dell_nas_storage`, `dell_object_storage`, `dell_san_storage`, `dell_tape_library` |
| **VMware vSphere Hosts & Clusters (`vmware_*`)** | 6 | `vmware_cluster`, `vmware_esxi_host`, `vmware_rack_server`, `vmware_resource_pool`, `vmware_vcenter`, `vmware_vmotion` |
| **VMware Virtual Machines & Storage (`vmware_*`)** | 8 | `vmware_datastore`, `vmware_snapshot`, `vmware_storage_array`, `vmware_template`, `vmware_vm`, `vmware_vm_group`, `vmware_vsan`, `vmware_vswitch` |

### 3.2. `drawlib.icons.original_server` — Vendor-Neutral Hardware & VM Concepts (`24` Icons)

| Sub-Suite | Count | Canonical Function Names (`original_server.*` / `OriginalServerIcon.*`) |
| :--- | :---: | :--- |
| **Physical Servers & Out-of-Band Management** | 7 | `blade_chassis`, `bmc`, `gpu_server`, `hci_appliance`, `management_server`, `rack_server`, `tower_server` |
| **Hypervisor Hosts, VMs & Live Migration** | 9 | `host_cluster`, `hypervisor_host`, `live_migration`, `resource_pool`, `virtual_machine`, `virtual_switch`, `vm_group`, `vm_snapshot`, `vm_template` |
| **SAN, NAS, Object Storage & Backup** | 8 | `backup_appliance`, `datastore`, `fc_switch`, `nas_storage`, `object_storage`, `san_storage`, `tape_library`, `virtual_san` |

```drawlib code=fold align=center file=icons_server_rules_arch.png caption="vSphere Virtualization & Fibre Channel SAN Topology Using ServerIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, ServerIcon
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

vcenter = d.add(
    Node("VMware\nvCenter", width=24, height=18, icon=ServerIcon.VMWARE_VCENTER, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
pod = d.add(NodeGroup(title="Production Compute & Storage Pod", padding=4.5), xy=(42, 4))
esxi = pod.add(Node("ESXi Host\nCluster", width=24, height=18, icon=ServerIcon.VMWARE_ESXI_HOST, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
san = pod.add(Node("NetApp\nAll-Flash SAN", width=24, height=18, icon=ServerIcon.NETAPP, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(vcenter, esxi, label="HTTPS", padding=1.5)
d.connect(esxi, san, label="32G FC", padding=1.5)
d.draw(xy=(4, 4))
save()
```
