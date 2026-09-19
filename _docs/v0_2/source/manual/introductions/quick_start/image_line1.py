from drawlib.apis import *

config(width=100, height=50, grid=True)

line((20, 7), (80, 7))
line_curved((20, 20), (80, 20), bend=0.2)
line_curved((20, 30), (80, 30), bend=-0.2)
lines([(20, 40), (30, 45), (70, 45), (80, 40)])

save()
