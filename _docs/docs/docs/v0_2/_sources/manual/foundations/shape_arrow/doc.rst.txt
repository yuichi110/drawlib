======================
Drawing Arrow Shapes
======================

Introductions
================

Arrow Shapes draw thick arrow.
There are these functios

- ``arrow()``: Draw arrow from xy1 to xy2.
- ``arrow_polyline``: Draw arrow which passes list of xys.
- ``arrow_l``: Draw L shape arrow from top left to right bottom.
- ``arrow_u``: Draw U shape arrow from top left to right top.
- ``arrow_arc``: Draw ellipse arc arrow from start angle to end angle.

Here are arrow examples:

.. figure:: image_introduction.png
    :width: 600
    :class: with-border
    :align: center

    arrow()

Name of Arguments
====================

All arrow functions have similar argument namings.
Understanding how to specify arrow size might be useful.

.. figure:: image_args1.png
    :width: 600
    :class: with-border
    :align: center

    Arrow size arguments.

- ``xy`` means coordinate of arrow. ``xy1`` and ``xy2``, ``xys`` are used.
- ``tail_width``: Tail width of arrow
- ``head_width``: Head width of arrow
- ``head_length``: Head length of arrow

You can specify arrow direction via arg ``head``.

.. figure:: image_args2.png
    :width: 600
    :class: with-border
    :align: center

    Arrow size arguments.

- ``->``: Draw arrow head at end of xy
- ``<-``: Draw arrow head at start of xy
- ``<->``: Draw arrow head at both start and end of xy


Functions
==============

arrow()
---------

The ``arrow()`` function draws an arrow shape between two points defined by ``xy1`` (start point) and ``xy2`` (end point). 
You can customize the arrow's tail and head sizes and styles.

This function accepts the following arguments:

- xy1: Start point coordinates (x1, y1)
- xy2: End point coordinates (x2, y2)
- tail_width: Width of the arrow's tail (not the head)
- head_width: Width of the arrow's head
- head_length: Length of the arrow's head
- head (optional): Style of the arrow's head (``"->"``, ``"<-"``, ``"<->"`` for different configurations)
- style (optional): Style of the arrow
- text (optional): Centered text
- textstyle (optional): Style of the centered text

Let's explore an example:

.. literalinclude:: image_arrow1.py
   :language: python
   :linenos:
   :caption: image_arrow1.py

Here is an example output:

.. figure:: image_arrow1.png
    :width: 600
    :class: with-border
    :align: center

    arrow()

In the ``arrow()`` function, the angle of the arrow is determined automatically by its start and end points. 
The function does not use the alignment attributes (``halign`` and ``valign``) from ``ShapeStyle``.

arrow_polyline
------------------

The ``arrow_polyline`` function draws an arrow which passes ``xys`` points.
It supports rounded edges.
It doesn't support having text inside.

- xys: List of arrow coordinates.
- tail_width: Width of the arrow's tail (not the head)
- head_width: Width of the arrow's head
- head_length: Length of the arrow's head
- head (optional): Style of the arrow's head (``"->"``, ``"<-"``, ``"<->"`` for different configurations)
- r (optional): R of arrow line
- style (optional): Style of the arrow
- text (optional): Centered text
- textstyle (optional): Style of the centered text

Let's explore an example:

.. literalinclude:: image_arrow_polyline.py
   :language: python
   :linenos:
   :caption: image_arrow_polyline.py

Here is an example output:

.. figure:: image_arrow_polyline.png
    :width: 600
    :class: with-border
    :align: center

    arrow_polyline()


arrow_l
----------

The ``arrow_l`` function is syntax sugar of ``arrow_polyline``.
It draw "L" style arrow easily by specifying ``width`` and ``height`` and ``angle``.

- xys: Center of arrow shape.
- width: width of arrow
- height: height of arrow
- tail_width: Width of the arrow's tail (not the head)
- head_width: Width of the arrow's head
- head_length: Length of the arrow's head
- head (optional): Style of the arrow's head (``"->"``, ``"<-"``, ``"<->"`` for different configurations)
- r (optional): R of arrow line
- angle (optional): Angle of arrow
- style (optional): Style of the arrow


Let's explore an example:

.. literalinclude:: image_arrow_l.py
   :language: python
   :linenos:
   :caption: image_arrow_l.py

Here is an example output:

.. figure:: image_arrow_l.png
    :width: 600
    :class: with-border
    :align: center

    arrow_l()

You need to change ``angle`` and direction of arrow ``head`` for drawing various style of L arrow. 

arrow_u
----------

The ``arrow_u`` function is syntax sugar of ``arrow_polyline``.
It draw "U" style arrow easily by specifying ``width`` and ``height`` and ``angle``.

- xy: Center of arrow shape.
- width: width of arrow
- height: height of arrow
- tail_width: Width of the arrow's tail (not the head)
- head_width: Width of the arrow's head
- head_length: Length of the arrow's head
- head (optional): Style of the arrow's head (``"->"``, ``"<-"``, ``"<->"`` for different configurations)
- r (optional): R of arrow line
- angle (optional): Angle of arrow
- style (optional): Style of the arrow


Let's explore an example:

.. literalinclude:: image_arrow_u.py
   :language: python
   :linenos:
   :caption: image_arrow_u.py

Here is an example output:

.. figure:: image_arrow_u.png
    :width: 600
    :class: with-border
    :align: center

    arrow_u()


You need to change ``angle`` and direction of arrow ``head`` for drawing various style of L arrow. 
  

arrow_arc
------------

The ``arrow_arc`` function draw arc on ellipse and circle(when width and height are same).
It specify ellipse ``width`` and ``height``.
And also, you can specify where arrow start and end via ``angle_start`` and ``angle_end``.
Please take care, length of head is specified by ``head_angle``.
``head_angle=N`` means drawing head within N degree.

- xy: Center of arrow shape.
- width: width of ellipse
- height: height of ellipse
- tail_width: Width of the arrow's tail (not the head)
- head_width: Width of the arrow's head
- head_angle: Length of the arrow's head by degree
- head (optional): Style of the arrow's head (``"->"``, ``"<-"``, ``"<->"`` for different configurations)
- angle_start (optional): Where the arrow start. default is 0.
- angle_end (optional): Where the arrow end. default is 360.
- angle (optional): Angle of arrow
- style (optional): Style of the arrow

Let's explore an example:

.. literalinclude:: image_arrow_arc.py
   :language: python
   :linenos:
   :caption: image_arrow_arc.py

Here is an example output:

.. figure:: image_arrow_arc.png
    :width: 600
    :class: with-border
    :align: center

    arrow_arc()

Please remember, arrow is always drawn from ``angle_start`` to ``angle_end`` counterclockwise.
If you want to draw clockwise arrow, please specify it via ``head``.