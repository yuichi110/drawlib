::: block (80, 50) (1760, 120)
# Lines, Polylines & Bezier Curves (`drawlib.lines`)
Precision 1D vector connectors with straight, orthogonal, filleted, arc, and polynomial Bezier routing.
:::

::: block (80, 190) (780, 770) compact
### 7 Connector Primitives & Arrowheads

```python
from drawlib.lines import (
    line, line_arc, line_bezier1, line_bezier2,
    line_curved, lines, lines_curved,
)
from drawlib.styles import Styles

# 1. Straight line & orthogonal polyline
line((10, 70), (45, 70), arrow_head="->", style=Styles.DarkBold)
lines([(55, 65), (72, 65), (72, 75), (90, 75)],
      arrow_head="->", style=Styles.PrimaryBold)

# 2. Curved arc spline (bend) & filleted polyline (r)
line_curved((10, 44), (45, 44), bend=0.35,
            arrow_head="<->", style=Styles.PrimaryBold)
lines_curved([(55, 38), (72, 38), (72, 52), (90, 52)],
             r=4.0, arrow_head="->", style=Styles.DarkBold)

# 3. Quadratic/Cubic Beziers & Elliptical Arcs
line_bezier1((10, 16), (45, 16), cp=(27, 30),
             arrow_head="->", style=Styles.SecondaryBold)
line_bezier2((55, 10), (90, 24), cp1=(72, 10), cp2=(72, 24),
             arrow_head="->", style=Styles.BlueBold)
```

- **Arrowhead Options**: `""` (none), `"->"` (forward), `"<-"` (reverse), `"<->"` (bidirectional).
- **Filled vs. Stick Heads**: Customize via `style.patch(line_arrow_head_fill=True, line_arrow_head_scale=22)`.
:::

::: block (900, 180) (940, 780)
```drawlib file:lines_showcase.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import (
    line,
    line_arc,
    line_bezier1,
    line_bezier2,
    line_curved,
    lines,
    lines_curved,
)
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=82)

# Row 1: line() and lines()
rectangle((27, 68), width=42, height=22, r=2.5, style=Styles.LightFlat)
line((12, 71), (42, 71), arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))
line((12, 65), (42, 65), arrow_head="<->", style=Styles.PrimaryDashed.patch(line_width=2.0))
text((27, 59.5), 'line(arrow_head="->" / "<->")', style=Styles.DarkBold.patch(text_size=8.0))

rectangle((73, 68), width=42, height=22, r=2.5, style=Styles.LightFlat)
lines([(57, 64), (73, 64), (73, 74), (89, 74)], arrow_head="->", style=Styles.PrimaryBold.patch(line_width=2.2))
text((73, 59.5), "lines() Orthogonal Z-Bend", style=Styles.DarkBold.patch(text_size=8.0))

# Row 2: line_curved() and lines_curved()
rectangle((27, 41), width=42, height=22, r=2.5, style=Styles.LightFlat)
line_curved((12, 42), (42, 42), bend=0.35, arrow_head="->", style=Styles.PrimaryBold.patch(line_width=2.2))
line_curved((42, 40), (12, 40), bend=0.35, arrow_head="->", style=Styles.SecondaryBold.patch(line_width=2.0))
text((27, 32.5), "line_curved(bend=0.35)", style=Styles.DarkBold.patch(text_size=8.0))

rectangle((73, 41), width=42, height=22, r=2.5, style=Styles.LightFlat)
lines_curved([(57, 36), (73, 36), (73, 48), (89, 48)], r=4.5, arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))
text((73, 32.5), "lines_curved(r=4.5)", style=Styles.DarkBold.patch(text_size=8.0))

# Row 3: line_bezier1(), line_bezier2(), and line_arc()
rectangle((50, 14), width=88, height=22, r=2.5, style=Styles.LightFlat)

# Quadratic Bezier
line_bezier1((10, 11), (34, 11), cp=(22, 24), arrow_head="->", style=Styles.PrimaryBold.patch(line_width=2.2))
circle((22, 22), radius=1.0, style=Styles.AccentFlat)
text((22, 5.5), "line_bezier1(cp)", style=Styles.DarkBold.patch(text_size=8.0))

# Cubic Bezier S-curve
line_bezier2((40, 10), (64, 21), cp1=(52, 10), cp2=(52, 21), arrow_head="->", style=Styles.SecondaryBold.patch(line_width=2.2))
text((52, 5.5), "line_bezier2(cp1, cp2)", style=Styles.DarkBold.patch(text_size=8.0))

# Elliptical Arc
line_arc((80, 14), width=18, height=13, angle_start=20, angle_end=320, arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))
text((80, 5.5), "line_arc()", style=Styles.DarkBold.patch(text_size=8.0))

save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- `drawlib.lines` provides 1D vector connectors to link nodes and components.
- You can use straight `line()`, Manhattan orthogonal `lines()`, symmetric request-response arcs with `line_curved(bend=...)`, automatically filleted polylines with `lines_curved(r=...)`, quadratic/cubic Bezier splines (`line_bezier1`, `line_bezier2`), and circular retry loops (`line_arc`).
:::
