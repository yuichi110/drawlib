# 1. なぜ Drawlib なのか？

現代のソフトウェア開発では、プルリクエスト・CI/CD パイプライン・AI コーディングエージェント（Claude Code, Cursor, Gemini CLI, GitHub Copilot 等）の普及によって実装コードが驚異的なスピードで進化する一方、開発のボトルネックは**「設計・アーキテクチャの可視化とドキュメントの同期（Documentation Rot の防止）」**へと移っています。システム構成図やシーケンス図・DB スキーマ図が手作業の別ツールに置き去りにされると、実装との乖離によってドキュメントが形骸化し、新規メンバーや AI セッションの全体把握が遅れ、最新の設計意図がチャット履歴やコミットログに埋もれてしまいます。

Drawlib は、**純粋 Python による宣言的な作図（Illustration as Code）**と**図解がファーストクラスで統合された技術文書出版（Illustrated Documentation as Code / IDaC）**を単一の Git リポジトリで実現し、エンジニアと AI エージェントがコードとまったく同じ開発体験で作図・差分レビュー・視覚検証・自動出版を行える基盤を提供します。

```drawlib align=center code=fold file=why_drawlib_hero_ja.png caption="図 1.1: 分断された従来の作図運用と Drawlib の Git 統合ワークフローの比較"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles

setup(width=148, height=66)

left_panel = Panel(
    "従来の分断された作図運用",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.MutedNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.warning,
    icon_style=Styles.DangerBold,
    header_height=9.0,
)
left_panel.draw((5.0, 5.0), width=65.0, height=56.0)

legacy_cards = CardList(
    style=Styles.White.patch(shape_r=1.6),
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Dark.patch(text_size=10.0),
    badge_style=Styles.MutedNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.5),
    icon_style=Styles.DarkBold,
    spacing=2.2,
    show_arrows=True,
    arrow_style=Styles.MutedBold,
)
legacy_cards.add(
    "GUI ツールでの手作業編集",
    "バイナリや巨大 XML によりコードレビュー困難",
    badge_text="1",
    icon=phosphor.wrench,
)
legacy_cards.add(
    "PNG 書き出し・手動貼り付け",
    "Wiki・設計書・スライドへ毎回手作業で転記",
    badge_text="2",
    icon=phosphor.images,
)
legacy_cards.add(
    "設計図の陳腐化と実装乖離",
    "PR 差分が追えず本番システムと図が不一致に",
    badge_text="3",
    icon=phosphor.warning,
    style=Styles.DangerNeutral.patch(shape_r=1.6),
    icon_style=Styles.DangerBold,
)
legacy_cards.draw((8.5, 8.0), width=58.0, height=41.0)

line((71.2, 33.0), (76.8, 33.0), arrow_head="->", style=Styles.DarkBold)

right_panel = Panel(
    "Drawlib の Git 統合ワークフロー",
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.check_circle,
    icon_style=Styles.PrimaryBold,
    header_height=9.0,
)
right_panel.draw((78.0, 5.0), width=65.0, height=56.0)

drawlib_cards = CardList(
    style=Styles.White.patch(shape_r=1.6),
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Dark.patch(text_size=10.0),
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.5),
    icon_style=Styles.DarkBold,
    spacing=2.2,
    show_arrows=True,
    arrow_style=Styles.DarkBold,
)
drawlib_cards.add(
    "Git 管理の Python & Markdown",
    "明快な PR 差分と単一の信頼できる情報源",
    badge_text="1",
    icon=phosphor.git_branch,
)
drawlib_cards.add(
    "Drawlib コンパイラ & AI 検証",
    "決定論的座標と -g グリッドによる自律検証",
    badge_text="2",
    icon=phosphor.cpu,
    style=Styles.PrimaryFlat.patch(shape_r=1.6),
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    description_style=Styles.White.patch(text_size=10.0),
    badge_style=Styles.White,
    badge_text_style=Styles.PrimaryBold.patch(text_size=10.5),
    icon_style=Styles.PrimaryBold,
)
drawlib_cards.add(
    "マルチ形式への一括ビルド出版",
    "HTML・辞書・PDF・DOCX・PPTX を自動生成",
    badge_text="3",
    icon=phosphor.globe,
    style=Styles.SecondaryNeutral.patch(shape_r=1.6),
)
drawlib_cards.draw((81.5, 8.0), width=58.0, height=41.0)

save()
```

---

## 1.1 既存ツールと AI 直接生成の限界

これまでソフトウェア開発現場では主に以下の 4 つのアプローチが試みられてきましたが、AI コーディング時代の実運用においてそれぞれ構造的な限界を抱えています。

- **GUI 作図ツールとバイナリ画像管理（`draw.io`・`Figma`・`Visio`・`Slides`）**: 画面上で直感的に配置できる反面、保存形式がバイナリ画像（`PNG` / `JPEG`）や膨大な XML となるため、Git のプルリクエスト上で意味のある差分レビューができません。AI エージェントがバイナリ画像の中身を直接編集することもできず、作成者ごとにフォント・色・余白が不統一になり、変更のたびに画像を手動エクスポートして Wiki・Word 仕様書・スライドへ貼り直す運用が設計図の形骸化を招きます。
- **テキスト DSL 系ツール（`Mermaid`・`PlantUML`・`Graphviz`）**: Markdown との親和性は高いものの、配置計算がブラックボックスな自動レイアウトエンジンに委ねられます。エッジを 1 本追加しただけで図全体の配置が崩れることが多く、細やかなタイポグラフィや余白制御、定量的な統計チャート（`BoxChart`・`HeatmapChart` 等）やリッチな SmartArts の表現には対応できません。
- **AI による生 SVG の直接生成**: AI エージェントに生 `<svg>` コードを直接出力させると、日本語（CJK）を含むテキストの折り返しやフォント幅の計測が困難なため枠からの文字はみ出しが多発します。さらに矢印やコネクタの座標計算ミスによる線の交差・位置ずれが起きやすく、何百行もの低レベルな `<path>` や `<rect>` タグは人間がレビュー・保守できません。
- **数値プロットライブラリの流用（`Matplotlib`・`Seaborn`）**: 学術計算グラフには優れていますが、システム構成図のノード・グループ枠・矢印ルーティング・34 種標準アイコンスイート・UML/ER 図・SmartArts・ドキュメント出版のための高レベル部品が存在しません。整った構成図を描くだけでも数百行のボイラープレートコードが必要となり、AI も構文エラーや座標崩れを起こしやすくなります。

| 評価軸 | GUI ツール (`draw.io` / `Visio`) | テキスト DSL (`Mermaid` / `PlantUML`) | 生 SVG / `Matplotlib` | **Drawlib (`v0.3.10`)** |
| :--- | :--- | :--- | :--- | :--- |
| **Git PR 差分の可読性** | 低（バイナリ・冗長な XML） | 高（簡潔なテキスト） | 低（大量の `<path>`・冗長コード） | **高（宣言的な Python コード）** |
| **レイアウト制御性** | 手動マウス操作のみ | ブラックボックス自動配置のみ | 軸・ピクセル座標の手動計算 | **精密なデカルト座標 + 5種自動ソルバー** |
| **表現領域の広さ** | 構成図・ワイヤーフレーム | 基本的なフロー・シーケンス | 低レベル図形または数値グラフのみ | **アイコン・SmartArts・チャート・構成図・アニメ** |
| **ドキュメント出版先** | 画像の手動書き出し | Web 上の埋め込み表示のみ | 単体画像ファイルのみ | **HTML・辞書・PDF・`.docx`・スライド・`.pptx`** |
| **AI 自律修正との親和性** | コーディング AI から操作不可 | 描画後の重なりを微調整困難 | 日本語はみ出し・座標崩れが多発 | **`-g` グリッドによるマルチモーダル自律修正** |

---

## 1.2 Drawlib を支える 3 つの柱

Drawlib `v0.3.10` は、技術的なビジュアル表現を再現可能なソフトウェア工学へと昇華させる **3 つの柱**を中心に設計されています。

```drawlib align=center code=fold file=drawlib_pillars_ja.png caption="図 1.2: Drawlib の3層アーキテクチャ — 基本図形・高レベル描画エンジンからマルチ形式出版まで"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess, Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=66)

stages = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.2),
    description_style=Styles.Dark.patch(text_size=10.0),
    spacing=2.0,
    flat_left_end=True,
)
stages.add("1. 基本図形とアイコン")
stages.add(
    "2. 高レベル描画エンジン",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.2),
)
stages.add("3. マルチ形式ドキュメント出版", style=Styles.SecondaryNeutral)
stages.draw((6.0, 49.0), width=136.0, height=11.5)

p1 = Panel(
    "基盤プリミティブ層",
    style=Styles.White.patch(shape_r=1.8),
    header_style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.cube,
    icon_style=Styles.DarkBold,
    header_height=7.8,
)
p1.draw((6.0, 18.0), width=43.0, height=28.0)
text(
    (10.0, 28.0),
    "• 43種の基本幾何図形\n• 曲線・直交ルーティング線\n• 日本語/欧文フォント管理\n• 34種ベクターアイコン群",
    style=Styles.Dark.patch(text_size=10.2, halign="left", text_line_spacing=1.45),
)

p2 = Panel(
    "宣言的ビジュアル層",
    style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.stack,
    icon_style=Styles.PrimaryBold,
    header_height=7.8,
)
p2.draw((52.5, 18.0), width=43.0, height=28.0)
text(
    (56.5, 28.0),
    "• 18種 SmartArts 部品\n• 10種の定量データチャート\n• 6種の専門ダイアグラム\n• 5種の自動グラフソルバー",
    style=Styles.Dark.patch(text_size=10.2, halign="left", text_line_spacing=1.45),
)

p3 = Panel(
    "統合パブリッシング層",
    style=Styles.White.patch(shape_r=1.8),
    header_style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.export,
    icon_style=Styles.DarkBold,
    header_height=7.8,
)
p3.draw((99.0, 18.0), width=43.0, height=28.0)
text(
    (103.0, 28.0),
    "• Web サイト & API 辞書\n• 単一 HTML & GitHub MD\n• ベクター PDF 出力\n• 編集可能な .docx / .pptx",
    style=Styles.Dark.patch(text_size=10.2, halign="left", text_line_spacing=1.45),
)

rectangle((74.0, 9.5), width=136.0, height=9.5, style=Styles.MutedDashed.patch(shape_r=1.8))
phosphor.grid_four((13.0, 9.5), width=5.0, style=Styles.PrimaryBold)
text(
    (18.5, 9.5),
    "第3の柱 — AI マルチモーダル自律ループ: 決定論的 (x, y) 座標系 + CLI グリッド検証 (drawlib show -g)",
    style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
)

save()
```

### 1.2.1 第1の柱：Illustration as Code（コードとしての作図）

Drawlib のすべての図解は、Pydantic による厳格な型検証と統一テーマプリセット（`GoogleStyles`・`DefaultStyles`・`MonochromeStyles`）を備えた純粋な Python コードとして記述されます。

- **豊富な高レベル表現コンポーネント**: 43 種の基本図形、曲線・直交コネクタ、**34 種のベクターアイコンスイート**（`phosphor`・`gcp`・`aws`・`azure`・15 種のドメイン別スイート等）に加え、**18 種の SmartArts**、**10 種の定量チャート**、**6 種の構成図・ソフトウェア設計図**、**5 種の自動グラフレイアウトソルバー**（`drawlib.graph`）、マルチフレーム**アニメーション**（`APNG`・`WebP`・`GIF`）を組み合わせられます。
- **Python 言語の表現力をそのまま活用**: JSON スキーマ、OpenAPI 定義、ベンチマーク CSV、あるいは `utils.py` に定義した共通マクロ関数から直接ダイアグラムを生成でき、手作業の転記ミスを根絶できます。

### 1.2.2 第2の柱：Illustrated Documentation as Code（図解ドキュメントのコード化）

Drawlib は単体画像の生成にとどまらず、Markdown 本文と埋め込み ```` ```drawlib ```` コードブロックを単一のコンパイル単位として統合します。

- **1 つのツールチェインで 5 つのプロジェクト種別に対応**: マルチページのドキュメントポータル（`site`）、検索可能な API/CLI リファレンス辞書（`catalog`）、章立ての技術白書（`doc`）、`16:9` ワイドスクリーンのプレゼンテーション（`slide`）、単体画像・アニメーション集（`images`）を標準搭載しています。
- **多言語・マルチ形式への一括ビルド**: `en/` と `ja/` の構造パリティ（章立て・図表対応）を自動検証しながら、レスポンシブ HTML（SEO メタデータ・`llms.txt` 対応）、GitHub 用 Markdown、ヘッドレス Chromium によるベクター PDF、編集可能な Word 文書（`.docx`）、ネイティブ PowerPoint（`.pptx`）を一括出力し、`.drawlib/cache.db` で高速に差分ビルドします。

### 1.2.3 第3の柱：AI マルチモーダル自律検証ループ

Drawlib は、人間のエンジニアとマルチモーダル AI コーディングエージェントの協業を前提としてゼロから設計されています。

- **決定論的座標系と `-g` グリッド検証**: 配置がブラックボックス化された DSL では AI が文字重なりをピンポイントで直せませんが、Drawlib のデカルト座標系と `drawlib show ... -g`（`10` 単位・`5` 単位の座標グリッド重畳出力）を使えば、AI が正確な座標値を読み取って修正できます。
- **自律的な視覚フィードバックループ**: AI エージェントはリポジトリの実装コードを読み取り、宣言的な作図ブロックを記述し、`-g` グリッド画像を視覚確認して文字切れや余白の偏りを自己修正する一連のループを数秒で完結できます（`drawlib rules show` による内蔵リファレンスも完備しています）。
