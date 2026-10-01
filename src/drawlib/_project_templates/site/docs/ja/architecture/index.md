# アーキテクチャ設計

システムの内部アーキテクチャ構成について解説します。

## コンポーネント構成

```drawlib 600px center caption:"コンポーネント構成詳細"
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=120, height=60)

# utils.py で定義したカスタムコンポーネントによるサービス描画
service_card((30, 42), title="フロントエンド UI", subtitle="Single Page App", width=34, height=18, style=Styles.primary_flat)
service_card((30, 18), title="認証サービス", subtitle="OAuth 2.0 / JWT", width=34, height=18, style=Styles.accent_flat)
service_card((90, 30), title="バックエンド", subtitle="マイクロサービス群", width=36, height=36, style=Styles.secondary_flat)

# プロトコルラベル付き接続線
connect((47, 42), (72, 35), label="HTTPS")
connect((47, 18), (72, 25), label="gRPC")
```
