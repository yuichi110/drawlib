# 第1章: システム全体概要

## はじめに

本章では、Drawlib の基本図形描画機能のみを使用したシステム全体の基本アーキテクチャについて解説します。

```drawlib center file:system_overview.png caption:"システム全体構成（基本図形）"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# 基本図形描画関数を使用したサービスノード
rectangle((25, 22.5), width=28, height=18, style=Styles.PrimaryFlat, text="クライアント", text_style=Styles.WhiteBold)
rectangle((75, 22.5), width=28, height=18, style=Styles.AccentFlat, text="クラウド基盤", text_style=Styles.WhiteBold)

# 矢印付き接続線
line((39, 22.5), (61, 22.5), arrow_head="->", style=Styles.PrimaryBold)
```

クライアントアプリケーションは、安全な通信経路を通じてクラウドバックエンドサービスと通信します。
