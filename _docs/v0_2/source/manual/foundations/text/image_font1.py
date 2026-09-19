from drawlib.apis import *

config(width=100, height=60, grid_only=True)
text(xy=(25, 5), text="Hello Drawlib.", style=TextStyle(font=Font.SANSSERIF_LIGHT))
text(xy=(25, 15), text="Hello Drawlib.", style=TextStyle(font=Font.SANSSERIF_REGULAR))
text(xy=(25, 25), text="Hello Drawlib.", style=TextStyle(font=Font.SANSSERIF_BOLD))
text(xy=(25, 35), text="Hello Drawlib.", style=TextStyle(font=Font.SERIF_LIGHT))
text(xy=(25, 45), text="Hello Drawlib.", style=TextStyle(font=Font.SERIF_REGULAR))
text(xy=(25, 55), text="Hello Drawlib.", style=TextStyle(font=Font.SERIF_BOLD))

text(xy=(75, 5), text="Hello Drawlib.", style=TextStyle(font=FontRoboto.ROBOTO_REGULAR))
text(xy=(75, 15), text="Hello Drawlib.", style=TextStyle(font=FontSansSerif.RALEWAYS_REGULAR))
text(xy=(75, 25), text="Hello Drawlib.", style=TextStyle(font=FontSerif.MERRIWEATHER_REGULAR))
text(xy=(75, 35), text="Hello Drawlib.", style=TextStyle(font=FontMonoSpace.SOURCECODEPRO_REGULAR))
text(xy=(75, 45), text="こんにちは Drawlib.", style=TextStyle(font=FontJapanese.MPLUS1P_REGULAR))
text(xy=(75, 55), text="สวัสดี ดรอว์ลิบ", style=TextStyle(font=FontThai.SERIF_REGULAR))

save()
