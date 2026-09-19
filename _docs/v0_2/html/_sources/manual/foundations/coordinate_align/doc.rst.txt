==========================
Coordinate and Alignment
==========================

Drawing items accurately requires precise positioning. 
Understanding drawlib's coordinates and alignment is essential to achieve this.

Coordinate
============

Nearly all drawing functions include arguments like ``xy`` or similar, such as ``xy1`` or ``xys``. 
These represent the tuple ``(X, Y)`` coordinate of your drawing item. 
Here, ``X`` represents the x-axis value, and ``Y`` represents the y-axis value.

Let's delve into some code examples:

.. literalinclude:: image1.py
   :language: python
   :linenos:
   :caption: image1.py

In this example, setting ``config(width=10, height=10, ...)`` implies:

* x-axis: 0 to 10
* y-axis: 0 to 10

Both axes always start from 0. In this scenario, the bottom-left is (0, 0), and the top-right is (10, 10). 
Within the for loop, we plot small circles from coordinates (0, 0) to (10, 10).

Executing this code generates the following image:

.. figure:: image1.png
    :width: 600
    :class: with-border
    :align: center

    Circles from (0, 0) to (10, 10)

As you observe, (0, 0) represents the minimum value. 
Therefore, the circle at (0, 0) is only partially displayed. 
Shapes existing at values less than 0 are not drawn, and similarly, those exceeding the maximum value of 10 are omitted.

The default values for width and height are both ``100``. 
We recommend explicitly setting width and height using config() even if you're using default values to showcase the image's coordinate size.

You may need to calculate coordinates either mentally or programmatically within drawlib's code for drawing objects. 
It's advisable to use simple values such as 100 to simplify calculations. 
Setting complex values like 1920 can complicate matters. 
We prefer using ``config(width=100, height=100)`` or ``config(width=100, height=50)``.

Alignment
============

Alignment refers to the arrangement of items, such as text, images, or shapes, on drawlib's canvas. 
These items can be aligned horizontally and vertically. 
The default alignment is center horizontally and center vertically. 
You can alter alignment using ``Style`` classes for each drawing item:

* Icon: ``IconStyle``
* Image: ``ImageStyle``
* Line: ``LineStyle`` and ``LineArrowStyle``
* Shape: ``ShapeStyle`` and ``ShapeTextStyle``
* Text: ``TextStyle``

All of these have attributes:

* ``halign``: Horizontal alignment
* ``valign``: Vertical alignment

By setting values ``"left"``, ``"center"``, or ``"bottom"`` to halign and ``"bottom"``, ``"center"``, or ``"top"`` to valign, you can adjust the drawing item's alignment. 
If alignment isn't specified, ``"center"`` is applied to both halign and valign.

Let's examine the alignment of rectangles with an example code:

.. literalinclude:: image2.py
   :language: python
   :linenos:
   :caption: image2.py

In this code, we display nine variations of alignments. 
The red dot represents "xy", and the inner text indicates the alignment.

.. figure:: image2.png
    :width: 600
    :class: with-border
    :align: center

    Alignment variations.

We prefer using ``(center, center)`` and ``(left, bottom)``. 
Occasionally, we employ ``(left, center)`` and ``(center, bottom)``. 

``(left, bottom)`` is beneficial for pinpointing the exact location of rectangle-like shape items. 
However, center alignment is much simpler for aligning different-sized multiple items horizontally or vertically. 
That's why we've set ``(center, center)`` as the default for all items. 
Consistency is key.

Here's an example of aligning items horizontally and vertically:

.. literalinclude:: image3.py
   :language: python
   :linenos:
   :caption: image3.py

Each item have different size an angles. 
If we use alignment like ``(left, bottom)``, aligning items becomes complex. 
However, ``(center, center)`` is straightforward.

.. figure:: image3.png
    :width: 600
    :class: with-border
    :align: center

    Align center, center is recommended

Please consider the best alignment for placing items.
It depends on the situation.