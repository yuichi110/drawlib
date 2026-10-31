# サーバー・OS・仮想化アイコン (`server` & `original_server`)

Drawlib は、物理サーバー・オペレーティングシステム・CPU アーキテクチャ・ストレージアレイ・仮想化プラットフォーム向けにペアとなる 2 つのアイコンモジュールを提供します。1 つは公式ブランド・Dell ハードウェア・VMware vSphere アイコン **82 個**を収録した **`drawlib.icons.server`**（`ServerIcon`）、もう 1 つはフラット 2D パステルのブランドツインおよびベンダーニュートラルなコンピュート／ストレージ／仮想化概念アイコン **80 個**を収録した **`drawlib.icons.original_server`**（`OriginalServerIcon`）です。両モジュールとも **[アイコン概要](./overview.md)** で解説されている共通の座標アンカーを備えており、**[アーキテクチャ図](../06_diagrams/architecture.md)** にそのまま組み込めます。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/03_icons/server/icons_server_hero.png" alt="server_1" />
  <figcaption class="drawlib-caption">公式ブランド・ハードウェアアイコン（server）とオリジナル 2D パステルアイコン（original_server）の比較</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import original_server, server
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=68)

columns = [
    ("Linux / OS", "ubuntu", server.ubuntu, original_server.ubuntu),
    ("Server OEM", "dell", server.dell, original_server.dell),
    ("CPU Silicon", "amd", server.amd, original_server.amd),
    ("Hypervisor", "proxmox", server.proxmox, original_server.proxmox),
    ("Virtual VM", "virtual_machine", server.vmware_vm, original_server.virtual_machine),
]

for col_idx, (cat_label, _, _, _) in enumerate(columns):
    cx = 43.0 + col_idx * 22.8
    text((cx, 62.0), cat_label, style=Styles.DarkBold.patch(text_size=10.5))

rows = [
    (43.5, "Official Suite", "server (82)", Styles.Neutral),
    (17.5, "2D Pastel Suite", "original_server (80)", Styles.PrimaryNeutral),
]

for row_idx, (cy, row_title, row_sub, row_style) in enumerate(rows):
    rectangle((16.5, cy), width=25.0, height=22.0, style=row_style.patch(shape_r=2))
    text((16.5, cy + 3.0), row_title, style=Styles.DarkBold.patch(text_size=10.0))
    text((16.5, cy - 3.5), row_sub, style=Styles.Muted.patch(text_size=10.0))

    for col_idx, (_, fn_name, fn_off, fn_orig) in enumerate(columns):
        cx = 43.0 + col_idx * 22.8
        rectangle((cx, cy), width=20.5, height=22.0, style=row_style.patch(shape_r=2))
        icon_fn = fn_off if row_idx == 0 else fn_orig
        lbl = (
            "vmware_vm"
            if (row_idx == 0 and fn_name == "virtual_machine")
            else fn_name
        )
        icon_fn((cx, cy + 3.2), width=8.5, style=Styles.Primary)
        text((cx, cy - 6.8), lbl, style=Styles.DarkBold.patch(text_size=10.0))

save()
```

</details>



---

## 1. API シグネチャとツインモジュール構成

`drawlib.icons.server` および `drawlib.icons.original_server` のすべてのアイコンは、`512×512` の RGBA PNG アセットを `1:1` の正方形アスペクト比で描画する中心アンカー `(cx, cy)` 関数です。

```python
from drawlib.diagrams.architecture import Node, OriginalServerIcon, ServerIcon
from drawlib.icons import original_server, original_server_icon, server, server_icon
from drawlib.styles import Styles

# 1. Direct module function calls (56 shared brand names + domain-specific hardware/concepts)
server.redhat((30, 25), width=10.0, style=Styles.Primary)
original_server.redhat((55, 25), width=10.0, style=Styles.Primary)
server.dell_rack_server((80, 25), width=10.0, style=Styles.Primary)
original_server.rack_server((105, 25), width=10.0, style=Styles.Primary)

# 2. Dynamic string lookup helpers
server_icon((30, 10), width=9.0, name="ubuntu", style=Styles.Primary)
original_server_icon((55, 10), width=9.0, name="hypervisor_host", style=Styles.Primary)

# 3. Strongly typed Enums for ArchitectureDiagram & SequenceDiagram
node_a = Node("RHEL Host", icon=ServerIcon.REDHAT)
node_b = Node("Hypervisor", icon=OriginalServerIcon.HYPERVISOR_HOST)
```

| 項目 | `drawlib.icons.server` | `drawlib.icons.original_server` |
| :--- | :--- | :--- |
| **ビジュアルスタイル** | 公式ベンダーロゴ + Dell／VMware ハードウェア・トポロジアートワーク | 統一感のある 2D パステルブランドツイン＆ベンダーニュートラルなインフラ概念アイコン |
| **正規アイコン総数** | **82**（ブランド `56` 個 + `dell_*` `12` 個 + `vmware_*` `14` 個） | **80**（ブランドツイン `56` 個 + ベンダーニュートラル概念 `24` 個） |
| **ダイアグラム Enum** | `ServerIcon.<NAME>` | `OriginalServerIcon.<NAME>` |
| **動的ディスパッチャ** | `server_icon(xy, width, name=..., style=...)` | `original_server_icon(xy, width, name=..., style=...)` |
| **アセットパッケージ** | `icon_server` | `icon_original_server` |

---

## 2. 共通ブランド・ベンダーアイコン（両モジュール共通 `56` 個）

`server` と `original_server` はどちらも、Linux／BSD／Windows オペレーティングシステム、エンタープライズサーバー OEM、CPU シリコンアーキテクチャ、ハイパーバイザー、エンタープライズストレージベンダーにわたる完全に同一の **56 個の正規ブランド・OSS プロジェクト名**を備えています。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/03_icons/server/icons_server_brands.png" alt="server_2" />
  <figcaption class="drawlib-caption">server と original_server の両方で利用できる代表的なブランド・OS アイコン 10 選</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import server
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=66)

row1 = [
    ("ubuntu", "Linux OS", server.ubuntu, Styles.Neutral),
    ("redhat", "Enterprise OS", server.redhat, Styles.PrimaryNeutral),
    ("windows", "Server OS", server.windows, Styles.Neutral),
    ("dell", "Server OEM", server.dell, Styles.SecondaryNeutral),
    ("hpe", "Server OEM", server.hpe, Styles.Neutral),
]

row2 = [
    ("intel", "CPU Silicon", server.intel, Styles.Neutral),
    ("amd", "CPU Silicon", server.amd, Styles.SecondaryNeutral),
    ("vmware", "Virtualization", server.vmware, Styles.PrimaryNeutral),
    ("proxmox", "Hypervisor", server.proxmox, Styles.Neutral),
    ("netapp", "Storage Array", server.netapp, Styles.Neutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 48.0 if row_idx == 0 else 18.0
    for col_idx, (fn_name, cat, icon_fn, card_st) in enumerate(items):
        cx = 16.0 + col_idx * 28.0
        rectangle((cx, cy), width=25.5, height=26.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 5.0), width=8.5, style=Styles.Primary)
        text((cx, cy - 3.2), fn_name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.5), cat, style=Styles.Muted.patch(text_size=10.0))

save()
```

</details>



### 2.1. 共通ブランドアイコン リファレンス一覧（全 `56` 正規名）

以下のすべての関数名は、`server.<name>()`（`ServerIcon.<NAME>`）および `original_server.<name>()`（`OriginalServerIcon.<NAME>`）の両方で同一名として利用できます。

| カテゴリ | 個数 | 正規関数名（`server.*` & `original_server.*`） |
| :--- | :---: | :--- |
| **Linux ディストリビューション** | 13 | `almalinux`, `alpine_linux`, `arch_linux`, `centos`, `debian`, `fedora`, `kali_linux`, `linux`, `nixos`, `redhat`, `rocky_linux`, `suse`, `ubuntu` |
| **BSD・デスクトップ・サーバー OS** | 4 | `apple`, `freebsd`, `openbsd`, `windows` |
| **エンタープライズサーバー OEM** | 9 | `asus`, `dell`, `fujitsu`, `hitachi`, `hpe`, `ibm`, `lenovo`, `nec`, `supermicro` |
| **CPU・シリコンアーキテクチャ** | 4 | `amd`, `arm`, `intel`, `risc_v` |
| **シングルボードコンピュータ・小型機器・電源装置** | 5 | `apc`, `arduino`, `beaglebone`, `mac_mini`, `raspberry_pi` |
| **ハイパーバイザー・仮想化・プライベートクラウド** | 10 | `citrix`, `kvm`, `lxc`, `nutanix`, `openstack`, `proxmox`, `qemu`, `virtualbox`, `vmware`, `xen` |
| **エンタープライズストレージ・NAS・バックアップ** | 11 | `buffalo`, `netapp`, `openzfs`, `pure_storage`, `qnap`, `rubrik`, `seagate`, `synology`, `truenas`, `veeam`, `western_digital` |

---

## 3. ハードウェア・仮想化トポロジアイコン（`dell_*` / `vmware_*` とベンダーニュートラル概念）

共通の 56 ブランドアイコンに加え、各モジュールにはそれぞれのビジュアルティアに合わせた専用のインフラトポロジアイコンが収録されています。
- **`drawlib.icons.server`（`26` 個）**: **Dell ハードウェア／ストレージアプライアンスアイコン 12 個（`dell_*`）**と、**VMware vSphere 仮想化アイコン 14 個（`vmware_*`）**を収録しています。
- **`drawlib.icons.original_server`（`24` 個）**: 特定のベンダーブランドに依存せず物理層・仮想化層を表現できる、**ベンダーニュートラルな 2D パステルのサーバー・ストレージ・仮想化概念アイコン 24 個**（`rack_server`、`gpu_server`、`hypervisor_host`、`virtual_machine`、`san_storage` など）を収録しています。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/03_icons/server/icons_server_concepts.png" alt="server_3" />
  <figcaption class="drawlib-caption">server（dell_* / vmware_*）と original_server のベンダーニュートラル概念アイコンの比較</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import original_server, server
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=68)

row1 = [
    ("dell_rack_server", "server.dell_*", server.dell_rack_server, Styles.Neutral),
    ("dell_gpu_server", "server.dell_*", server.dell_gpu_server, Styles.PrimaryNeutral),
    ("dell_san_storage", "server.dell_*", server.dell_san_storage, Styles.Neutral),
    ("vmware_esxi_host", "server.vmware_*", server.vmware_esxi_host, Styles.SecondaryNeutral),
    ("vmware_vcenter", "server.vmware_*", server.vmware_vcenter, Styles.Neutral),
]

row2 = [
    ("rack_server", "original_server", original_server.rack_server, Styles.Neutral),
    ("gpu_server", "original_server", original_server.gpu_server, Styles.PrimaryNeutral),
    ("san_storage", "original_server", original_server.san_storage, Styles.Neutral),
    ("hypervisor_host", "original_server", original_server.hypervisor_host, Styles.SecondaryNeutral),
    ("virtual_machine", "original_server", original_server.virtual_machine, Styles.Neutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 49.0 if row_idx == 0 else 19.0
    for col_idx, (fn_name, mod_label, icon_fn, card_st) in enumerate(items):
        cx = 16.0 + col_idx * 28.0
        rectangle((cx, cy), width=26.0, height=26.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 5.0), width=8.5, style=Styles.Primary)
        text((cx, cy - 3.2), fn_name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.5), mod_label, style=Styles.Muted.patch(text_size=10.0))

save()
```

</details>



### 3.1. `drawlib.icons.server` — Dell ハードウェア・VMware vSphere アイコン（`26` 個）

| サブスイート | 個数 | 正規関数名（`server.*` / `ServerIcon.*`） |
| :--- | :---: | :--- |
| **Dell サーバー・コンピュートハードウェア（`dell_*`）** | 7 | `dell_blade_chassis`, `dell_bmc_management`, `dell_fc_switch`, `dell_gpu_server`, `dell_hci_appliance`, `dell_rack_server`, `dell_tower_server` |
| **Dell ストレージ・バックアップアプライアンス（`dell_*`）** | 5 | `dell_backup_appliance`, `dell_nas_storage`, `dell_object_storage`, `dell_san_storage`, `dell_tape_library` |
| **VMware vSphere ホスト・クラスター（`vmware_*`）** | 6 | `vmware_cluster`, `vmware_esxi_host`, `vmware_rack_server`, `vmware_resource_pool`, `vmware_vcenter`, `vmware_vmotion` |
| **VMware 仮想マシン・ストレージ（`vmware_*`）** | 8 | `vmware_datastore`, `vmware_snapshot`, `vmware_storage_array`, `vmware_template`, `vmware_vm`, `vmware_vm_group`, `vmware_vsan`, `vmware_vswitch` |

### 3.2. `drawlib.icons.original_server` — ベンダーニュートラルなハードウェア・仮想化概念（`24` 個）

| サブスイート | 個数 | 正規関数名（`original_server.*` / `OriginalServerIcon.*`） |
| :--- | :---: | :--- |
| **物理サーバー・帯域外管理（OOB）** | 7 | `blade_chassis`, `bmc`, `gpu_server`, `hci_appliance`, `management_server`, `rack_server`, `tower_server` |
| **ハイパーバイザーホスト・VM・ライブマイグレーション** | 9 | `host_cluster`, `hypervisor_host`, `live_migration`, `resource_pool`, `virtual_machine`, `virtual_switch`, `vm_group`, `vm_snapshot`, `vm_template` |
| **SAN・NAS・オブジェクトストレージ・バックアップ** | 8 | `backup_appliance`, `datastore`, `fc_switch`, `nas_storage`, `object_storage`, `san_storage`, `tape_library`, `virtual_san` |

---

## 4. 実践的なアーキテクチャ図

以下の例では、**[`ArchitectureDiagram`](../06_diagrams/architecture.md)** と `ServerIcon` を組み合わせて、ハイブリッドな仮想化基盤と SAN ストレージトポロジを構築しています。



```python
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, ServerIcon
from drawlib.styles import Styles

clear()
setup(width=144, height=74)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Enterprise vSphere Cluster & Fibre Channel SAN Architecture",
)

vcenter = d.add(
    Node(
        "VMware\nvCenter",
        width=24,
        height=18,
        icon=ServerIcon.VMWARE_VCENTER,
        icon_size=7.5,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(10.0, 38.0),
)

cluster = d.add(NodeGroup(title="Production Compute & Storage Pod", padding=5.0), xy=(40.0, 4.0))

esxi = cluster.add(
    Node(
        "ESXi Host\nCluster",
        width=25,
        height=18,
        icon=ServerIcon.VMWARE_ESXI_HOST,
        icon_size=7.5,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(12.0, 34.0),
)
rhel = cluster.add(
    Node(
        "RHEL Guest\nWorkloads",
        width=25,
        height=18,
        icon=ServerIcon.REDHAT,
        icon_size=7.5,
    ),
    xy=(12.0, 6.0),
)
san = cluster.add(
    Node(
        "NetApp\nAll-Flash SAN",
        width=25,
        height=18,
        icon=ServerIcon.NETAPP,
        icon_size=7.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(60.0, 34.0),
)
veeam = cluster.add(
    Node(
        "Veeam\nBackup Vault",
        width=25,
        height=18,
        icon=ServerIcon.VEEAM,
        icon_size=7.5,
    ),
    xy=(60.0, 6.0),
)

d.connect(vcenter, esxi, label="HTTPS", padding=1.5)
d.connect(esxi, rhel, label="Guest VM", padding=1.5)
d.connect(esxi, san, label="32G FC", padding=1.5)
d.connect(san, veeam, label="Snapshot", padding=1.5)

d.draw(xy=(4.0, 4.0))
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/03_icons/server/icons_server_arch.png" alt="server_4" />
  <figcaption class="drawlib-caption">ArchitectureDiagram と ServerIcon を用いたエンタープライズ仮想化＆ファイバーチャネル SAN 構成図</figcaption>
</figure>



> [!TIP]
> 物理スイッチ、ルーター、およびファイアウォールについては**[ネットワーク・Cisco トポロジアイコン (`network` & `original_network`)](./network.md)**を、ラック、UPS 電源、およびコロケーション施設については**[データセンター・ファシリティアイコン (`facility` & `original_facility`)](./facility.md)**を参照してください。
