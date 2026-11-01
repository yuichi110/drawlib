# Roadmap（ロードマップ）

`Roadmap` コンポーネントは、垂直または水平のスパイン（主軸）に沿って、時系列タイムライン、アジェンダシーケンス、段階的なエンジニアリングロードマップを描画します。
各マイルストーンは、スパイン上のバッジ（`badge_text`）およびコネクタ線と、マイルストーンタイトル（`text`）・補足説明（`description`）・オプションのベクター `icon` を収めた角丸矩形またはピル型カード（`card_shape="rounded_rect" | "pill"`）を組み合わせて表現します。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/04_smartarts/roadmap/smartarts_roadmap_hero.png" alt="roadmap_1" />
  <figcaption class="drawlib-caption">Roadmap のスパインモード: 直線垂直タイムライン（curve_bend=0.0）と曲線ピル型アジェンダ（curve_bend=0.22）</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.smartarts import Roadmap
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=60)

# Subtle center divider
line((64.5, 4.0), (64.5, 56.0), style=Styles.MutedDashed)

# 1. Left Panel: Vertical Straight Spine (curve_bend=0.0, card_shape="rounded_rect")
phosphor.git_commit(xy=(5.5, 53.0), width=3.4, style=Styles.PrimaryFlat)
text((10.0, 54.5), "1. Straight Spine (curve_bend=0.0)", style=Styles.BlackBold.patch(text_size=10.5, halign="left"))

rm_straight = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.0,
    card_shape="rounded_rect",
)
rm_straight.add(
    "T+00m: Alert Triggered",
    "SYN flood hits 180 Gbps",
    badge_text="1",
    icon=phosphor.warning,
    badge_style=Styles.AccentFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
    icon_style=Styles.AccentBold,
)
rm_straight.add("T+02m: BGP Scrubbing", "Anycast diversion active", badge_text="2", icon=phosphor.shield_check)
rm_straight.add(
    "T+07m: SLA Restored",
    "Origin P99 at 11.4ms",
    badge_text="3",
    icon=phosphor.check_circle,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rm_straight.draw(xy=(5.0, 8.0), width=55.5, height=42.0)

circle((5.0, 8.0), radius=1.1, style=Styles.DangerFlat)
text((5.0, 3.8), "xy=(5, 8) [Bottom-Left]", style=Styles.DangerBold.patch(text_size=10.0, halign="left"))

# 2. Right Panel: Vertical Curved Spine (curve_bend=0.22, card_shape="pill")
phosphor.bezier_curve(xy=(68.5, 53.0), width=3.4, style=Styles.PrimaryFlat)
text((73.0, 54.5), "2. Curved Pill Agenda (curve_bend=0.22)", style=Styles.BlackBold.patch(text_size=10.5, halign="left"))

rm_curved = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.22,
    card_shape="pill",
)
rm_curved.add(
    "01. Core Engine",
    "Vector canvas & themes",
    badge_text="01",
    icon=phosphor.cube,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rm_curved.add("02. AI Agent CLI", "Headless build & grid review", badge_text="02", icon=phosphor.robot)
rm_curved.add("03. Cloud & GeoMap", "GCP icons & 215 maps", badge_text="03", icon=phosphor.globe_hemisphere_east)
rm_curved.draw(xy=(68.5, 8.0), width=58.5, height=42.0)

circle((68.5, 8.0), radius=1.1, style=Styles.DangerFlat)
text((68.5, 3.8), "xy=(68.5, 8) [Bottom-Left]", style=Styles.DangerBold.patch(text_size=10.0, halign="left"))

save()
```

</details>



---

## 1. 基本概念と基本的な使い方

`Roadmap` は `.add(text, description, badge_text=..., icon=...)` によって時系列タイムラインやマイルストーンアジェンダを段階的に構築し、デフォルトで `(width, height)` バウンディングボックス全体の**左下角 `(x, y)`**（`align="center"` の場合は中央）を基準に配置します。垂直スパインを滑らかなベジェ曲線へ湾曲させる表現（`curve_bend`, `card_shape="pill"`）や、`alternating=True` を伴う `direction="horizontal"` への切り替え、残りの要素の位置をずらさない `.items[i]` の強調・非表示化に対応しています。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/04_smartarts/roadmap/roadmap_parameter_tour.png" alt="roadmap_2" />
  <figcaption class="drawlib-caption">基本的な使い方とパラメータツアー: スパインとマイルストーン、ベジェ曲線とピル型カード、水平交互レイアウト、強調と中央配置（APNG アニメーション）</figcaption>
</figure>



<div class="drawlib-source-link">
  <a href="https://github.com/yuichi110/drawlib/blob/main/docs/docs_src/ja/04_smartarts/roadmap.md" target="_blank" rel="noopener noreferrer">GitHub でアニメーションのソースコードを見る &rarr;</a>
</div>

- **スパインとマイルストーンの構築（`.add()`, `xy`）**: `text`・`description`・`badge_text`・オプションの `icon` を持つマイルストーンを順に追加し、デフォルトで**左下 `xy`** を基準とする `(width, height)` 領域内に描画します。
- **ベジェ曲線とカード形状（`curve_bend`, `card_shape`）**: 直線矢印スパインと `"rounded_rect"` カードの組み合わせには `curve_bend=0.0` を維持し、滑らかな 2 次ベジェ曲線のアジェンダには `[-0.5, 0.5]` の範囲の `curve_bend` と `card_shape="pill"` を指定します。
- **垂直方向と水平方向の切り替え（`direction`, `alternating`）**: 左から右へ進むロードマップには `direction="horizontal"` を指定し、さらに `alternating=True` を有効にすると中央スパインの上下に偶数・奇数のマイルストーンカードを交互に配置できます。
- **動的な要素変更と中央配置（`.items[i]`, `align="center"`）**: `rm.items[i].style` を上書きして特定の注目マイルストーンを強調したり、`rm.items[i].show = False` で他の要素の位置をずらさずに非表示にしたり、`align="center"` でバウンディングボックスを `(cx, cy)` の中央に配置したりできます。

---

## 2. 垂直タイムラインと曲線アジェンダ（`direction="vertical"`）

`direction="vertical"`（デフォルト）では、マイルストーンが**上から下へ**流れます。`curve_bend=0.0` を設定すると下向き矢印付きの直線垂直スパインと円形マイルストーンバッジが描画され、`0` 以外の `curve_bend`（`-0.5` 〜 `0.5`）を設定するとスパインが 2 次ベジェ曲線に沿って湾曲し、各マイルストーンカードも曲線に追従して水平方向へシフトします。



```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import Roadmap
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=58)

text((6.0, 52.5), "Zero-Downtime Sharded Database Migration — Execution Timeline", style=Styles.DarkBold.patch(text_size=11.0, halign="left"))

migration = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.0,
    card_shape="rounded_rect",
)
migration.add(
    "Phase 1: Dual-Write Shadowing",
    "Replicate mutations to new Vitess shards via async CDC stream",
    badge_text="P1",
    icon=phosphor.git_branch,
)
migration.add(
    "Phase 2: Canary Read Verification",
    "Shadow-compare 10% of read queries for row-level checksum parity",
    badge_text="P2",
    icon=phosphor.magnifying_glass,
)
migration.add(
    "Phase 3: Atomic Cutover & Decommission",
    "Flip primary routing in Consul (< 50ms drain) and archive legacy replica",
    badge_text="P3",
    icon=phosphor.rocket_launch,
    style=Styles.PrimaryNeutral,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.5),
)
migration.draw(xy=(6.0, 5.0), width=108.0, height=44.0)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/04_smartarts/roadmap/smartarts_roadmap_vertical.png" alt="roadmap_3" />
  <figcaption class="drawlib-caption">垂直方向の Roadmap によるデータベース無停止マイグレーション実行タイムライン</figcaption>
</figure>



---

## 3. 上下交互配置の水平マイルストーンロードマップ（`direction="horizontal"`）

`direction="horizontal"` を指定すると、右向き矢印付きのスパインが**左から右へ**伸びます。`alternating=True` を設定すると、偶数インデックス（`0, 2, 4...`）のマイルストーンカードが水平スパインの**上側**に、奇数インデックス（`1, 3, 5...`）のカードが**下側**に交互に配置されるため、横方向の窮屈さを避けつつ長めのマイルストーンタイトル（`text`）や説明文（`description`）を収めることができます。



```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import Roadmap
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=56)

text((6.0, 50.5), "2026 Platform Engineering & Reliability Roadmap (Horizontal Alternating)", style=Styles.DarkBold.patch(text_size=11.0, halign="left"))

quarters = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="horizontal",
    alternating=True,
    card_shape="rounded_rect",
)
quarters.add(
    "Q1: Foundation",
    "Unified telemetry &\nOpenTelemetry SDK",
    badge_text="Q1",
    icon=phosphor.cube,
)
quarters.add(
    "Q2: Service Mesh",
    "Multi-cluster mTLS\n& envoy rate limits",
    badge_text="Q2",
    icon=phosphor.shield_check,
)
quarters.add(
    "Q3: Edge Compute",
    "Anycast Workers &\nregional KV cache",
    badge_text="Q3",
    icon=phosphor.lightning,
    style=Styles.PrimaryNeutral,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
)
quarters.add(
    "Q4: Autonomous DR",
    "Chaos game days &\nauto-failover drills",
    badge_text="Q4",
    icon=phosphor.rocket_launch,
)
quarters.draw(xy=(6.0, 4.0), width=116.0, height=43.0)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/04_smartarts/roadmap/smartarts_roadmap_horizontal.png" alt="roadmap_4" />
  <figcaption class="drawlib-caption">水平・上下交互レイアウトによる年間プラットフォームエンジニアリングロードマップ</figcaption>
</figure>



---

## 4. スパインモードと座標ジオメトリ

- **アンカー基準位置（`xy`, `align`）**: `Roadmap.draw(xy=(x, y), width=W, height=H, align="bottom_left")` は全体のバウンディングボックスの左下角を `(x, y)` に固定し、右方向（`+x`）に `W` 単位、上方向（`+y`）に `H` 単位の領域へ展開します。`align="center"` の場合は `(W, H)` のバウンディングボックスを `(x, y)` の中央に配置します。
- **垂直スパインモード（`direction="vertical"`）**:
  - `curve_bend = 0.0` *（デフォルト）*: 左側に下向き矢印（`->`）付きの直線垂直スパインを描画し、スパイン上の円形マイルストーンバッジから各カードへ水平コネクタ線を伸ばします。
  - `curve_bend != 0.0`（範囲 `-0.5` 〜 `0.5`）: 2 次ベジェ曲線スパイン（`line_bezier1`）を描画します。各マイルストーンバッジとカードは、`[0, 1]` 区間のパラメータ `t` に対する正確なベジェ曲線上の点 `B(t)` に沿って水平方向にオフセット配置されます。
- **水平スパインモード（`direction="horizontal"`）**:
  - `alternating = False` *（デフォルト）*: バウンディングボックスの下部付近に水平スパインを配置し、すべてのマイルストーンカードをスパイン上部の 1 行に揃えて並べます。
  - `alternating = True`: 垂直方向の中央線（`y0 + H/2`）に沿って水平スパインを配置し、カードをスパインの上下に交互に振り分けます。
- **カード形状（`card_shape`）**:
  - `"rounded_rect"` *（デフォルト）*: マイルストーンの `badge_style` と連動した左端アクセントストライプ付きの標準的な角丸矩形カード（`shape_r=2.0`）。
  - `"pill"`: 曲線型アジェンダレイアウトに最適なカプセル／スタジアム型カード（`shape_r = card_height / 2`）。

---

## 5. API リファレンス

### コンストラクタ
```python
Roadmap(
    *,
    style: Style,
    text_style: Style,
    spine_style: Style,
    badge_style: Style,
    badge_text_style: Style,
    description_style: Style | None = None,
    icon_style: Style | None = None,
    direction: Literal["vertical", "horizontal"] = "vertical",
    curve_bend: float = 0.0,
    card_shape: Literal["pill", "rounded_rect"] = "rounded_rect",
    alternating: bool = False,
    spacing: float = 2.5,
)
```

### メソッドとプロパティ
- **`add(text: str, description: str = "", *, badge_text: str | None = None, icon: Callable | None = None, style: Style | None = None, text_style: Style | None = None, description_style: Style | None = None, badge_style: Style | None = None, badge_text_style: Style | None = None, icon_style: Style | None = None, show: bool = True) -> RoadmapItem`**:
  マイルストーン項目（`text` がマイルストーンの主タイトル、`description` が補足説明・サブタイトル）を末尾に追加し、変更可能な `RoadmapItem` を返します。`item.show = False` を設定すると、スパイン（主軸）と残りの全マイルストーンの正確な位置を維持したまま、該当マイルストーンのバッジ・コネクタ・カードを非表示にします。
- **`roadmap.items -> list[RoadmapItem]`**:
  事後変更用の登録済み `RoadmapItem` インスタンスのリストを返します。
- **`draw(xy: tuple[float, float], width: float = 100.0, height: float = 60.0, *, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> Self`**:
  `xy`（デフォルトは左下角、`align="center"` の場合は中央）を基準とする `(width, height)` のバウンディングボックス内に、スパイン、マイルストーンバッジ、コネクタ、およびカードを描画します。

