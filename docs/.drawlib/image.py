from drawlib import *

IMAGE_PIKACHU = 'pikachu'

if not has_cache_image(IMAGE_PIKACHU):
    set_cache_image(IMAGE_PIKACHU, Pimage("./image.png"))
