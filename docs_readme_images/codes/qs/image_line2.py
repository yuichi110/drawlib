from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.types import LineStyle

config(width=100, height=50, grid=True)

line((20, 7), (80, 7))
line(
    (20, 16),
    (80, 16),
    style=LineStyle(line_style="dashed", line_width=5, line_color=Colors.Red),
)
line((20, 25), (80, 25), arrowhead="->")
line((20, 34), (80, 34), arrowhead="<->")
line((20, 43), (80, 43), arrowhead="<-", style=LineStyle(arrow_head_scale=50, line_style="dashdot", arrow_head_fill=True))

save()
