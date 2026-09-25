# Simple Document

This is an example document created with [Drawlib](https://github.com/yuichi110/drawlib).

## Architecture Overview

```drawlib
config(width=100, height=50)

# Services
rectangle((25, 25), width=28, height=18, style=styles.blue_flat, text="API Gateway", textstyle=styles.white_bold)
rectangle((75, 25), width=28, height=18, style=styles.green_flat, text="Core Service", textstyle=styles.white_bold)

# Connection
line((39, 25), (61, 25), arrowhead="->", style=styles.bold)
text((50, 28), "REST", style=styles.primary)
```

Drawlib allows you to write illustrations as code directly embedded in Markdown.
