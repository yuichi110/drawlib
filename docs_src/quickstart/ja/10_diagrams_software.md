# 10. ソフトウェア設計図：シーケンス・フロー・状態遷移・クラス・ER図

第 9 章で扱ったクラウド構成図（`ArchitectureDiagram`）に加え、`drawlib.diagrams` にはソフトウェア詳細設計向けの 5 つの専用エンジン（`SequenceDiagram`・`FlowDiagram`・`StateDiagram`・`ClassDiagram`・`ERDiagram`）が用意されており、UML 2.x・ISO 5807（JIS X 0121）・Crow's Foot（IE 記法）に準拠した設計図を宣言的な Python コードから描画できます。

```drawlib align=center code=fold file=sequence_auth_flow_ja.png caption="図 10.1: ParticipantGroup・実行区間・alt/else フレームを用いた OAuth 2.0 トークン検証シーケンス"
import math
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import (
    GcpIcon,
    Participant,
    ParticipantGroup,
    PhosphorIcon,
    SequenceDiagram,
)
from drawlib.styles import Styles

d = SequenceDiagram(
    node_style=Styles.DarkBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    autonumber=True,
    col_width=36.0,
    step_y=5.6,
    margin=4.0,
)

client = d.add(
    Participant(
        "クライアント",
        width=24.0,
        height=12.5,
        icon=PhosphorIcon.DEVICES,
        icon_size=5.0,
        card_style=Styles.Neutral,
    )
)

platform = d.add(
    ParticipantGroup(
        title="認証・API 基盤",
        padding=4.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="bottom"),
    )
)
gateway = platform.add(
    Participant(
        "API ゲートウェイ",
        width=26.0,
        height=12.5,
        icon=PhosphorIcon.CLOUD_CHECK,
        icon_size=5.0,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    )
)
auth = platform.add(
    Participant(
        "認証サービス",
        width=26.0,
        height=12.5,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=5.0,
        card_style=Styles.White,
    )
)
store = platform.add(
    Participant(
        "セッション DB",
        width=26.0,
        height=12.5,
        icon=GcpIcon.MEMORYSTORE,
        icon_size=5.0,
        card_style=Styles.SecondaryNeutral,
    )
)

client.request(gateway, "POST /v1/orders (Bearer JWT)")
gateway.activate()
gateway.request(auth, "署名検証リクエスト")
auth.activate()
auth.request(store, "GET session:jti")
store.reply(auth, "有効クレーム返却")

with d.alt("") as alt_blk:
    alt_blk.style = Styles.MutedDashed
    alt_blk.text_style = Styles.DarkBold.patch(text_size=10.0)
    auth.reply(gateway, "200 検証済みクレーム", style=Styles.SuccessBold)
    gateway.request(store, "XADD 監査ログ送信", is_async=True, style=Styles.SecondaryBold)
    gateway.reply(client, "200 OK (注文受付)", style=Styles.SuccessBold)
    d.note("300 秒キャッシュ", over=[gateway, auth], style=Styles.PrimaryNeutral.patch(text_size=10.0))

d.space(2.0)
with d.else_("") as else_blk:
    else_blk.style = Styles.MutedDashed
    else_blk.text_style = Styles.DarkBold.patch(text_size=10.0)
    auth.reply(
        gateway,
        "401 無効トークン",
        style=Styles.DangerBold,
        text_style=Styles.DangerBold.patch(text_size=10.0),
    )
    gateway.reply(
        client,
        "401 Unauthorized",
        style=Styles.DangerBold,
        text_style=Styles.DangerBold.patch(text_size=10.0),
    )

auth.deactivate()
gateway.deactivate()

w, h = d.get_size()
setup(width=math.ceil(w) + 8, height=math.ceil(h) + 8)
d.draw(xy=(4.0, 4.0))
save()
```

---

## 10.1 5 つのソフトウェア設計図エンジンの概要

`drawlib.diagrams` の各エンジンは共通のビルダーライフサイクルを備えています。コンストラクタで基本スタイルを定義し、`.add()` で要素を登録して関係線を接続し、必要に応じて `.get_size()` で外寸を取得したうえで `.draw(xy=(x0, y0))`（既定は左下アンカー）でキャンバスへ描画します。

| モジュール | 主クラス | 主な構成要素 | 座標指定方式 | 主な用途 |
| :--- | :--- | :--- | :--- | :--- |
| `drawlib.diagrams.sequence` | `SequenceDiagram` | `Participant`, `ParticipantGroup`, `Message`, `Note`, `Block` | `col_width`（X）と `step_y`（Y）で自動進行 | RPC/REST 通信手順、OAuth 認可、非同期イベント連鎖 |
| `drawlib.diagrams.flow` | `FlowDiagram` | `Start`, `End`, `Process`, `Decision`, `Data`, `Lane`, `Junction` | 共通／スイムレーン空間上の中心 `xy=(cx, cy)` | CI/CD ゲート判定、業務フロー、部門横断スイムレーン |
| `drawlib.diagrams.state` | `StateDiagram` | `State`, `InitialState`, `FinalState`, `ChoiceState`, `ForkJoinState` | 中心 `xy=(cx, cy)` と曲線／直交遷移パス | プロトコル状態機械、ワーカー寿命管理、並行状態図 |
| `drawlib.diagrams.class_diagram` | `ClassDiagram` | `ClassNode`, `AttributeInfo`, `MethodInfo`, `ClassRelationship` | 高さ自動計算の 3 区画ボックス＋中心 `xy=(cx, cy)` | OOP ドメインモデル、インターフェース実装、継承構造 |
| `drawlib.diagrams.er` | `ERDiagram` | `Entity`, `ColumnInfo`, `Relationship` | 中心 `xy=(cx, cy)` と行単位 `start_column` / `end_column` | リレーショナル DB 設計、PK/FK 制約、Crow's Foot 図 |

---

## 10.2 SequenceDiagram による時系列 API シーケンス

`SequenceDiagram`（`from drawlib.diagrams.sequence import SequenceDiagram, Participant, ParticipantGroup`）は、時系列プロトコルにおける縦方向の座標計算を完全に自動化します。

- **参加者・グループ境界・アイコン**: `d.add(Participant(...))` で左から右へライフラインを自動配置し、`ParticipantGroup(title=..., padding=4.0)` でバックエンド基盤を枠線で囲めます。33 種のアイコン列挙型（`PhosphorIcon`, `GcpIcon`, `AwsIcon`, `AzureIcon` など）も同モジュールから直接インポート可能です。
- **同期・非同期・応答メッセージ**: `a.request(b, "ラベル")` で実線の同期呼び出し、`is_async=True` で開矢印の非同期通知、`b.reply(a, "ラベル")` で破線の応答矢印、`a.request(a, "検証")` で自己呼び出しを描画します。`autonumber=True` を指定すると全メッセージに連番（`1.`, `2.`, ...）が自動付与されます。
- **実行区間（Activation）とノート**: `p.activate()` と `p.deactivate()` でライフライン上のアクティブな処理区間を明示でき、`p.note("注記", pos="right")` や複数ライフラインを跨ぐ `d.note("注記", over=[p1, p2])` で補足説明を配置できます。
- **複合フラグメント（`alt`, `else_`, `loop`, `opt`, `par`）**: Python の `with` 文（`with d.alt("条件"):` / `with d.else_("代替"):`、`with d.loop("30秒周期"):`、`with d.opt("2FA有効"):`、`with d.par("並列配信"):`）で UML 2.0 のフレーム構造を直感的に記述できます。
- **余白ゼロのキャンバス自動採寸**: メッセージ定義後に `w, h = d.get_size()` を取得し、整数サイズ `setup(width=math.ceil(w) + 8, height=math.ceil(h) + 8)` と `d.draw(xy=(4.0, 4.0))` を組み合わせることで、右半分や下半分が不自然に空くことのない引き締まった図面になります。

---

## 10.3 業務フローと状態遷移：FlowDiagram と StateDiagram

処理分岐や部門間の連携には `FlowDiagram`、イベント駆動のライフサイクル管理には `StateDiagram` を使用します。

- **`FlowDiagram`（`drawlib.diagrams.flow`）**:
  - **ISO 5807 / JIS X 0121 標準記号**: `Start`・`End`（端子ピル）、`Process`（処理矩形）、`Decision`（条件分岐ひし形）、`Data`（入出力平行四辺形）、および合流点を作る `Junction`（`flow.junction(xy)` や `node.fork([...])`）を提供します。
  - **スイムレーン（`flow.add_lane`）**: 縦列（`lane_orientation="vertical"`）または横行（`"horizontal"`）のレーンを追加できます。全レーンが単一のグローバル座標系を共有するため、異なるレーン間で同じ `y` 座標を指定するだけで水平位置が正確に揃います。
  - **高コントラスト配色の鉄則**: 通常ステップは `Styles.Neutral` や `Styles.PrimaryNeutral` に `Styles.DarkBold` 文字を合わせます。最重要ステップに `Styles.PrimaryFlat` や `Styles.AccentFlat` の濃色塗りを適用する際は、**必ず `text_style=Styles.WhiteBold` を指定してください**（濃紺の `PrimaryFlat` 背景に青系の `PrimaryBold` 文字を載せると視認性が損なわれます）。
- **`StateDiagram`（`drawlib.diagrams.state`）**:
  - **状態クラスと擬似状態クラス**: `State(name, entry=..., do=..., exit=...)`（カスタム動作行を追加する `.add_action(kind, action)` / `StateAction` 対応）に加え、`InitialState()`（開始黒丸）、`FinalState()`（終了二重丸）、`ChoiceState()`（動的ガード分岐ひし形）、`ForkJoinState(orientation="horizontal" | "vertical")`（並行同期バー）を使用します。
  - **UML 遷移ラベルと曲線ルーティング（`sd.connect`）**: `event="...", guard="...", action="..."` を渡すと `"event [guard] / action"` 形式へ自動整形されます。双方向遷移には `routing="curved"` と `bend=0.25`、自己遷移には `sd.connect(s, s, side="top")` を用います。

```drawlib align=center code=fold file=flow_and_state_ja.png caption="図 10.2: ソフトウェア振る舞い設計の対比 — カナリアリリースの FlowDiagram（左）とワーカー状態遷移の StateDiagram（右）"
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start
from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=160, height=78)

# 左パネル: FlowDiagram
rectangle((41, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.git_branch((9.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (13.5, 68.0),
    "FlowDiagram: カナリアリリース判定",
    style=Styles.DarkBold.patch(text_size=11.0, halign="left"),
)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
)
f_start = flow.add(
    Start("PR マージ", width=23, height=9.0, style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=10.0)),
    xy=(22, 54),
)
f_canary = flow.add(
    Process(
        "カナリア配備",
        width=26,
        height=10.0,
        style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=10.2),
    ),
    xy=(58, 54),
)
f_check = flow.add(
    Decision(
        "SLO 正常?",
        width=25,
        height=13.0,
        style=Styles.PrimaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.0),
    ),
    xy=(58, 35),
)
f_alert = flow.add(
    Data(
        "自動ロールバック",
        width=26,
        height=10.0,
        style=Styles.DangerNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.0),
    ),
    xy=(22, 35),
)
f_prod = flow.add(
    End(
        "本番 100% 展開",
        width=26,
        height=9.5,
        style=Styles.SecondaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.0),
    ),
    xy=(58, 14),
)

f_start.connect(f_canary, padding=0.6)
f_canary.connect(f_check, start_side="bottom", end_side="top", padding=0.6)
f_check.connect(
    f_alert,
    label="No",
    start_side="left",
    end_side="right",
    style=Styles.DangerBold,
    text_style=Styles.DangerBold.patch(text_size=10.0),
    padding=0.6,
)
f_check.connect(f_prod, label="Yes", start_side="bottom", end_side="top", padding=0.6)
flow.draw()

# 右パネル: StateDiagram
rectangle((119, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.arrows_clockwise((87.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (91.5, 68.0),
    "StateDiagram: ワーカー状態遷移",
    style=Styles.DarkBold.patch(text_size=11.0, halign="left"),
)

sd = StateDiagram(
    node_style=Styles.Neutral.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)
s_init = sd.add(InitialState(), xy=(89, 53))
s_warm = sd.add(
    State("初期化中", entry="loadModel()", width=28, style=Styles.Neutral.patch(text_size=10.0)),
    xy=(114, 53),
)
s_active = sd.add(
    State(
        "稼働中",
        do="serveGrpc()",
        exit="drainPool()",
        width=28,
        style=Styles.PrimaryNeutral.patch(text_size=10.0),
    ),
    xy=(114, 29),
)
s_choice = sd.add(ChoiceState(), xy=(146, 29))
s_final = sd.add(FinalState(), xy=(114, 11))

sd.connect(s_init, s_warm, start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(
    s_warm,
    s_active,
    label="  ready",
    start_side="bottom",
    end_side="top",
    routing="direct",
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.connect(
    s_active,
    s_choice,
    event="err",
    start_side="right",
    end_side="left",
    routing="direct",
    style=Styles.WarningBold,
    padding=0.8,
)
sd.connect(
    s_choice,
    s_warm,
    label="  [retry]",
    start_side="top",
    end_side="right",
    routing="orthogonal",
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.connect(
    s_choice,
    s_final,
    label="  [fatal]",
    start_side="bottom",
    end_side="right",
    routing="orthogonal",
    style=Styles.DangerBold,
    text_style=Styles.DangerBold.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.connect(
    s_active,
    s_final,
    label="  stop",
    start_side="bottom",
    end_side="top",
    routing="direct",
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.draw()

save()
```

---

## 10.4 ClassDiagram によるオブジェクト指向クラス設計

`ClassDiagram`（`drawlib.diagrams.class_diagram`）は、ステレオタイプ（`stereotype="interface"` や `is_abstract=True`）・属性区画・メソッド区画から成る UML 2.0 の 3 区画クラスボックス（`ClassNode`）を行数に応じた自動高さで描画します。

- **メソッドチェーンによるメンバ定義**: `.add_attribute(name, type, visibility="-", default_value=..., is_static=...)` と `.add_method(name, params, return_type, visibility="+", is_abstract=...)` を連鎖させ、可視性記号（`"+"` public、`"-"` private、`"#"` protected、`"~"` package）を付与できます。
- **6 種の標準 UML 関係線**: `cd.connect(source, target, relationship_type=...)` で `"inheritance"`（継承：実線＋白抜き三角）、`"realization"`（実装：破線＋白抜き三角）、`"composition"`（コンポジション：黒塗りひし形）、`"aggregation"`（集約：白抜きひし形）、`"dependency"`（依存：破線＋開矢印）、`"association"`（関連：実線）を描き分け、`start_multiplicity`・`end_multiplicity`・`end_role` で多重度やロール名を添えられます。

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Styles

setup(width=140, height=64)

cd = ClassDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=10.8),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)

repo = cd.add(
    ClassNode("PaymentGateway", stereotype="interface", width=44, header_style=Styles.SecondaryNeutral)
    .add_method("authorize", "amount: Decimal", "AuthReceipt"),
    xy=(32, 42),
)
stripe_gw = cd.add(
    ClassNode("StripeGateway", width=44)
    .add_attribute("api_client", "HttpClient", visibility="-")
    .add_method("authorize", "amount: Decimal", "AuthReceipt"),
    xy=(32, 16),
)
invoice = cd.add(
    ClassNode(
        "Invoice",
        width=40,
        header_style=Styles.PrimaryFlat.patch(
            text_color=Styles.WhiteBold.text_color,
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=10.8,
        ),
    )
    .add_attribute("id", "UUID", visibility="+")
    .add_attribute("status", "InvoiceState", visibility="#")
    .add_method("capture", "gw: PaymentGateway", "bool"),
    xy=(106, 29),
)

cd.connect(stripe_gw, repo, "realization", start_side="top", end_side="bottom")
cd.connect(invoice, repo, "dependency", label="<<uses>>", start_side="left", end_side="right")

cd.draw(xy=(4.0, 4.0))
save("class_model.png")
```

---

## 10.5 ERDiagram によるリレーショナルデータベース設計

`ERDiagram`（`drawlib.diagrams.er`）は Information Engineering（Crow's Foot / 鳥の足記法）による ER 図エンジンであり、各テーブル（`Entity`）のカラムを「`PK` / `FK` バッジ列」「カラム名列」「SQL 型＋`(NN)` 非 NULL 制約列」の 3 サブカラムに自動整列します。

- **エンティティ定義（`Entity`）**: `Entity("table_name", width=38)` に対して `.add_column(name, type, pk=False, fk=False, nullable=True)` をチェーンしてスキーマを宣言します。
- **Crow's Foot 多重度とカラム行アンカー接続**: `erd.connect(parent, child, cardinality="1:*", start_column="id", end_column="user_id")` でテーブル間を接続します（`"1:1"`, `"1:0..1"`, `"0..1:1"`, `"1:*"`, `"1:1..*"`, `"0..1:*"`, `"*:*"` に対応）。`start_column` と `end_column` にカラム名を渡すと、外部キー線が該当カラム行の正確な高さ（Y 座標）へスナップします。

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Styles

setup(width=136, height=52)

erd = ERDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=10.8),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)

tenants = erd.add(
    Entity("tenants", width=40)
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("slug", "VARCHAR(64)", nullable=False)
    .add_column("created_at", "TIMESTAMPTZ", nullable=False),
    xy=(30, 26),
)
api_keys = erd.add(
    Entity(
        "api_keys",
        width=42,
        header_style=Styles.PrimaryFlat.patch(
            text_color=Styles.WhiteBold.text_color,
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=10.8,
        ),
    )
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("tenant_id", "UUID", fk=True, nullable=False)
    .add_column("key_hash", "CHAR(64)", nullable=False)
    .add_column("revoked_at", "TIMESTAMPTZ", nullable=True),
    xy=(102, 26),
)

tenants.connect(
    api_keys,
    cardinality="1:*",
    start_column="id",
    end_column="tenant_id",
    start_side="right",
    end_side="left",
)

erd.draw(xy=(4.0, 4.0))
save("er_schema.png")
```
