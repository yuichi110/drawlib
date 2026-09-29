from drawlib.canvas import save, setup
from drawlib.lines import line, line_curved, lines
from drawlib.styles import Colors, Styles

setup(width=100, height=50, grid=True, background_color=Colors.canvas)
line((10, 25), (40, 25), arrowhead="->", style=Styles.Primary)
line_curved((60, 10), (90, 40), bend=0.3, style=Styles.Primary)
lines([(25, 10), (50, 40), (75, 10)], style=Styles.Primary)

save()
