"""write docstring later"""

from typing import Optional, Union, Any
import os
from PIL.Image import Image
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.offsetbox as offsetbox
from drawlib._util import error_handler, get_script_relative_path

_image_cache: dict[Union[str, Image], Any] = {}


@error_handler
def get_image(
    x: float,
    y: float,
    file: Optional[str] = None,
    pilimg: Optional[Image] = None,
    zoom: float = 0.1,
) -> offsetbox.AnnotationBbox:
    """write docstring later"""

    if file is None and pilimg is None:
        raise ValueError('requires one of args "file" or "image".')
    if file and pilimg:
        raise ValueError('suports only one args "file" or "image".')

    if file is not None:
        path = get_script_relative_path(file)
        if not os.path.exists(path):
            raise FileNotFoundError('image file "{path}" does not exist.')

        if path not in _image_cache:
            im = pyplot.imread(path)
            _image_cache[path] = im
        else:
            im = _image_cache[path]
    else:
        key = str(pilimg)
        if key not in _image_cache:
            im = numpy.array(pilimg)
            _image_cache[key] = im
        im = _image_cache[key]

    imagebox = offsetbox.OffsetImage(im, zoom=zoom)
    ab = offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False)
    return ab
