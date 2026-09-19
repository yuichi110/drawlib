from drawlib.apis import *

config(width=100, height=50)
line_curved(xy1=(10, 20), xy2=(90, 20), bend=0.4)
text((50, 7), "0.4")
line_curved(xy1=(10, 23), xy2=(90, 23), bend=0.2)
text((50, 18), "0.2")
line_curved(xy1=(10, 27), xy2=(90, 27), bend=-0.2)
text((50, 32), "-0.2")
line_curved(xy1=(10, 30), xy2=(90, 30), bend=-0.4)
text((50, 43), "-0.4")
save()
