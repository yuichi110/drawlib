# プロジェクト概要

[Drawlib](https://github.com/yuichi110/drawlib) で作成されたドキュメントサイトへようこそ。

## 1. 基本構成（プリミティブ API）

Drawlib の基本図形描画機能のみを使用したシンプルな構成図です：

```drawlib 600px center caption:"基本アーキテクチャ構成図"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# 基本図形描画関数を使用したサービスノード
rectangle((25, 22.5), width=28, height=18, style=Styles.PrimaryFlat, text="クライアント", textstyle=Styles.WhiteBold)
rectangle((75, 22.5), width=28, height=18, style=Styles.AccentFlat, text="バックエンド API", textstyle=Styles.WhiteBold)

# 矢印付き接続線
line((39, 22.5), (61, 22.5), arrowhead="->", style=Styles.PrimaryBold)
```

## 2. 応用構成（ユーティリティとアセット）

`utils.py` で定義した再利用可能な描画コンポーネントと、`_assets/` ディレクトリに配置した画像アセットを組み合わせた実践例です：

```drawlib 600px center caption:"共通ヘルパーと画像アセットを活用した構成図"
from drawlib.canvas import setup
from drawlib.images import image
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=110, height=52)

# utils.py の共通ヘルパー関数によるサービス描画
service_card((20, 24), title="Web クライアント", subtitle="Browser / App")
service_card((55, 24), title="Linux サーバー", subtitle="Ubuntu / Nginx", style=Styles.AccentFlat)
service_card((90, 24), title="データベース", subtitle="PostgreSQL", style=Styles.SecondaryFlat)

# プロトコルラベル付き接続線
connect((32, 24), (43, 24), label="HTTPS")
connect((67, 24), (78, 24), label="SQL")

# docs_src/_assets/ 配下のローカル画像アセットの埋め込み
image((55, 41), width=8, image="_assets/linux.png")
```

ドキュメントの各章:
- [システムアーキテクチャ](architecture/index.md)
- [業務ワークフロー](workflow/index.md)
