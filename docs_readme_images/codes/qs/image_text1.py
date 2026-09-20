from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.fonts import FontFile, FontRoboto
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=50)

text((50, 7), "Hello drawlib. こんにちは。")
text(
    (50, 16),
    "Hello drawlib. こんにちは。",
    angle=10,
    style=Style(text_font=FontRoboto.ROBOTO_REGULAR),
)
text(
    (50, 25),
    "Hello drawlib.",
    style=Style(text_font=FontFile("avenger/regular.ttf")),
)
text(
    (50, 34),
    "Hello drawlib. こんにちは。",
    style=Style(text_color=Colors.Red, text_size=24),
)
text(
    (50, 43),
    "Hello drawlib. こんにちは。",
    style=Style(text_color=Colors.White, text_bg_fill_color=Colors.Black),
)
save()
