# 第2章: 詳細設計

## コンポーネント構成

本章では、`utils.py` で定義した再利用可能な描画ヘルパーと、`_assets/` ディレクトリに配置した画像アセットを活用したマルチティア構成について解説します。

```drawlib align=center file=component_architecture.png caption="詳細コンポーネント構成図"
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

# Embedded local image asset from doc_src/_assets/ directory
image((55, 41), width=8, image="_assets/linux.png")
```

システムはクライアントアクセス、Linux ホスト上で稼働するアプリケーションロジック、および永続化ストレージに責務を分離しています。
