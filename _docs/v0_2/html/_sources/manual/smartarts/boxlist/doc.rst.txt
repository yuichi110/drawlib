=============
BoxList
=============

BoxList draws list of texts within boxes.
Here is examples of BoxList.

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    image1.png

As you can see, BoxList supports changing size, style and alignments.

Quick Start
=============

BoxList is used in these procedures.

1. Create object with specifying default styles.
2. Add single or multiple items to list with optional style.
3. draw with specifying xy, size and align.

Here is an example code.

.. literalinclude:: image1.py
   :language: python
   :linenos:
   :caption: image1.py

This function call draws a bubble speech shape with a tail starting from the right edge, beginning at 30% from the bottom, extending to 70% along its path.

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    image1.png

Alignment and XY
==================

BoxList supports 4 alignment.

- ``left``: Left to right. Default
- ``right``: Right to left
- ``bottom``: Bottom to top
- ``top``: Top to bottom

Each BoxList location depends on args ``xy`` of function ``draw``.

.. literalinclude:: image1.py
   :language: python
   :linenos:
   :caption: image1.py


API Specification
====================

``BoxList()``
----------------

Initialize BoxList.

Args.

- default_box_style (Union[str, ShapeStyle, None]): The style for the boxes.
- default_text_style (Union[str, ShapeTextStyle, None]): The style for the text inside the boxes.

``append()``
---------------

Appends a new box with text to the BoxList.

Args:

- text (str): The text to be displayed inside the box.
- box_style (Union[str, ShapeStyle, None], optional): The style for the box. Can be a style name, a ShapeStyle object, or None. If None, the default box style is used.
- text_style (Union[str, ShapeTextStyle, None], optional): The style for the text inside the box. Can be a style name, a ShapeTextStyle object, or None. If None, the default text style is used.

``insert()``
--------------

Inserts a new box with text at a specified position in the BoxList.

Args:

- index (int): The position at which to insert the new box.
- text (str): The text to be displayed inside the box.
- box_style (Union[str, ShapeStyle, None], optional): The style for the box. Can be a style name, a ShapeStyle object, or None. If None, the default box style is used.
- text_style (Union[str, ShapeTextStyle, None], optional): The style for the text inside the box. Can be a style name, a ShapeTextStyle object, or None. If None, the default text style is used.

``extend()``
---------------

Extends the BoxList by appending multiple boxes with text.

Args:

- texts (List[str]): A list of texts to be displayed inside the boxes.
- box_style (Union[str, ShapeStyle, None], optional): The style for the boxes. Can be a style name, a ShapeStyle object, or None. If None, the default box style is used.
- text_style (Union[str, ShapeTextStyle, None], optional): The style for the text inside the boxes. Can be a style name, a ShapeTextStyle object, or None. If None, the default text style is used.

``draw()``
------------

Draws a list of boxes at the specified location.

Args:

- xy (Tuple[float, float]): The starting point (x, y) to draw the list of boxes.
- box_width (float): The width of each box.
- box_height (float): The height of each box.
- align (Literal["left", "right", "bottom", "top"]): The alignment of the boxes relative to the starting point.