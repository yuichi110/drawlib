from drawlib.canvas import config, save
from drawlib.lines import line, line_curved, lines
from drawlib.preset_styles import get_styles

config(width=100, height=50, grid=True)
ps = get_styles()

line((10, 25), (40, 25), arrowhead="->", style=ps.primary)
line_curved((60, 10), (90, 40), bend=0.3, style=ps.primary)
lines([(25, 10), (50, 40), (75, 10)], style=ps.primary)

save()

