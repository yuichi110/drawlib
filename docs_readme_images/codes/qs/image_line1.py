from drawlib.canvas import config, save
from drawlib.lines import line, line_curved, lines

config(width=100, height=50, grid=True)

line((10, 25), (40, 25), arrowhead="->")
line_curved((60, 10), (90, 40), bend=0.3)
lines([(25, 10), (50, 40), (75, 10)])

save()
