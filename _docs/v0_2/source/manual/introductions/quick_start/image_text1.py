from drawlib.apis import *

config(width=100, height=50)

text((50, 7), "Hello drawlib. こんにちは。")
text(
    (50, 16),
    "Hello drawlib. こんにちは。",
    angle=10,
    style=TextStyle(font=FontRoboto.ROBOTO_REGULAR),
)
text(
    (50, 25),
    "Hello drawlib.",
    style=TextStyle(font=FontFile("avenger/regular.ttf")),
)
text(
    (50, 34),
    "Hello drawlib. こんにちは。",
    style=TextStyle(color=Colors.Red, size=24),
)
text(
    (50, 43),
    "Hello drawlib. こんにちは。",
    style=TextStyle(color=Colors.White, bgfcolor=Colors.Black),
)
save()
