from drawlib.apis import *

dtheme.apply_official_theme("essentials")
config(width=100, height=50)

bl = dsart.BoxList(default_text_style="white")
bl.extend(["1", "2", "3", "4"])


bl.draw(xy=(5, 35), box_width=8, box_height=6, align="left")
circle((5, 35), 0.5, style="red_flat")
text((25, 32), 'align="left" (default)')

bl.draw(xy=(45, 15), box_width=8, box_height=6, align="right")
circle((45, 15), 0.5, style="red_flat")
text((25, 12), 'align="right"')

bl.draw(xy=(65, 5), box_width=8, box_height=6, align="bottom")
circle((65, 5), 0.5, style="red_flat")
text((69, 32), 'align="bottom"')

bl.draw(xy=(85, 45), box_width=8, box_height=6, align="top")
circle((85, 45), 0.5, style="red_flat")
text((89, 18), 'align="top"')

save()
