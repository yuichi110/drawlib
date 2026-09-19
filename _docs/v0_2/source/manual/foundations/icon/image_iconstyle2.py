from drawlib.apis import *

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10, style="green")
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10, style="red_light")
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10, style="blue_bold")
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10, style="green_flat")
save()
