from drawlib.apis import *

config(width=100, height=50)
text(
    (50, 25),
    "Hello Drawlib!",
    style=TextStyle(
        size=36,
        font=FontFile("./avenger/regular.ttf"),
    ),
)
save()
