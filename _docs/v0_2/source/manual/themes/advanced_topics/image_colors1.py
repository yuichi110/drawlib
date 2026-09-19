from drawlib.apis import *

config(width=100, height=50)

print(dtheme.colors.list())
# ['red', 'green', 'blue', 'black', 'white']

print(dtheme.colors.get("blue"))
# (109, 124, 197, 1.0)x
