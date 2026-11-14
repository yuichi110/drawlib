# 6. 34種のアイコンスイートと画像アセット処理

システム構成図や技術ドキュメントに直感的な UI アイコン・公式クラウドサービスロゴ・鮮明なラスター画像を組み合わせることで、図解の情報伝達力は飛躍的に高まります。Drawlib はオンデマンド自動キャッシュ対応の**全 34 種の内蔵アイコンスイート**（`drawlib.icons`）と、非破壊画像変換およびサブキャンバス合成エンジン（`drawlib.images`）を標準搭載しています。

```drawlib align=center code=fold file=icon_suites_showcase_ja.png caption="図 6.1: UI グリフ・主要クラウド・15 領域ブランド・Original 2D スイートから成る全 34 種の内蔵アイコン"
from drawlib.canvas import save, setup
from drawlib.icons import (
    ai,
    aws,
    azure,
    cnative,
    data,
    gcp,
    original_ai,
    original_cnative,
    original_data,
    original_security,
    phosphor,
)
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=144, height=68)

hdr = Styles.DarkBold.patch(text_size=10.5, halign="left")
lbl = Styles.DarkBold.patch(text_size=10.0)
xs_l = [15.5, 30.2, 44.8, 59.5]
xs_r = [84.5, 99.2, 113.8, 128.5]

# 4 つのニュートラル分類カード
rectangle((37.5, 49.5), width=64.0, height=26.5, style=Styles.PrimaryNeutral.patch(shape_r=2.2))
rectangle((106.5, 49.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((37.5, 18.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((106.5, 18.5), width=64.0, height=26.5, style=Styles.SecondaryNeutral.patch(shape_r=2.2))

# 1. Phosphor 汎用 UI ベクターグリフ
text((9.0, 59.0), "1. 汎用 UI ベクターグリフ (phosphor)", style=hdr)
phosphor.cpu((xs_l[0], 50.2), width=7.2, style=Styles.Dark)
phosphor.database((xs_l[1], 50.2), width=7.2, style=Styles.PrimaryBold)
phosphor.shield_check((xs_l[2], 50.2), width=7.2, style=Styles.Success.patch(icon_style="fill"))
phosphor.git_branch((xs_l[3], 50.2), width=7.2, style=Styles.SecondaryBold)
for cx, name in zip(xs_l, ["cpu", "database", "shield", "git_branch"]):
    text((cx, 41.0), name, style=lbl)

# 2. 公式クラウドスイート (gcp, aws, azure)
text((78.0, 59.0), "2. 公式クラウド (gcp, aws, azure)", style=hdr)
gcp.cloud_run((xs_r[0], 50.2), width=7.8, style=Styles.Primary)
gcp.bigquery((xs_r[1], 50.2), width=7.8, style=Styles.Primary)
aws.aws_lambda((xs_r[2], 50.2), width=7.8, style=Styles.Primary)
azure.cosmos_db((xs_r[3], 50.2), width=7.8, style=Styles.Primary)
for cx, name in zip(xs_r, ["Cloud Run", "BigQuery", "Lambda", "Cosmos DB"]):
    text((cx, 41.0), name, style=lbl)

# 3. 15 領域のマルチブランドスイート (ai .. workspace)
text((9.0, 28.0), "3. 15 領域ブランド (ai, cnative, data...)", style=hdr)
ai.gemini((xs_l[0], 19.2), width=7.8, style=Styles.Primary)
cnative.kubernetes((xs_l[1], 19.2), width=7.8, style=Styles.Primary)
cnative.docker((xs_l[2], 19.2), width=7.8, style=Styles.Primary)
data.postgresql((xs_l[3], 19.2), width=7.8, style=Styles.Primary)
for cx, name in zip(xs_l, ["gemini", "k8s", "docker", "postgres"]):
    text((cx, 10.0), name, style=lbl)

# 4. style= による背景ティント＆枠線付き 15 種 original_* スイート
text((78.0, 28.0), "4. 15 種 original_* (style= ティント枠)", style=hdr)
tinted = Styles.Secondary.patch(
    image_tint_color=Colors.White,
    image_border_color=Colors.Secondary,
    image_border_width=1.0,
)
original_ai.ai_agent((xs_r[0], 19.2), width=7.8, style=tinted)
original_data.data_lakehouse((xs_r[1], 19.2), width=7.8, style=tinted)
original_security.zero_trust((xs_r[2], 19.2), width=7.8, style=tinted)
original_cnative.argo((xs_r[3], 19.2), width=7.8, style=tinted)
for cx, name in zip(xs_r, ["ai_agent", "lakehouse", "zero_trust", "argo"]):
    text((cx, 10.0), name, style=lbl)

save()
```

---

## 6.1 全 34 種の内蔵アイコンスイート体系

`drawlib.icons` のすべてのアイコン関数は、基本図形と共通の**中心アンカー `xy = (cx, cy)`**・`1:1` 正方形サイズ `width=`・必須キーワード引数 `*, style: Style` に統一されています。各スイートは初回使用時に自動ダウンロード＆キャッシュされます（オフライン CI 用に `uv run drawlib cache download --all` で一括事前取得も可能）。

| ティア | スイート構成（全 34 種） | 描画方式と `style=` カスタマイズ |
| :--- | :--- | :--- |
| **1. 汎用 UI ベクターアイコン (1)** | `phosphor`（1,500 種以上＋低レベル `font_icon`） | `style.icon_style`（`"thin"`, `"light"`, `"regular"`, `"bold"`, `"fill"` または `Styles.*Bold` / `*Flat`）の 5 ウェイトに対応する鮮明なベクターフォントグリフ。`style.icon_color` で直接着色可能。 |
| **2. 公式クラウドスイート (3)** | `gcp`, `aws`, `azure` | Google Cloud・AWS・Microsoft Azure の公式サービスアイコン（`512x512` RGBA）。 |
| **3. 領域別マルチブランド (15)** | `ai`, `business`, `client`, `cloud`, `cnative`, `code`, `data`, `devops`, `facility`, `itservice`, `network`, `security`, `server`, `social`, `workspace` | 生成 AI・CI/CD＆DevOps・コンテナ／Kubernetes（`cnative`）・DB／データ基盤（`data`）・フロントエンド（`client`）・サーバー／設備・ネットワーク・セキュリティ等の主要製品ロゴを網羅。 |
| **4. `original_*` 2D スイート (15)** | `original_ai` 〜 `original_workspace` | 各ブランドを統一トーンのフラット 2D パステル調に揃えたツイン版に加え、ベンダー中立な概念アイコン（`original_ai.ai_agent`・`original_data.data_lakehouse`・`original_security.zero_trust` 等）を収録。`style=` で背景ティント（`image_tint_color`）・外枠（`image_border_*`）・回転・透過を指定でき、`Dimage.colorize()` で単色リカラーも可能。 |

---

## 6.2 単体アイコン描画関数と高レベル Enum トークンの使い分け

アイコンの利用方法は、自由配置キャンバスか高レベル構成図かに応じて 2 通りのイディオムを使い分けます。

1. **単体関数の直接呼び出し（`drawlib.icons.<suite>.<name>`）**: `phosphor.cpu((25, 20), width=8.0, style=Styles.PrimaryBold)`（または `Styles.Accent.patch(icon_style="fill")`）や `gcp.cloud_run((60, 20), width=9.0, style=Styles.Primary)` のように、キャンバス上の中心座標 `(cx, cy)` へ直接描画します。
2. **型安全な Enum トークン（`PhosphorIcon`・`GcpIcon`・`AwsIcon`・`CnativeIcon` 等）**: 高レベル構成図モジュール（`drawlib.diagrams.architecture`・`drawlib.diagrams.sequence`）やアイコン対応 `SmartArts` では、`StrEnum` トークンを `Node(..., icon=GcpIcon.CLOUD_RUN)` のように渡すだけでアイコンとラベルの余白・整列が自動計算されます。

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, PhosphorIcon
from drawlib.icons import phosphor
from drawlib.styles import Styles

setup(width=120, height=40)

# 1. 中心座標 (cx, cy) を指定する単体アイコン描画
phosphor.sparkle((16, 20), width=7.5, style=Styles.Accent.patch(icon_style="fill"))

# 2. 高レベル ArchitectureDiagram への Enum トークン指定
arch = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=11.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)
gw = arch.add(Node("境界ゲートウェイ", width=34, height=16, icon=PhosphorIcon.SHIELD_CHECK), xy=(52, 20))
svc = arch.add(
    Node(
        "Cloud Run API",
        width=34,
        height=16,
        icon=GcpIcon.CLOUD_RUN,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(98, 20),
)
arch.connect(gw, svc, arrow="->")
arch.draw()

save()
```

---

## 6.3 ラスター画像（`image`）・`Dimage` 変換・サブキャンバス合成

画面キャプチャやマスコット画像、入れ子のミニ図解を扱うために、`drawlib.images` は 3 つの機能を提供します。

- **`image(xy, width=..., image="_assets/linux.png", style=...)`**: アスペクト比を維持したまま中心座標 `xy = (cx, cy)` に画像を配置します。移植性を保つため、画像ファイルは常に `_assets/` 配下に置き相対パス（`"_assets/linux.png"`）で参照します。`style.patch(angle=..., alpha=..., image_tint_color=..., image_border_width=..., image_border_color=..., image_border_style=...)` で回転・透過背景の塗りつぶし・枠線装飾を行えます。
- **イミュータブルな `Dimage` 変換チェーン**: `Dimage("_assets/linux.png")` で画像をラップすると、元画像を破壊せずにメソッドチェーンで加工できます。
  - **幾何変換・透過処理**: `.resize(width, height)`、**左下ピクセルを `(0, 0)` とする** `.crop(x, y, width, height)`、左右反転 `.mirror()`、上下反転 `.flip()`、余白自動除去 `.trim()`、背景透過化 `.make_transparent(color="auto", tolerance=15)`、透過部塗りつぶし `.fill(color)`、不透明度上限 `.alpha(0.8)`。
  - **色調・フィルタ処理**: `.grayscale()`・`.sepia()`・`.colorize(from_black_to=..., from_white_to=...)`・`.brightness(0.9)`・`.invert()`・`.posterize(num_colors=4)`・`.mosaic(block_size=16)`・`.blur()`・輪郭抽出 `.line_extraction()`。
- **インメモリ・サブキャンバス合成（`get_dimage_from_code`）**: 独立した Python 作図コード文字列を隔離プロセスでレンダリングし、メモリ上の `Dimage` として取得します。親キャンバスの状態に影響を与えずにミニバッジや Picture-in-Picture 図解を自在に合成できます。

```drawlib align=center code=fold file=dimage_pipeline_ja.png caption='図 6.2: Dimage("_assets/linux.png") の非破壊フィルタパイプラインとスタイル付きカードへの埋め込み'
from drawlib.canvas import save, setup
from drawlib.images import Dimage, get_dimage_from_code, image
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=144, height=62)

base = Dimage("_assets/linux.png")
xs = [20.5, 54.8, 89.2, 123.5]
card_w, card_h, cy = 28.5, 50.0, 31.0

title_st = Styles.DarkBold.patch(text_size=10.5)
code_st = Styles.Dark.patch(text_size=10.0)

# ステップ 1: 元のラスター画像アセット
rectangle((xs[0], cy), width=card_w, height=card_h, style=Styles.Neutral.patch(shape_r=2.2))
text((xs[0], 51.0), "1. 元画像", style=title_st)
image((xs[0], 31.8), width=14.5, image=base)
text((xs[0], 12.0), "Dimage(\n'_assets/linux.png')", style=code_st)

# ステップ 2: 左下基準 crop + 左右反転 mirror + 角度付き配置
rectangle((xs[1], cy), width=card_w, height=card_h, style=Styles.PrimaryNeutral.patch(shape_r=2.2))
text((xs[1], 51.0), "2. 切り抜き・回転", style=title_st)
cropped = base.crop(110, 340, 455, 440).mirror()
image(
    (xs[1], 31.8),
    width=14.5,
    image=cropped,
    style=Styles.Primary.patch(
        angle=10,
        image_border_width=1.2,
        image_border_color=Colors.Primary,
    ),
)
text((xs[1], 12.0), ".crop().mirror()\n+ angle=10", style=code_st)

# ステップ 3: グレースケール等の色調フィルタ
rectangle((xs[2], cy), width=card_w, height=card_h, style=Styles.Neutral.patch(shape_r=2.2))
text((xs[2], 51.0), "3. フィルタ変換", style=title_st)
image((xs[2], 31.8), width=14.5, image=base.grayscale())
text((xs[2], 12.0), ".grayscale()\n(.sepia / .blur)", style=code_st)

# ステップ 4: スタイル付きカードへの埋め込み + サブキャンバス合成
rectangle((xs[3], cy), width=card_w, height=card_h, style=Styles.SecondaryNeutral.patch(shape_r=2.2))
text((xs[3], 51.0), "4. カード合成", style=title_st)
rectangle(
    (xs[3], 43.8),
    width=22.5,
    height=5.6,
    style=Styles.PrimaryFlat.patch(shape_r=1.4),
    text="Linux ノード",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)
framed = base.resize(270, 320).fill(Colors.White)
image(
    (xs[3], 29.2),
    width=12.2,
    image=framed,
    style=Styles.Primary.patch(
        image_border_width=1.5,
        image_border_color=Colors.Primary,
    ),
)
sub_badge = get_dimage_from_code("""
from drawlib.canvas import setup
from drawlib.shapes import checkmark, circle
from drawlib.styles import Styles
setup(width=36, height=36)
circle((18, 18), radius=15, style=Styles.SuccessFlat)
checkmark((18, 18), width=15, style=Styles.WhiteFlat)
""").make_transparent(color="auto", tolerance=15)
image((xs[3] + 6.5, 22.8), width=5.6, image=sub_badge)
text((xs[3], 12.0), ".fill() + サブ描画\nget_dimage_from_code", style=code_st)

# 各ステージ間の矢印コネクタ
for i in range(3):
    line((xs[i] + 14.8, cy), (xs[i + 1] - 14.8, cy), arrow_head="->", style=Styles.DarkBold)

save()
```
