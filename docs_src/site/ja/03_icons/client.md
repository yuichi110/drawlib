# クライアント端末・エンドポイントアイコン

Drawlib は、`drawlib.icons.client`（`ClientIcon`）に **60 種の公式ブランドアイコン**を、`drawlib.icons.original_client`（`OriginalClientIcon`）に全 60 種の対応するブランドツインと 32 種のベンダー中立な端末・ウェアラブル・店舗 POS・コネクテッドカー・産業用ロボティクスコンセプトアイコンから成る **92 種のフラット 2D パステルアイコン**を提供しています。カスタムのキャンバスレイアウトや[アーキテクチャ図](../06_diagrams/architecture.md)内で活用できます（全 34 モジュールの全体像は[アイコン概要](./overview.md)を参照してください）。

```drawlib code=fold align=center file=icons_client_hero.png caption="クライアント端末・エンドポイントアイコン: 公式ブランド (client) と 2D パステルブランド＆コンセプトツイン (original_client)"
from drawlib.canvas import save, setup
from drawlib.icons import client, original_client
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=68)

columns = [
    (
        26.0,
        "1. Official Brand",
        "client (60 Logos)",
        Styles.Neutral,
        [
            ("Chrome", client.chrome),
            ("Apple", client.apple),
            ("Android", client.android),
            ("Tesla", client.tesla),
        ],
    ),
    (
        72.0,
        "2. 2D Pastel Brand",
        "original_client (60 Twins)",
        Styles.PrimaryNeutral,
        [
            ("Chrome", original_client.chrome),
            ("Apple", original_client.apple),
            ("Android", original_client.android),
            ("Tesla", original_client.tesla),
        ],
    ),
    (
        118.0,
        "3. 2D Pastel Concept",
        "original_client (+32 Generic)",
        Styles.SecondaryNeutral,
        [
            ("Laptop", original_client.laptop),
            ("Smartphone", original_client.smartphone),
            ("Vehicle", original_client.connected_car),
            ("Robotics", original_client.industrial_robot),
        ],
    ),
]

for cx, title, subtitle, card_style, icons_list in columns:
    rectangle((cx, 34), width=42.0, height=60, style=card_style.patch(shape_r=2.5))
    text((cx, 58.5), title, style=Styles.DarkBold.patch(text_size=11.0))
    text((cx, 53.2), subtitle, style=Styles.Muted.patch(text_size=10.0))

    offsets = [(-9.8, 40.5), (9.8, 40.5), (-9.8, 19.5), (9.8, 19.5)]
    sub_card_style = Styles.White.patch(shape_r=1.5, line_width=0.6)
    for (dx, iy), (lbl, fn) in zip(offsets, icons_list, strict=True):
        ix = cx + dx
        rectangle((ix, iy - 2.0), width=17.5, height=17.5, style=sub_card_style)
        fn((ix, iy + 1.2), width=7.5, style=Styles.Primary)
        text((ix, iy - 6.8), lbl, style=Styles.DarkBold.patch(text_size=10.0))

save()
```

---

## 1. API シグネチャとツインモジュール構成

クライアントアイコンペアでは、Web ブラウザ・OS・ハードウェアメーカーの公式ロゴと、統一感のある 2D パステル調のエンドポイントイラストとを使い分けられます。

| モジュール | ダイアグラム Enum | 正規アイコン数 | アセットパッケージ | 主な用途 |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.client` | `ClientIcon` | **60** | `icon_client` | Web ブラウザ、デスクトップ／モバイル OS、PC・スマートフォンメーカー、ゲーム機、産業機器・自動車ブランドの公式ロゴ。 |
| `drawlib.icons.original_client` | `OriginalClientIcon` | **92**（`60 + 32`） | `icon_original_client` | 全 60 ブランドのフラット 2D パステルツインに加え、**32 種のベンダー中立エンドポイントコンセプトアイコン**（`laptop`、`smartphone`、`pos_terminal`、`plc_controller` など）を収録。 |

両モジュールのすべての関数は、`1:1` の正方形アスペクト比で**中心 `(cx, cy)`** を基準に正規化済みの `512×512` RGBA PNG を描画します。

```python
from drawlib.diagrams.architecture import ClientIcon, Node, OriginalClientIcon
from drawlib.icons import client, original_client
from drawlib.styles import Colors, Styles

# 1. Direct canvas rendering — official browser logo vs. 2D pastel twin
client.chrome((30, 25), width=9.0, style=Styles.Primary)
original_client.chrome((50, 25), width=9.0, style=Styles.Primary)

# 2. Vendor-neutral endpoint concept icon with background tint & border
framed = Styles.Primary.patch(
    image_tint_color=Colors.Primary1,
    image_border_color=Colors.Primary,
    image_border_width=1.2,
    image_border_style="dashed",
)
original_client.pos_terminal((70, 25), width=9.0, style=framed)

# 3. Inside ArchitectureDiagram Node or SequenceDiagram Participant
web_node = Node("Web Browser", width=24, height=18, icon=ClientIcon.CHROME, icon_size=7.5)
iot_node = Node("PLC Edge", width=24, height=18, icon=OriginalClientIcon.PLC_CONTROLLER, icon_size=7.5)
```

---

## 2. 公式・パステルブランドアイコン (`client` & `original_client`)

以下に示す **60 種のブランドアイコン**は、`client.<name>()` と `original_client.<name>()` の間で同一の正規関数名を共有しており、`ClientIcon.<NAME>` および `OriginalClientIcon.<NAME>` でも同一の大文字 Enum メンバーとして定義されています。

```drawlib code=fold align=center file=icons_client_brands.png caption="drawlib.icons.client の代表的なブランドアイコン 10 選 (original_client と共通)"
from drawlib.canvas import save, setup
from drawlib.icons import client
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=62)

row1 = [
    ("chrome", "Web Browser", client.chrome, Styles.Neutral),
    ("safari", "Web Browser", client.safari, Styles.PrimaryNeutral),
    ("firefox", "Web Browser", client.firefox, Styles.Neutral),
    ("windows", "Desktop OS", client.windows, Styles.SecondaryNeutral),
    ("macos", "Desktop OS", client.macos, Styles.Neutral),
]

row2 = [
    ("ios", "Mobile OS", client.ios, Styles.PrimaryNeutral),
    ("android", "Mobile OS", client.android, Styles.Neutral),
    ("linux", "Kernel / OS", client.linux, Styles.SecondaryNeutral),
    ("playstation", "Game Console", client.playstation, Styles.Neutral),
    ("tesla", "Connected EV", client.tesla, Styles.PrimaryNeutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 45.0 if row_idx == 0 else 17.0
    for col_idx, (name, cat, icon_fn, card_st) in enumerate(items):
        cx = 18.4 + col_idx * 26.8
        rectangle((cx, cy), width=24.8, height=24.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 4.5), width=8.0, style=Styles.Primary)
        text((cx, cy - 3.2), name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.0), cat, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 2.1. 正規ブランドアイコン全 60 種一覧 (`client` & `original_client`)

| カテゴリ | 数 | 正規関数名 (`client.<name>` / `original_client.<name>`) |
| :--- | :---: | :--- |
| **Web ブラウザ** | 10 | `arc`, `brave`, `chrome`, `chromium`, `edge`, `firefox`, `opera`, `safari`, `tor_browser`, `vivaldi` |
| **OS・アプリストア** | 10 | `android`, `app_store`, `chromeos`, `ios`, `linux`, `macos`, `microsoft_store`, `play_store`, `ubuntu`, `windows` |
| **PC・モバイル・電子機器メーカー** | 13 | `acer`, `apple`, `asus`, `dell`, `hp`, `lenovo`, `logitech`, `meta`, `microsoft`, `panasonic`, `samsung`, `sony`, `switchbot` |
| **スマートホーム・メディア・ゲーム機** | 10 | `alexa`, `amazon_fire`, `fire_tv`, `fitbit`, `kindle`, `netflix`, `nintendo`, `playstation`, `xbox`, `youtube` |
| **プリンタ・スキャナ・接続規格** | 7 | `bluetooth`, `brother`, `canon`, `epson`, `ricoh`, `usb`, `zebra` |
| **自動車・建機・産業機器 (OT)** | 10 | `abb`, `bmw`, `caterpillar`, `fanuc`, `honeywell`, `john_deere`, `komatsu`, `siemens`, `tesla`, `toyota` |

---

## 3. ベンダー中立コンセプトアイコン (`original_client` 専用)

60 種のブランドツインに加え、`drawlib.icons.original_client`（`OriginalClientIcon`）には **32 種のベンダー中立なクライアント端末・周辺機器・ウェアラブル・店舗 POS・車両・ロボティクスコンセプトアイコン**が収録されています。

```drawlib code=fold align=center file=icons_client_concepts.png caption="drawlib.icons.original_client 専用の代表的なベンダー中立エンドポイントコンセプトアイコン 10 選"
from drawlib.canvas import save, setup
from drawlib.icons import original_client
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=62)

row1 = [
    ("laptop", "Workstation", original_client.laptop, Styles.Neutral),
    ("desktop_pc", "Desktop PC", original_client.desktop_pc, Styles.PrimaryNeutral),
    ("smartphone", "Mobile App", original_client.smartphone, Styles.Neutral),
    ("tablet", "Tablet Client", original_client.tablet, Styles.SecondaryNeutral),
    ("smartwatch", "Wearable", original_client.smartwatch, Styles.Neutral),
]

row2 = [
    ("vr_headset", "XR / Spatial", original_client.vr_headset, Styles.PrimaryNeutral),
    ("pos_terminal", "Retail POS", original_client.pos_terminal, Styles.Neutral),
    ("connected_car", "V2X Telemetry", original_client.connected_car, Styles.SecondaryNeutral),
    ("drone", "Autonomous UAV", original_client.drone, Styles.Neutral),
    ("industrial_robot", "Factory OT", original_client.industrial_robot, Styles.PrimaryNeutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 45.0 if row_idx == 0 else 17.0
    for col_idx, (name, role, icon_fn, card_st) in enumerate(items):
        cx = 18.4 + col_idx * 26.8
        rectangle((cx, cy), width=24.8, height=24.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 4.5), width=8.0, style=Styles.Primary)
        text((cx, cy - 3.2), name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.0), role, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 3.1. 正規コンセプトアイコン全 32 種一覧 (`original_client` 専用)

| 正規関数名 (`original_client.*`) | `OriginalClientIcon` Enum | エンドポイント区分 | 主なアーキテクチャ上の役割 |
| :--- | :--- | :--- | :--- |
| `barcode_scanner` | `OriginalClientIcon.BARCODE_SCANNER` | 小売・物流 | 倉庫・店舗在庫管理用のハンディ型 1D/2D バーコードスキャナ |
| `connected_car` | `OriginalClientIcon.CONNECTED_CAR` | 自動車・V2X | コネクテッドカーのテレマティクスおよび OTA 更新クライアント |
| `desktop_pc` | `OriginalClientIcon.DESKTOP_PC` | パーソナルコンピューティング | オフィス用デスクトップワークステーションまたはシンクライアント端末 |
| `drone` | `OriginalClientIcon.DRONE` | 自律移動・ロボティクス | 点検・配送向けの無人航空機（UAV／ドローン）ノード |
| `ereader` | `OriginalClientIcon.EREADER` | モバイル・コンシューマ | E-Ink 電子書籍リーダーおよびオフライン文書閲覧タブレット |
| `external_monitor` | `OriginalClientIcon.EXTERNAL_MONITOR` | オフィス周辺機器 | 高解像度外部ディスプレイまたはデジタルサイネージ画面 |
| `game_console` | `OriginalClientIcon.GAME_CONSOLE` | リビング・メディア | 家庭用ゲーム機およびコントローラエンドポイント |
| `gps_tracker` | `OriginalClientIcon.GPS_TRACKER` | フリート・IoT | 資産位置ビーコンおよび GNSS 車両動態管理トラッキングモジュール |
| `headset` | `OriginalClientIcon.HEADSET` | オフィス周辺機器 | コールセンター向けブームマイク付き VoIP ヘッドセット |
| `heavy_machinery` | `OriginalClientIcon.HEAVY_MACHINERY` | 産業・OT | 建設用油圧ショベル、鉱山ダンプ、農業機械などの重機端末 |
| `industrial_robot` | `OriginalClientIcon.INDUSTRIAL_ROBOT` | 産業・OT | 工場組立ラインの多関節ロボットアームおよびロボットセル |
| `ip_phone` | `OriginalClientIcon.IP_PHONE` | オフィス周辺機器 | エンタープライズ SIP / VoIP デスク電話機 |
| `keyboard_mouse` | `OriginalClientIcon.KEYBOARD_MOUSE` | オフィス周辺機器 | デスクトップ入力周辺機器および HID ワークステーションインターフェース |
| `kiosk_terminal` | `OriginalClientIcon.KIOSK_TERMINAL` | 小売・公共端末 | セルフチェックイン・発券・セルフ注文用のタッチパネルキオスク端末 |
| `laptop` | `OriginalClientIcon.LAPTOP` | パーソナルコンピューティング | 開発者・業務用ノート PC |
| `nfc_tag` | `OriginalClientIcon.NFC_TAG` | ID・IoT | 非接触 NFC スマートタグまたはタッチペアリングトリガ |
| `plc_controller` | `OriginalClientIcon.PLC_CONTROLLER` | 産業・OT | 工場 SCADA ライン制御用のプログラマブルロジックコントローラ（PLC） |
| `pos_terminal` | `OriginalClientIcon.POS_TERMINAL` | 小売・決済 | 店舗レジのカードリーダーおよび POS チェックアウト端末 |
| `printer` | `OriginalClientIcon.PRINTER` | オフィス周辺機器 | ネットワーク接続対応のレーザー／インクジェット複合機 |
| `projector` | `OriginalClientIcon.PROJECTOR` | オフィス周辺機器 | 会議室プレゼンテーション用プロジェクタ |
| `qr_code` | `OriginalClientIcon.QR_CODE` | モバイル・ID | スキャン認証やモバイルディープリンク用の QR コードマトリクス |
| `smart_card` | `OriginalClientIcon.SMART_CARD` | ID・セキュリティ | EMV IC カード、社員証バッジ、ハードウェア PIV 認証カード |
| `smart_glasses` | `OriginalClientIcon.SMART_GLASSES` | ウェアラブル・XR | 拡張現実（AR）光学ヘッドマウントディスプレイ |
| `smart_ring` | `OriginalClientIcon.SMART_RING` | ウェアラブル・ヘルスケア | 生体ヘルスケア計測および非接触トークン機能を備えたスマートリング |
| `smart_speaker` | `OriginalClientIcon.SMART_SPEAKER` | スマートホーム | 音声操作対応のホームアシスタントスマートスピーカーハブ |
| `smart_tv` | `OriginalClientIcon.SMART_TV` | リビング・メディア | ネットワーク接続対応の OTT ストリーミングスマートテレビ |
| `smartphone` | `OriginalClientIcon.SMARTPHONE` | モバイル・コンシューマ | ネイティブ iOS/Android モバイルアプリクライアント |
| `smartwatch` | `OriginalClientIcon.SMARTWATCH` | ウェアラブル・ヘルスケア | コンパニオンアプリ連携および生体センサ搭載スマートウォッチ |
| `tablet` | `OriginalClientIcon.TABLET` | モバイル・コンシューマ | フィールドサービス・医療・メディア向けタッチタブレット |
| `usb_drive` | `OriginalClientIcon.USB_DRIVE` | ストレージ・セキュリティ | リムーバブル USB フラッシュメモリまたはハードウェアセキュリティトークン |
| `vr_headset` | `OriginalClientIcon.VR_HEADSET` | ウェアラブル・XR | 没入型 VR/MR 空間コンピューティングヘッドセット |
| `webcam` | `OriginalClientIcon.WEBCAM` | オフィス周辺機器 | USB Web 会議カメラまたはエッジビジョンセンサ |

---

## 4. 実践的なアーキテクチャ図 (`ClientIcon` & `OriginalClientIcon`)

**[`ArchitectureDiagram`](../06_diagrams/architecture.md)** 内で `ClientIcon` と `OriginalClientIcon` を組み合わせることで、マルチチャネルのユーザー端末、店舗 POS 端末、産業用 OT エンドポイントがバックエンドゲートウェイへ接続する構成をモデル化できます。

```drawlib code=show align=center file=icons_client_arch.png caption="コンシューマ端末・店舗 POS・産業 OT エッジの統合データ取り込みトポロジ"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    ClientIcon,
    GcpIcon,
    Node,
    NodeGroup,
    OriginalClientIcon,
)
from drawlib.styles import Styles

setup(width=148, height=68)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Multi-Endpoint Consumer, Retail POS & Industrial OT Telemetry Topology",
)

# Client & Edge Endpoints
endpoints = d.add(NodeGroup(title="Client Endpoints", padding=4.5), xy=(0.0, 0.0))
web = endpoints.add(
    Node("Chrome\nWeb App", width=22, height=16, icon=ClientIcon.CHROME, icon_size=6.8),
    xy=(15.5, 34.5),
)
pos = endpoints.add(
    Node(
        "Retail POS\nTerminal",
        width=22,
        height=16,
        icon=OriginalClientIcon.POS_TERMINAL,
        icon_size=6.8,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(15.5, 12.5),
)

# Cloud & OT Ingestion Platform
cloud = d.add(NodeGroup(title="Unified Edge & Cloud Ingestion", padding=4.5), xy=(39.0, 0.0))
lb = cloud.add(
    Node(
        "Cloud Load\nBalancing",
        width=22,
        height=16,
        icon=GcpIcon.CLOUD_LOAD_BALANCING,
        icon_size=6.8,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(15.5, 23.5),
)
run = cloud.add(
    Node(
        "Cloud Run\nBFF API",
        width=23,
        height=16,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=6.8,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(50.0, 34.5),
)
pubsub = cloud.add(
    Node(
        "Pub/Sub\nEvent Bus",
        width=23,
        height=16,
        icon=GcpIcon.PUBSUB,
        icon_size=6.8,
    ),
    xy=(50.0, 12.5),
)
bq = cloud.add(
    Node(
        "BigQuery\nLakehouse",
        width=22,
        height=16,
        icon=GcpIcon.BIGQUERY,
        icon_size=6.8,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(84.5, 23.5),
)

d.connect(web, lb, padding=1.5)
d.connect(pos, lb, padding=1.5)
d.connect(lb, run, padding=1.5)
d.connect(lb, pubsub, padding=1.5)
d.connect(run, bq, padding=1.5)
d.connect(pubsub, bq, padding=1.5)

d.draw(xy=(4.5, 4.0))
save()
```

> [!TIP]
> ソーシャルプラットフォームやマーケティング分析のアイコンについては **[ソーシャル・メディア・コミュニティアイコン (`social` / `original_social`)](./social.md)** を参照するか、**[アイコン概要](./overview.md)** に戻ってください。
