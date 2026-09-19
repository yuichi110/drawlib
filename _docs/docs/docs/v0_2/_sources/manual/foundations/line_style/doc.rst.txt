======================
Line Style
======================

Drawlib provides six functions for drawing lines and lines with arrowheads:

* ``line()``
* ``line_curve()``
* ``line_bezier1()``
* ``line_bezier2()``
* ``lines()``
* ``lines_bezier()``

They all share the following optional arguments:

- ``arrowhead``: Specifies the type of arrowhead. Options are ``["", "->", "<-", "<->"]``.
- ``width``: Specifies the line width. This should typically be configured within the style, but it is also available as an optional argument.
- ``style``: Defines the line style. Accepts a LineStyle object or a string (style name).

These optional arguments control the line's style. 
Regarding line width, you can control it using both the ``width`` argument and the ``style`` attribute. 
We recommend using the style attribute, as it is a visual parameter. 
If you configure it in the style, you can change the line width by modifying the shared style. 
However, since many users might want to change the line width easily, the width argument is provided as a shortcut.

Additionally, we have a function called ``arrow()``. 
You might think it is similar to a line with an arrowhead, but it actually draws a thick and bold arrow shape, not an arrow line.

LineStyle
===========

The ``LineStyle`` object has the following attributes:

* width: Line width, represented as a float value.
* color: Line color, specified in RGB (0~255, 0~255, 0~255) or RGBA (0~255, 0~255, 0~255, 0~1.0). You can use the Color classes for convenience.
* alpha: Line transparency, ranging from 0.0 (totally transparent) to 1.0 (fully opaque).
* style: Line style, which can be one of ``["solid", "dashed", "dotted", "dashdot"]``. The default style is solid.
* ahfill: Arrowhead fill, indicating whether the arrowhead is filled (``True``) or not (``False``). The default is ``False``.
* ahscale: Arrowhead scale, determining the size of the arrowhead. A larger value results in a larger arrowhead. The default scale is ``20.0``.

The first four attributes (``width``, ``color``, ``alpha``, ``style``) affect both lines and lines with arrowheads. 
The last two attributes (``ahfill``, ``ahscale``) specifically affect lines with arrowheads.
This structure allows for precise control over the appearance of lines and their associated arrowheads within Drawlib.

It's important to note that whether the arrowhead is present or not carries logical meaning, so it is considered a function argument rather than a style attribute.


Drawing line with style
==========================

Let's explore different line styles through examples.

.. literalinclude:: image1.py
   :language: python
   :linenos:
   :caption: image1.py

Running this code produces the following output:

.. figure:: image1.png
    :width: 500
    :class: with-border
    :align: center

    lines with styles

This example demonstrates various line styles applied to lines using Drawlib.


Drawing line arrow with style
================================

All line functions in Drawlib support the ``arrowhead`` argument, which allows you to add arrowheads to lines.

The ``arrowhead`` argument accepts one of the following parameters:

- ``""``: No arrowhead (default).
- ``"->"``: Right arrowhead.
- ``"<-"``: Left arrowhead.
- ``"<->"``: Both right and left arrowheads.

You can customize the visual appearance of arrowheads using the following ``LineStyle`` attributes:

* ``ahfill``: Arrowhead fill. Determines whether the arrowhead is filled (``True``) or not (``False``). Default is ``False``.
* ``ahscale``: Arrowhead scale. Controls the size of the arrowhead. Larger values result in larger arrowheads. Default is ``20.0``.

Let's see an example:

.. literalinclude:: image2.py
   :language: python
   :linenos:
   :caption: image2.py

Executing this code generates the following output:

.. figure:: image2.png
    :width: 500
    :class: with-border
    :align: center

    arrow lines with styles

This example demonstrates lines with different arrowhead styles and visual configurations using Drawlib.


Theme's Pre-Defined Line Styles
=================================

Drawlib provides pre-defined line styles.
You can provide style via name easily.
What name you can use depends on theme you choose.

The style has this syntax: ``<color>_<type>_<weight>``. 

- ``<color>``: Specifies the color of the line.

``<type>`` is one of thme.

- (default): solid line
- ``solid``: solid line
- ``dashed``: dashed line

``<weight>`` is one of them

- (default): regular line width
- ``light``: half of the default width
- ``bold``: double the default width

If the type and weight are default, they may not be explicitly shown in the style name.

Let's look at an example:

.. literalinclude:: image3.py
   :language: python
   :linenos:
   :caption: image3.py

Executing this code generates the following output:

.. figure:: image3.png
    :width: 500
    :class: with-border
    :align: center

    lines with pre-defined style names

This example demonstrates lines drawn using pre-defined style names in Drawlib, showcasing different colors, line types, and thicknesses based on the specified styles.