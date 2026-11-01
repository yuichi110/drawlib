# Heatmap & Thermal Overlay（ヒートマップ）：2D マトリクスとダイアグラム熱分布オーバーレイ

`drawlib.charts.heatmap` は、`Style` のカラーストップ補間（`styles=[Style, ...]` または `min_style=...`、`max_style=...`）で彩られる 2 つの相補的なヒートマップ可視化クラスを提供します。
1. **`HeatmapChart`**: カテゴリ軸 `x_categories` × `y_categories` 上の標準的な 2D マトリクス／グリッド型ヒートマップです。背景明度に応じて文字色を自動反転するセル内数値ラベル、セル間隔・角丸めの調整（`cell_gap`、`cell_r`）、および連続カラーバー（`draw_colorbar`）や段階別凡例（`draw_legend`）を備えています。
2. **`HeatmapOverlay`**: `ClassDiagram`、`ArchitectureDiagram`、`ErDiagram`、`GeoMap` などの既存ダイアグラムの上に直接重ねて描画できる空間サーマル／ホットスポットオーバーレイです。高リスクなクラス、循環的複雑度、バグ密度、リージョンやサービスのボトルネックを `"smooth"`（2D ガウス熱分布グラデーション）または `"contour"`（同心ベクター等高線リング）モードで強調表示できます。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/05_charts/heatmap/heatmap_topologies_overview.png" alt="heatmap_1" />
  <figcaption class="drawlib-caption">ヒートマップの 2 形態：2D マトリクス HeatmapChart と ClassDiagram 上の HeatmapOverlay</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapChart, HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=136, height=62)

# Left: 2D Matrix HeatmapChart
matrix = HeatmapChart(
    styles=[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat],
    x_categories=["00h", "06h", "12h", "18h"],
    axis_line_style=Styles.Muted,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    width=58.0,
    height=40.0,
    title="1. 2D Matrix HeatmapChart",
    title_style=Styles.BlackBold.patch(text_size=11.5),
    value_format="{:.1f}%",
)
matrix.add_row("API", [0.4, 1.2, 4.8, 2.1])
matrix.add_row("Auth", [0.2, 0.8, 2.5, 1.4])
matrix.add_row("Billing", [0.5, 1.9, 7.6, 3.8])
matrix.draw(xy=(4.0, 16.0))
matrix.draw_colorbar(
    xy=(14.0, 6.5),
    text_style=Styles.Muted.patch(text_size=9.5),
    length=38.0,
    thickness=2.0,
)

# Right: Spatial Thermal HeatmapOverlay on ClassDiagram
diag = ClassDiagram(
    node_style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    title="2. ClassDiagram + HeatmapOverlay",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
c_api = diag.add(ClassNode("OrderService", width=26.0).add_method("submit", "req", "bool"), xy=(82.0, 36.0))
c_god = diag.add(
    ClassNode("LegacyBillingGodClass", width=32.0)
    .add_attribute("flags", "dict")
    .add_method("process_all", "tx", "void"),
    xy=(116.0, 36.0),
)
diag.connect(c_api, c_god, "dependency", directed=True)
diag.draw(xy=(0.0, 0.0))

overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.55,
)
overlay.add_spot(c_god, value=0.95, radius=19.0)
overlay.add_spot(c_api, value=0.35, radius=14.0)
overlay.draw(xy=(0.0, 0.0))
overlay.draw_colorbar(
    xy=(82.0, 6.5),
    text_style=Styles.Muted.patch(text_size=9.5),
    length=38.0,
    thickness=2.0,
)

save()
```

</details>



---

## 1. 基本概念と基本的な使い方

`HeatmapChart` は `.add_row(...)` や `.set_cell(...)` でカテゴリ型の 2D グリッドマトリクスを構築し、デフォルトで**左下 `(x, y)`** を基準にアンカーします。補間された `Style` カラーストップの明度に応じてセルラベルの文字色を濃色・白色へ自動切り替え（`auto_contrast_text=True`）できるのが特徴です。一方、マトリクスグリッドを補完する `HeatmapOverlay` は、既存のダイアグラムやキャンバス座標（`add_spot(...)`）の上に `"smooth"`（2D ガウス熱分布フィールド）または `"contour"`（同心ベクター等高線リング）を直接投影し、分離配置型の `.draw_colorbar(...)` スケールや `"bottom_left"`／`"center"` 配置と柔軟に組み合わせられます。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/05_charts/heatmap/heatmap_parameter_tour.png" alt="heatmap_2" />
  <figcaption class="drawlib-caption">基本的な使い方とパラメータツアー：HeatmapChart の 2D マトリクス、セル個別設定、HeatmapOverlay の熱分布と等高線ホットスポット（APNG アニメーション）</figcaption>
</figure>



<div class="drawlib-source-link">
  <a href="https://github.com/yuichi110/drawlib/blob/main/docs/docs_src/ja/05_charts/heatmap.md" target="_blank" rel="noopener noreferrer">GitHub でアニメーションのソースコードを見る &rarr;</a>
</div>

- **`HeatmapChart` と `HeatmapOverlay` の役割分担**: 表形式の 2D カテゴリマトリクス（`x_categories` × `y_categories`）には `HeatmapChart` を使用し、既存の図（`ClassDiagram`、`ArchitectureDiagram`、`GeoMap`、またはカスタムカード）の上に空間的なサーマルホットスポット（`add_spot(xy_or_node, value, radius)`）を投影する場合には `HeatmapOverlay` を使用します。
- **スタイルのカラーストップ補間とカラーバー（`styles`, `draw_colorbar`）**: 両クラスとも `styles=[Style, ...]`（または `min_style` / `max_style`）に沿って色を補間し、分離配置可能な `.draw_colorbar(xy, text_style, length=...)` と `.draw_legend(...)` ヘルパーを備えています。さらに `HeatmapChart` では、`auto_contrast_text=True` の際にセル背景の明暗に応じて暗色／明色ラベルを自動反転します。
- **マトリクスの行方向とセル個別上書き（`y_origin`, `cell_gap`, `set_cell`）**: `HeatmapChart` の行順序を `y_origin="top"`（表順）と `y_origin="bottom"`（デカルト座標順）で切り替えたり、`x_label_position="bottom" | "top"`、`cell_gap`、`cell_r` を調整したり、`None` で欠損セルを空欄にしたり、`.set_cell(x, y, value, label=..., style=...)` で特定のセルを強調したりできます。
- **オーバーレイモード・重なり合成・配置基準（`mode`, `blend_mode`, `align`）**: `HeatmapOverlay` を `mode="smooth"`（重なり領域を累積加算 `blend_mode="add"` または包絡最大値 `"max"` で合成）と `mode="contour"`（`levels=N` 段のベクター等値線リング）で切り替えられ、いずれのクラスも `"bottom_left"`（デフォルト）または `align="center"` で配置できます。

---

## 2. 標準的な 2D マトリクスヒートマップ（`HeatmapChart`）

`HeatmapChart` は、`x_categories` と `y_categories` にわたる 2D グリッドの数値を補間された `Style` カラーにマッピングし、セルラベルのコントラストを自動調整（`auto_contrast_text=True`）することで、明るいセルと暗いセルのどちらでも数値の高い視認性を保ちます。



```python
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapChart
from drawlib.styles import Styles

setup(width=115, height=80)

chart = HeatmapChart(
    styles=[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat],
    x_categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    axis_line_style=Styles.Muted,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    width=92.0,
    height=50.0,
    cell_gap=0.7,
    cell_r=0.5,
    title="Production Gateway Error Rate (%) by Day & Hour",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    value_format="{:.1f}%",
)
chart.add_row("Monday", [0.2, 0.1, 1.4, 3.8, 2.9, 0.8])
chart.add_row("Tuesday", [0.3, 0.2, 1.8, 4.5, 3.1, 0.9])
chart.add_row("Wednesday", [0.1, 0.2, 2.2, 6.4, 4.8, 1.2])
chart.add_row("Thursday", [0.4, 0.3, 1.5, 3.2, 2.4, 0.7])
chart.add_row("Friday", [0.5, 0.2, 2.9, 8.5, 5.2, 1.9])

chart.draw(xy=(12.0, 22.0))
chart.draw_colorbar(
    xy=(36.0, 8.0),
    text_style=Styles.Muted.patch(text_size=10.0),
    length=48.0,
    thickness=2.4,
    label="Error Rate (%)",
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/05_charts/heatmap/heatmap_matrix_latency.png" alt="heatmap_3" />
  <figcaption class="drawlib-caption">連続カラーバーを備えたサービスレイテンシ・エラー相関マトリクス</figcaption>
</figure>



---

## 3. 6 クラスの `ClassDiagram` ホットスポット重ね合わせ（`HeatmapOverlay`：Smooth モード）

コードベース、アーキテクチャトポロジー、または UML クラスモデルを分析する際、`HeatmapOverlay` を使うと脆弱なコンポーネントや複雑度の高いコンポーネントの上で視覚的な温度を引き上げることができます（`add_spot(class_node, value=..., radius=...)`）。`ClassNode` を直接渡すと、キャンバス上の中心座標 `.xy` が自動的に解決されます。

次の例では、**注文・決済サブシステムの 6 クラス UML `ClassDiagram`** の上に滑らかな 2D ガウス分布サーマルフィールド（`mode="smooth"`）を重ね合わせ、高リスクな God クラス `LegacyPaymentGateway`（`0.96`）と、それに密結合している `OrderOrchestrator`（`0.72`）および `FraudRuleEngine`（`0.55`）を視覚的に特定しています。



```python
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=142, height=96)

# 1. Build 6-Class UML ClassDiagram (2 rows x 3 columns)
diagram = ClassDiagram(
    node_style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    title="Order & Payment Subsystem: Complexity & Bug Hotspot Analysis (6 Classes)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    margin=8.0,
)

# Top Tier (Row 1: y = 68.0)
ctrl = diagram.add(
    ClassNode("OrderController", width=29.0)
    .add_method("create_order", "req", "Order")
    .add_method("cancel_order", "id", "bool"),
    xy=(24.0, 68.0),
)
orch = diagram.add(
    ClassNode("OrderOrchestrator", width=31.0)
    .add_attribute("retry_policy", "dict", is_public=False)
    .add_method("dispatch", "order", "Receipt")
    .add_method("rollback", "tx_id", "void"),
    xy=(71.0, 68.0),
)
notif = diagram.add(
    ClassNode("NotificationService", width=29.0)
    .add_attribute("smtp_host", "str", is_public=False)
    .add_method("send_receipt", "user", "bool")
    .add_method("alert_ops", "msg", "void"),
    xy=(118.0, 68.0),
)

# Bottom Tier (Row 2: y = 33.0)
fraud = diagram.add(
    ClassNode("FraudRuleEngine", width=29.0)
    .add_attribute("rule_cache", "list", is_public=False)
    .add_method("evaluate", "order", "float")
    .add_method("reload_rules", "", "int"),
    xy=(24.0, 33.0),
)
gateway = diagram.add(
    ClassNode("LegacyPaymentGateway", width=33.0)
    .add_attribute("global_locks", "dict", is_public=False)
    .add_attribute("raw_socket_pool", "list", is_public=False)
    .add_method("charge_card", "payload", "str")
    .add_method("reconcile_batch", "raw", "void")
    .add_method("parse_iso8583", "buf", "dict"),
    xy=(71.0, 33.0),
)
ledger = diagram.add(
    ClassNode("LedgerRepository", width=29.0)
    .add_attribute("db_pool", "Pool", is_public=False)
    .add_method("append_entry", "tx", "UUID")
    .add_method("query_audit", "id", "list"),
    xy=(118.0, 33.0),
)

# Connect the 6 classes orthogonally
diagram.connect(ctrl, orch, "dependency", start_side="right", end_side="left", label="delegates", directed=True)
diagram.connect(orch, notif, "dependency", start_side="right", end_side="left", label="notifies", directed=True)
diagram.connect(ctrl, fraud, "dependency", start_side="bottom", end_side="top", label="validates", directed=True)
diagram.connect(orch, gateway, "composition", start_side="bottom", end_side="top", label="invokes", directed=True)
diagram.connect(fraud, gateway, "association", start_side="right", end_side="left", label="scores", directed=True)
diagram.connect(gateway, ledger, "association", start_side="right", end_side="left", label="records", directed=True)

diagram.draw(xy=(0.0, 0.0))

# 2. Overlay Thermal Hotspots directly onto ClassNode coordinates
overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.55,
    blend_mode="max",
)
overlay.add_spot(gateway, value=0.96, radius=22.0)
overlay.add_spot(orch, value=0.72, radius=18.0)
overlay.add_spot(fraud, value=0.55, radius=16.0)
overlay.add_spot(ctrl, value=0.30, radius=14.0)
overlay.add_spot(ledger, value=0.15, radius=12.0)
overlay.draw(xy=(0.0, 0.0))

overlay.draw_colorbar(
    xy=(47.0, 6.5),
    text_style=Styles.Muted.patch(text_size=10.0),
    length=48.0,
    thickness=2.2,
    label="Complexity & Bug Risk Score",
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/05_charts/heatmap/heatmap_overlay_class_diagram.png" alt="heatmap_4" />
  <figcaption class="drawlib-caption">滑らかなサーマルホットスポットを重ね合わせた 6 クラス UML クラス図 (mode='smooth')</figcaption>
</figure>



---

## 4. 同心等値線リングの重ね合わせ（`mode="contour"`）

連続的なグラデーションよりも離散的な等値線リングが適しているシャープなベクター図や印刷向けドキュメントでは、6 クラス図に対して `mode="contour"` と `levels=4` を設定します。



```python
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=142, height=96)

diagram = ClassDiagram(
    node_style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    title="Change Blast Radius Analysis Across 6 Classes (mode='contour')",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    margin=10.0,
)

# Top Tier (Row 1: y = 66.0)
ctrl = diagram.add(
    ClassNode("OrderController", width=29.0)
    .add_method("create_order", "req", "Order")
    .add_method("cancel_order", "id", "bool"),
    xy=(24.0, 66.0),
)
orch = diagram.add(
    ClassNode("OrderOrchestrator", width=31.0)
    .add_attribute("retry_policy", "dict", is_public=False)
    .add_method("dispatch", "order", "Receipt")
    .add_method("rollback", "tx_id", "void"),
    xy=(71.0, 66.0),
)
notif = diagram.add(
    ClassNode("NotificationService", width=29.0)
    .add_attribute("smtp_host", "str", is_public=False)
    .add_method("send_receipt", "user", "bool")
    .add_method("alert_ops", "msg", "void"),
    xy=(118.0, 66.0),
)

# Bottom Tier (Row 2: y = 32.0)
fraud = diagram.add(
    ClassNode("FraudRuleEngine", width=29.0)
    .add_attribute("rule_cache", "list", is_public=False)
    .add_method("evaluate", "order", "float")
    .add_method("reload_rules", "", "int"),
    xy=(24.0, 32.0),
)
gateway = diagram.add(
    ClassNode("LegacyPaymentGateway", width=33.0)
    .add_attribute("global_locks", "dict", is_public=False)
    .add_attribute("raw_socket_pool", "list", is_public=False)
    .add_method("charge_card", "payload", "str")
    .add_method("reconcile_batch", "raw", "void")
    .add_method("parse_iso8583", "buf", "dict"),
    xy=(71.0, 32.0),
)
ledger = diagram.add(
    ClassNode("LedgerRepository", width=29.0)
    .add_attribute("db_pool", "Pool", is_public=False)
    .add_method("append_entry", "tx", "UUID")
    .add_method("query_audit", "id", "list"),
    xy=(118.0, 32.0),
)

diagram.connect(ctrl, orch, "dependency", start_side="right", end_side="left", label="delegates", directed=True)
diagram.connect(orch, notif, "dependency", start_side="right", end_side="left", label="notifies", directed=True)
diagram.connect(ctrl, fraud, "dependency", start_side="bottom", end_side="top", label="validates", directed=True)
diagram.connect(orch, gateway, "composition", start_side="bottom", end_side="top", label="invokes", directed=True)
diagram.connect(fraud, gateway, "association", start_side="right", end_side="left", label="scores", directed=True)
diagram.connect(gateway, ledger, "association", start_side="right", end_side="left", label="records", directed=True)

diagram.draw(xy=(0.0, 0.0))

overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="contour",
    levels=4,
    max_alpha=0.45,
)
overlay.add_spot(gateway, value=0.96, radius=20.0)
overlay.add_spot(orch, value=0.72, radius=16.0)
overlay.add_spot(fraud, value=0.55, radius=14.0)
overlay.draw(xy=(0.0, 0.0))

overlay.draw_legend(
    xy=(43.0, 6.0),
    text_style=Styles.Muted.patch(text_size=10.0),
    orientation="horizontal",
    labels=["Low", "Moderate", "High", "Critical"],
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/05_charts/heatmap/heatmap_overlay_contour_mode.png" alt="heatmap_5" />
  <figcaption class="drawlib-caption">同心ベクター等値線リングを重ね合わせた 6 クラス UML クラス図 (mode='contour')</figcaption>
</figure>



---

## 5. クラウドアーキテクチャのレイテンシ・障害オーバーレイ（`ArchitectureDiagram` + `HeatmapOverlay`）

`HeatmapOverlay.add_spot()` は `ArchitectureDiagram` の `Node` および `NodeGroup` インスタンスも直接受け取ることができます。ネストされた `NodeGroup` 階層の座標オフセットが自動解決されるため、クラウドアーキテクチャ図の上でインフラのボトルネック、CPU 飽和、または P99 レイテンシスパイクを直感的に強調できます。



```python
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup
from drawlib.styles import Colors, Styles

setup(width=140, height=88)

arch = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=9.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    node_card_style=Styles.Neutral.patch(shape_fill_color=Colors.White, shape_r=1.2),
)

vpc = arch.add(
    NodeGroup(
        title="Production Cloud VPC",
        padding=5.5,
        style=Styles.Neutral,
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="top"),
    ),
    xy=(8.0, 15.0),
)

# Edge Ingress
lb = vpc.add(
    Node("Cloud Load\nBalancing", width=22.0, height=16.0, icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=6.8),
    xy=(15.0, 25.0),
)

# Compute Subnet
compute_grp = vpc.add(
    NodeGroup(
        title="GKE Compute Tier",
        padding=4.5,
        style=Styles.PrimaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.0, halign="left", valign="top"),
    ),
    xy=(36.0, 4.0),
)
api_svc = compute_grp.add(
    Node("Catalog API", width=22.0, height=15.0, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=6.5),
    xy=(14.0, 33.0),
)
checkout_svc = compute_grp.add(
    Node("Checkout Worker", width=22.0, height=15.0, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=6.5),
    xy=(14.0, 12.0),
)

# Data Subnet
data_grp = vpc.add(
    NodeGroup(
        title="Stateful Data Tier",
        padding=4.5,
        style=Styles.SecondaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.0, halign="left", valign="top"),
    ),
    xy=(82.0, 4.0),
)
cache_node = data_grp.add(
    Node("Memorystore\nRedis", width=22.0, height=15.0, icon=GcpIcon.MEMORYSTORE, icon_size=6.5),
    xy=(14.0, 33.0),
)
sql_primary = data_grp.add(
    Node("Cloud SQL\nPrimary (Lock!)", width=22.0, height=15.0, icon=GcpIcon.CLOUD_SQL, icon_size=6.5),
    xy=(14.0, 12.0),
)

lb.fork([api_svc, checkout_svc], at_x=34.0, padding=1.0)
api_svc.connect(cache_node, label="read", padding=1.0)
checkout_svc.connect(sql_primary, label="tx write", padding=1.0)

arch.draw(xy=(0.0, 0.0))

# Overlay thermal hotspots directly on nested ArchitectureDiagram Nodes
overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.58,
    width=140.0,
    height=77.0,
    title="Production VPC: P99 Latency & Saturation Hotspot Analysis",
    title_style=Styles.BlackBold.patch(text_size=13.0),
)
overlay.add_spot(sql_primary, value=0.96, radius=19.0)
overlay.add_spot(checkout_svc, value=0.72, radius=17.0)
overlay.add_spot(lb, value=0.35, radius=14.0)
overlay.draw(xy=(0.0, 0.0))

overlay.draw_colorbar(
    xy=(46.0, 5.5),
    text_style=Styles.Muted.patch(text_size=10.0),
    length=48.0,
    thickness=2.2,
    label="P99 Latency / Saturation Score",
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/05_charts/heatmap/heatmap_overlay_architecture.png" alt="heatmap_6" />
  <figcaption class="drawlib-caption">サーマルボトルネックを重ね合わせたクラウド VPC アーキテクチャ図</figcaption>
</figure>



---

## 6. 地理的トラフィック・地域別ヒートマップ（`GeoMap` + `HeatmapOverlay`）

`GeoMap`（`drawlib.smartarts.GeoMap`）と組み合わせる場合は、`gmap.get_area_xy(area)`（国名・都道府県名・市区町村名による指定）または `gmap.lonlat_to_xy(lon, lat)`（経緯度による指定）を `overlay.add_spot()` に直接渡すことで、世界地図・国別地図・都市地図の上に地理的ヒートマップを構築できます。



```python
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.shapes import rectangle
from drawlib.smartarts import GeoMap
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=140, height=78)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
rectangle((36.5, 43.0), width=65.0, height=58.0, style=card_style)
rectangle((103.5, 43.0), width=65.0, height=58.0, style=card_style)

text((36.5, 68.5), "1. Global Edge Traffic (GeoMap.World.All)", style=Styles.BlackBold.patch(text_size=11.0))
text((103.5, 68.5), "2. Domestic Load by Prefecture (GeoMap.Countries.Japan)", style=Styles.BlackBold.patch(text_size=11.0))

# Left: World Map + HeatmapOverlay
world = GeoMap(GeoMap.World.All, area_style=Styles.Neutral)
world.draw(xy=(6.5, 16.0), width=60.0, height=48.0)

world_overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.62,
    min_value=0.0,
    max_value=1.0,
)
world_overlay.add_spot(world.get_area_xy("Japan"), value=0.95, radius=9.5, label="Tokyo")
world_overlay.add_spot(world.get_area_xy("United States"), value=0.85, radius=11.0, label="US-East")
world_overlay.add_spot(world.get_area_xy("Germany"), value=0.72, radius=9.5, label="EU-Central")
world_overlay.add_spot(world.get_area_xy("Singapore"), value=0.60, radius=8.5, label="Singapore")
world_overlay.add_spot(world.get_area_xy("Brazil"), value=0.40, radius=8.0)
world_overlay.draw(xy=(0.0, 0.0))

# Right: Japan Map + HeatmapOverlay
jp = GeoMap(GeoMap.Countries.Japan, area_style=Styles.Neutral)
jp.draw(xy=(73.5, 16.0), width=60.0, height=48.0, lon_range=(129, 146), lat_range=(30, 46))

jp_overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.65,
    min_value=0.0,
    max_value=1.0,
)
jp_overlay.add_spot(jp.get_area_xy("Tokyo"), value=0.98, radius=10.5, label="Tokyo")
jp_overlay.add_spot(jp.get_area_xy("Osaka"), value=0.80, radius=8.5, label="Osaka")
jp_overlay.add_spot(jp.get_area_xy("Aichi"), value=0.62, radius=7.0)
jp_overlay.add_spot(jp.get_area_xy("Fukuoka"), value=0.55, radius=7.5, label="Fukuoka")
jp_overlay.add_spot(jp.lonlat_to_xy(141.35, 43.06), value=0.45, radius=7.5, label="Sapporo")
jp_overlay.draw(xy=(0.0, 0.0))

jp_overlay.draw_colorbar(
    xy=(46.0, 5.0),
    text_style=Styles.Muted.patch(text_size=10.0),
    length=48.0,
    thickness=2.2,
    label="Normalized Traffic Intensity",
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/05_charts/heatmap/heatmap_overlay_geomap.png" alt="heatmap_7" />
  <figcaption class="drawlib-caption">GeoMap 上の地理的トラフィック・エッジリクエストのヒートマップ（世界・日本）</figcaption>
</figure>



