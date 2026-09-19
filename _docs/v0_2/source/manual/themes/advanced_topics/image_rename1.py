from drawlib.apis import *

# style code
dtheme.apply_official_theme("default")
dtheme.allstyles.rename("red", "1")
dtheme.allstyles.rename("green", "2")
dtheme.allstyles.rename("blue", "3")

# illustration code
config(width=100, height=50)
circle((20, 25), radius=10, style="1")
rectangle((50, 25), width=20, height=20, style="2")
text((80, 25), text="Hello\nDrawlib!", size=28, style="3")
save()
