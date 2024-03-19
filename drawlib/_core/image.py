from typing import Optional, Union
from PIL.Image import Image
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.offsetbox as offsetbox

_image_cache: dict[Union[str, Image], numpy.array] = {}


def get_image(
    x: float,
    y: float,
    file: Optional[str] = None,
    pilimg: Optional[Image] = None,
    zoom=1,
):
    if file is None and pilimg is None:
        raise ValueError()
    if file and pilimg:
        raise ValueError()

    if file:
        if file not in _image_cache:
            im = pyplot.imread(file)
            _image_cache[file] = im
        else:
            im = _image_cache[file]
    else:
        key = str(pilimg)
        if key not in _image_cache:
            im = numpy.array(pilimg)
            _image_cache[key] = im
        im = _image_cache[key]

    imagebox = offsetbox.OffsetImage(im, zoom=zoom)
    return offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False)
