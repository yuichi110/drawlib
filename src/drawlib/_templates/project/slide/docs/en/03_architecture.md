::: block xy=(80, 40) width=1760 height=60
# Architecture
:::

::: block xy=(80, 140) width=740 height=840 font_size=22px
## Scalable Microservices in Code

- **Declarative Python**: Pure code, version-controlled with clean git diffs
- **Vector Native SVG**: Crisp scaling, Ctrl+F searchable text
- **Interactive Deck**: Fullscreen, keyboard shortcuts, overview modal
:::

::: block xy=(860, 140) width=980 height=840 z_index=5
```drawlib file=microservices.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

clear()
setup(width=100, height=60)
rectangle((25, 30), width=30, height=20, style=Styles.PrimaryFlat, text="Client SPA", text_style=Styles.WhiteBold)
rectangle((75, 30), width=30, height=20, style=Styles.SecondaryFlat, text="API Gateway", text_style=Styles.WhiteBold)
line((40, 30), (60, 30), arrow_head="->", style=Styles.PrimaryBold)
save()
```
:::

::: block xy=(80, 1010) width=1760 height=30 font_size=14px
*Drawlib Presentation*
:::
