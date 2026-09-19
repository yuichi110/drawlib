from drawlib.apis import *

config(width=100, height=50, grid=True)

t1 = dsart.Table()
t1.draw(
    xy=(5, 45),
    width=40,
    height=40,
    data=[
        ["Name", "Gendor", "Age"],
        ["Ada", "Female", "1"],
        ["Bob", "Male", "2"],
        ["Cindy", "Female", "3"],
        ["David", "Male", "4"],
    ],
)

save()
