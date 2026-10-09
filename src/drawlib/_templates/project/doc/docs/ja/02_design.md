# 第2章: 詳細設計

## コンポーネント設計

本章では、`utils.py` で定義した再利用可能な描画コンポーネントと、`_assets/` ディレクトリに配置した画像アセットを活用した 3 層アーキテクチャの詳細設計について解説します。

```drawlib center file:component_architecture.png caption:"詳細コンポーネント構成図"
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

# doc_src/_assets/ 配下のローカル画像アセットの埋め込み
image((55, 41), width=8, image="_assets/linux.png")
```

システムはクライアントアクセス、Linux ホスト上で稼働するアプリケーションロジック、および永続化データベースに責務を分離しています。
