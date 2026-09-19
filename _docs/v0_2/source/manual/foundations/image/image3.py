import PIL.Image
from drawlib.apis import *

file_path = dutil_script.get_relative_path("python.png")
print(file_path)
# /Users/yuichi/GitHub/drawlib_docs/v0_1/docs/source/manual/foundations/image/python.png

config(width=100, height=50, grid_only=True)

# specify file
image(xy=(20, 25), width=20, image="python.png")

# specify Dimage
dimage = Dimage("python.png")
image(xy=(50, 25), width=20, image=dimage)

# specify PIL Image
pil_image = PIL.Image.open(file_path)
image(xy=(80, 25), width=20, image=pil_image)
save()
