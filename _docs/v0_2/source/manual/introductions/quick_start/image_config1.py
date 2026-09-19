from drawlib.apis import *

config(width=200, height=100)

line((10, 10), (90, 90))
circle((25, 75), radius=20)
image((75, 25), width=30, image="python.png")
text((75, 5), "Hello drawlib!")

save()
