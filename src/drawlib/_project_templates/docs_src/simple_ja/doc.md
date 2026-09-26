# システム設計書

[Drawlib](https://github.com/yuichi110/drawlib) を利用したスタンドアロンドキュメントのサンプルです。

## 概要図

```drawlib
setup(width=100, height=50)

rectangle((25, 25), width=30, height=20, style=styles.blue_flat, text="クライアント", textstyle=styles.white_bold)
rectangle((75, 25), width=30, height=20, style=styles.green_flat, text="API サーバー", textstyle=styles.white_bold)
line((40, 25), (60, 25), arrowhead="->", style=styles.bold)
```

このドキュメントは単一の HTML ファイルおよび GitHub 用 Markdown にコンパイルされます。
