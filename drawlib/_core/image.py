from typing import Optional, Union, Tuple
from PIL.Image import Image
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.offsetbox as offsetbox
from matplotlib.axes import Axes
import matplotlib as mpl
from drawlib._util import error_handler

_image_cache: dict[Union[str, Image], numpy.array] = {}


@error_handler
def get_image(
    x: float,
    y: float,
    file: Optional[str] = None,
    pilimg: Optional[Image] = None,
    zoom: Optional[float] = 0.1,
):
    if file is None and pilimg is None:
        raise ValueError('requires one of args "file" or "image".')
    if file and pilimg:
        raise ValueError('suports only one args "file" or "image".')

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
