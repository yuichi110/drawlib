=============
BulletPoints
=============

Class ``dsart.BulletPoints`` is used for drawing bullet points.

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    image1.png

As you can see, you can control text style and bullet point styles.

API Specification
======================

``dsart.BulletPoints()``
--------------------------

Args:

- vertical_margin (float): The vertical space between bullet points.
- indent_width (float): The width of the indentation for each level.
- default_style (Union[str, TextStyle, None]): The default text style for the bullet points.

``set_indent()``
-----------------

Sets the indentation level for the next bullet point.

Args:

- level (int): The indentation level.

``set_bullet_style()``
-------------------------

Sets the style and function for drawing bullets at a specific indentation level.

Args:

- indent_level (int): The indentation level to apply the style to.
- function (Callable): The function to draw the bullet shape.
- style (Union[str, ShapeStyle]): The style to apply to the bullet shape.
- args (dict): Additional arguments to pass to the drawing function.

``add()``
-----------

Adds a bullet point with the specified text and style.

Args:

- text (str): The text for the bullet point.
- style (Union[str, TextStyle, None]): The text style for the bullet point.

``draw()``
-------------

Draws the list of bullet points starting from the specified location.

Args:

xy (Tuple[float, float]): The starting point (x, y) to draw the bullet points.
