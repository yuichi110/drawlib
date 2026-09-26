from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.fonts import FontFile, FontRoboto
from drawlib.config import styles
from drawlib.text import text

setup(width=100, height=50)
text((50, 7), "Hello drawlib. こんにちは。", style=styles.primary)
text(
    (50, 16),
    "Hello drawlib. こんにちは。",
    angle=10,
    style=styles.primary.patch(text_font=FontRoboto.ROBOTO_REGULAR),
)
text(
    (50, 25),
    "Hello drawlib.",
    style=styles.primary.patch(text_font=FontFile("avenger/regular.ttf")),
)
text(
    (50, 34),
    "Hello drawlib. こんにちは。",
    style=styles.primary.patch(text_color=Colors.Red, text_size=24),
)
text(
    (50, 43),
    "Hello drawlib. こんにちは。",
    style=styles.primary.patch(text_color=Colors.White, text_bg_fill_color=Colors.Black),
)
save()

