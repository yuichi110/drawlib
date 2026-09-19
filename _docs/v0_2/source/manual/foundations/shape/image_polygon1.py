from drawlib.apis import *

config(width=100, height=50, grid_only=True)
polygon(xys=[(25, 20), (30, 25), (25, 45), (20, 25)])
polygon(xys=[(70, 25), (75, 20), (95, 25), (75, 30)], text="polygon()")
save()
