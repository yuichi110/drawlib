# 第1章: システム全体概要

## はじめに

本章では、Drawlib の基本図形描画機能を使用したシステム全体のハイレベル構成について解説します（複数言語間で共有され 1 回だけ描画されます）。

```drawlib align=center file=system_overview.png caption="システム全体構成図"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# Standard shapes drawn with primitive functions
rectangle((25, 22.5), width=28, height=18, style=Styles.PrimaryFlat, text="Client App", text_style=Styles.WhiteBold)
rectangle((75, 22.5), width=28, height=18, style=Styles.AccentFlat, text="Cloud Backend", text_style=Styles.WhiteBold)

# Connecting line with arrow
line((39, 22.5), (61, 22.5), arrow_head="->", style=Styles.PrimaryBold)
```

クライアントアプリケーションは、安全な通信経路を通じてクラウドバックエンドサービスと通信します。
