from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.config import styles

setup(width=100, height=50, grid=True)
line((20, 7), (80, 7), style=styles.primary)
line(
    (20, 16),
    (80, 16),
    style=styles.dashed.patch(line_width=5, line_color=Colors.Red),
)
line((20, 25), (80, 25), arrowhead="->", style=styles.primary)
line((20, 34), (80, 34), arrowhead="<->", style=styles.primary)
line(
    (20, 43),
    (80, 43),
    arrowhead="<-",
    style=styles.primary.patch(line_arrow_head_scale=50, line_style="dashdot", line_arrow_head_fill=True),
)

save()

