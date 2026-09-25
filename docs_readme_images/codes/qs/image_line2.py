from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.preset_styles import get_styles

config(width=100, height=50, grid=True)
ps = get_styles()

line((20, 7), (80, 7), style=ps.primary)
line(
    (20, 16),
    (80, 16),
    style=ps.dashed.patch(line_width=5, line_color=Colors.Red),
)
line((20, 25), (80, 25), arrowhead="->", style=ps.primary)
line((20, 34), (80, 34), arrowhead="<->", style=ps.primary)
line(
    (20, 43),
    (80, 43),
    arrowhead="<-",
    style=ps.primary.patch(line_arrow_head_scale=50, line_style="dashdot", line_arrow_head_fill=True),
)

save()

