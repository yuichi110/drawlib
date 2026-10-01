from drawlib.canvas import save, setup
from drawlib.fonts import FontFile, FontRoboto
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=100, height=50, color=Colors.Canvas)
text((50, 7), "Hello drawlib. こんにちは。", style=Styles.Primary)
text(
    (50, 16),
    "Hello drawlib. こんにちは。",
    angle=10,
    style=Styles.Primary.patch(text_font=FontRoboto.ROBOTO_REGULAR),
)
text(
    (50, 25),
    "Hello drawlib.",
    style=Styles.Primary.patch(text_font=FontFile("../_assets/avenger/regular.ttf")),
)
text(
    (50, 34),
    "Hello drawlib. こんにちは。",
    style=Styles.Primary.patch(text_color=Colors.Red, text_size=24),
)
text(
    (50, 43),
    "Hello drawlib. こんにちは。",
    style=Styles.Primary.patch(text_color=Colors.White, text_bg_fill_color=Colors.Black),
)
save()
