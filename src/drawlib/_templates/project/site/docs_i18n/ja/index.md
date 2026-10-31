# プロジェクト概要

[Drawlib](https://github.com/yuichi110/drawlib) で作成された多言語ドキュメントサイトへようこそ。

## 1. 基本構成（プリミティブ API）

Drawlib の基本図形描画機能のみを使用したシンプルな構成図です（複数言語間で共有され 1 回だけ描画されます）：

```drawlib align=center file=basic_architecture.png caption="基本アーキテクチャ構成図"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# Standard shapes drawn with primitive functions
rectangle((25, 22.5), width=28, height=18, style=Styles.PrimaryFlat, text="Client App", text_style=Styles.WhiteBold)
rectangle((75, 22.5), width=28, height=18, style=Styles.AccentFlat, text="Backend API", text_style=Styles.WhiteBold)

# Connecting line with arrow
line((39, 22.5), (61, 22.5), arrow_head="->", style=Styles.PrimaryBold)
```

## 2. 応用構成（ユーティリティとアセット）

`utils.py` で定義した再利用可能な描画コンポーネントと、`_assets/` ディレクトリに配置した画像アセットを組み合わせた実践例です：

```drawlib align=center file=reusable_helpers_architecture.png caption="共通ヘルパーと画像アセットを活用した構成図"
from drawlib.canvas import setup
from drawlib.images import image
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=110, height=52)

# Service nodes drawn using reusable helper from utils.py
service_card((20, 24), title="Web Client", subtitle="Browser / App")
service_card((55, 24), title="Linux Server", subtitle="Ubuntu / Nginx", style=Styles.AccentFlat)
service_card((90, 24), title="Database", subtitle="PostgreSQL", style=Styles.SecondaryFlat)

# Connections with protocol labels
connect((32, 24), (43, 24), label="HTTPS")
connect((67, 24), (78, 24), label="SQL")

# Embedded local image asset from docs_src/_assets/ directory
image((55, 41), width=8, image="_assets/linux.png")
```

ドキュメントの各章:
- [アーキテクチャ](architecture/index.md)
- [ワークフロー](workflow/index.md)
